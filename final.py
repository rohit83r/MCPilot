import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import mcp_server_tools,StdioServerParams
import os
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, jsonify
from pyngrok import ngrok
from flask_cors import CORS
import requests


NOTION_API_KEY=os.getenv('NOTION_SECRET')
GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")

SYSTEM_MESSAGE="You are a helpful assistant that can search and summarize content from the user's Notion workspace and also list what is asked . Try to assume the tool and call the same and get the answer. Say TERMINATE when you are donewith the task."

port=7001
app=Flask(__name__)
CORS(app)

async def setup():
    params=StdioServerParams(
        command='npx',
        args=['-y','mcp-remote','https://mcp.notion.com/mcp'],
        env={
            'NOTION_API_KEY':NOTION_API_KEY
        },
        read_timeout_seconds=20   
    )
    
    model = OpenAIChatCompletionClient(
        model='gemini-2.0-flash',
        api_key=GEMINI_API_KEY
    )
    
    mcp_tools = await mcp_server_tools(server_params=params)
    
    # Depending on the capability of the agent we can filter the tools if our agent is powerful enough, there is no need to filter the tools. Use Paid Version of the OPENAI API and good model for best use case. 
    # mcp_tools = [t for t in mcp_tools if "create" in t.name] 
    
    agent =AssistantAgent(
        name='Notion_Agent',
        system_message=SYSTEM_MESSAGE,
        model_client=model,
        tools=mcp_tools,
        reflect_on_tool_use=True
    )
    
    team=RoundRobinGroupChat(
        participants=[agent],
        max_turns=5,
        termination_condition=TextMentionTermination("TERMINATE")
    )
    
    return team

async def run_task(task:str)->str:
    team=await setup()
    output=[]
    async for msg in team.run_stream(task=task):
        output.append(str(msg))
    return '\n\n\n\n'.join(output)


#===============================================================================================================================================================================#

@app.route('/health',methods=['GET'])
def health():
    return jsonify({"status":"OK","message":"Notion MCP Flask App is Live"}),200

@app.route('/',methods=['GET'])
def root():
    return jsonify({"status":"OK","message":"MCP Notion app is live , use /health or /run to work"}),200

@app.route('/run',methods=['POST'])
def run():
    try:
        data =requests.get_json()
        task=data.get('task')
        
        if not task:
            return jsonify({'error':'Task is required'}),400
        
        print (f'Got the task {task}')
        
        result=asyncio.run(run_task(task))
        return jsonify({'status':'success','result':result}),200
    except Exception as e:
        return jsonify({'status':'error','result':str(e)}),500
        
        
if __name__=='__main__' :
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    public_url=ngrok.connect(port).public_url
    print(f"Public URL:{public_url}/api/hello \n\n")
    
    app.run(port=port)    