import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import mcp_server_tools,StdioServerParams
import os
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
load_dotenv()

NOTION_API_KEY=os.getenv('NOTION_SECRET')
GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')

SYSTEM_MESSAGE="You are a helpful assistant that can search and summarize content from the user's Notion workspace and also list what is asked . Try to assume the tool and call the same and get the answer. Say TERMINATE when you are donewith the task."

async def config():
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



async def orchestrate(team,task):
    async for message in team.run_stream(task=task):
        yield message
        
async def main():
    team=await config()
    task='Create a new page titled "PageFromMCPNotion" '
    
    async for msg in orchestrate(team,task):
        print('-'*100)
        print(msg)
        print('-'*100)
        
        
if __name__=='__main__':
    asyncio.run(main())