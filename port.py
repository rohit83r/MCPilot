from flask import Flask, jsonify
import os
from pyngrok import ngrok
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")

app=Flask(__name__)
CORS(app)



@app.route('/api/hello',methods=['GET'])
def hello():
    return jsonify({"message":"Hello, World! from windows via Terminal"})

if __name__ == '__main__' :
    port=7001
    os.environ['FLASK_ENV']='development'
    
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    public_url=ngrok.connect(port).public_url
    print(f"Public URL:{public_url}/api/hello \n\n")
    
    app.run(port=port)