# Google Calendar MCP Agent

A LangGraph ReAct agent that manages your Google Calendar in natural language by calling tools over the Model Context Protocol (MCP).

## What it does
- Connects to the `@cocal/google-calendar-mcp` server over stdio and loads its tools at runtime
- Lets you read and manage calendar events by chatting ("what's on my calendar tomorrow?", "book 30 minutes on Friday")
- Ships a second, built-from-scratch math MCP server (`app/math/`) as a minimal reference for writing your own MCP tools

## How it works
Groq Llama-4-Scout drives a `create_react_agent` loop. MCP tools are loaded through `langchain-mcp-adapters`, so the agent discovers tools at runtime instead of hard-coding API calls.

## Run
```bash
pip install -r requirements.txt
# set GROQ_API_KEY and your Google OAuth credentials path (see app/main.py)
python -m app.main
```
