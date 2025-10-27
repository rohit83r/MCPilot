# 🤖 MCP Pilot — AI-Powered Agent for Notion via Model Context Protocol (MCP)

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-green)
![Ngrok](https://img.shields.io/badge/ngrok-secure%20tunnel-orange)
![MCP](https://img.shields.io/badge/Protocol-Model%20Context%20Protocol-purple)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

> **MCP Pilot** is an AI-powered agent that connects to your **Notion workspace** through the **Model Context Protocol (MCP)** — allowing you to **create, read, write, and update** Notion pages simply by *talking* to the AI.

---

## 🧠 Overview

MCP Pilot turns your Notion into an intelligent workspace companion.

It uses:
- **Flask** as the backend web server  
- **ngrok** to expose a secure public API  
- **Gemini (or OpenAI)** as the LLM  
- **Autogen + MCP** to connect and interact with Notion tools  

With MCP Pilot, you can run commands like:

> “Create a Notion page titled *Weekly Summary*”  
> “Summarize my notes from last week.”  
> “Update the Project X page with new milestones.”

The agent communicates with Notion **entirely via MCP**, no manual API coding needed.

---

## ⚙️ Tech Stack

| Component | Description |
|------------|-------------|
| **Backend** | Flask (Python) |
| **AI Model** | Gemini / OpenAI via Autogen |
| **MCP Interface** | Notion MCP (`https://mcp.notion.com/mcp`) |
| **Networking** | ngrok (for public HTTPS tunnel) |
| **Frontend** | Lovable.dev (optional for UI demo) |
| **Async Runtime** | asyncio-based agent tasks |

---

## 🚀 Features

✅ Connects securely to Notion via MCP  
✅ Create, read, and update pages with natural language  
✅ Works locally using ngrok (no cloud deploy required)  
✅ Provides REST API endpoints for integration  
✅ Built on async Autogen Agent framework  
✅ Easy to extend for multiple MCP tools  

---

## 🧩 API Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/health` | Health check (verifies server status) |
| `GET` | `/` | Root endpoint |
| `POST` | `/run` | Run an AI task on Notion |

### Example Request

```bash
curl -X POST https://<your-ngrok-url>/run \
  -H "Content-Type: application/json" \
  -d '{"task": "Create a new Notion page titled MCP Pilot Overview"}'
````

### Example Response

```json
{
  "status": "success",
  "result": "Notion page 'MCP Pilot Overview' created successfully."
}
```

---

## 🧪 Setup Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/rohit83r/MCPilot.git
cd MCPilot
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # on macOS/Linux
venv\Scripts\activate      # on Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create a `.env` File

Create a file named `.env` in the project root and add:

```bash
NOTION_SECRET=your_notion_integration_secret
GEMINI_API_KEY=your_gemini_or_openai_key
NGROK_AUTH_TOKEN=your_ngrok_auth_token
```

> 💡 You can create a Notion integration and get your secret from:
> [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)

### 5️⃣ Run the Flask Server

```bash
python final.py
```

You’ll see output like:

```
Public URL: https://xxxx.ngrok.io/health

 * Running on http://127.0.0.1:7001
```

Visit the public URL in your browser to verify!

---

## 🧠 Architecture

```
            ┌──────────────────────────┐
            │        Frontend UI       │
            │    (Lovable / Postman)   │
            └────────────┬─────────────┘
                         │
                         ▼
              ┌─────────────────┐
              │  Flask Web API  │
              │ (/run, /health) │
              └────────┬────────┘
                       │
                       ▼
              ┌───────────────────────────────┐
              │   Autogen AI Agent (Gemini)   │
              │  └──> MCP Tools for Notion    │
              └───────────────────────────────┘
                       │
                       ▼
              ┌────────────────────────────┐
              │   Notion MCP Endpoint      │
              │   https://mcp.notion.com   │
              └────────────────────────────┘
```



## 💬 Example Use Cases

* Create project documentation directly in Notion
* Auto-update your task lists from meeting summaries
* Summarize and organize your notes
* Build custom AI-driven Notion workflows

---

## 📜 License

This project is licensed under the **MIT License**
---

## 💡 Contribute

Pull requests are welcome!
If you’d like to contribute:

1. Fork the repo
2. Create a feature branch
3. Commit and push
4. Open a PR

---

## 🌟 Support

If you like this project, please ⭐ **star the repository** and share it on LinkedIn or Twitter!

> Built by **Rohit Srivas** — exploring the future of Agentic AI, MCP, and intelligent automation 🚀

---

