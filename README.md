# MCP with the OpenAI Agents SDK

Examples of connecting OpenAI Agents SDK agents to Model Context Protocol (MCP) servers: a local Streamable HTTP MCP server, a client that talks to it through a custom `httpx` client, and an agent that uses the hosted DeepWiki MCP server with a tool-approval callback.

## Files

| File | What it demonstrates |
|------|----------------------|
| `server.py` | A local MCP server built with `FastMCP` over Streamable HTTP, exposing two tools: `add(a, b)` and `get_secret_word()`. |
| `streammain.py` | Starts `server.py` in a subprocess (via `uv run`), connects with `MCPServerStreamableHttp` using a custom `httpx_client_factory` (custom headers and timeouts, SSL verification off for testing), and asks an agent to add 7 and 22. Prints a trace link. |
| `stdio_mcpserver.py` | Interactive assistant using `HostedMCPTool` with the public DeepWiki MCP server (`https://mcp.deepwiki.com/mcp`). An `on_approval_request` callback auto-approves read-only tools and rejects anything else. Despite the file name, it does not use a stdio server. |

## Tech stack

Python 3.10+, `openai-agents`, `mcp`, `httpx`, `python-dotenv`, and [uv](https://docs.astral.sh/uv/) (used by `streammain.py` to launch the server).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then fill in the values
```

| Variable | Required | Description | Where to get it |
|----------|----------|-------------|-----------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key, read automatically by the SDK | https://platform.openai.com/api-keys |
| `STREAMABLE_HTTP_HOST` | No | Host for the local MCP server (default `127.0.0.1`) | Choose locally |
| `STREAMABLE_HTTP_PORT` | No | Port for the local MCP server (default `18080` for `server.py`; a random free port for `streammain.py`) | Choose locally |

## Running

```bash
# Local MCP server + client demo (starts server.py for you; requires uv)
python streammain.py

# Hosted DeepWiki MCP assistant (type "exit" to quit)
python stdio_mcpserver.py

# Run the MCP server on its own
python server.py
```

## Connecting another MCP client to `server.py`

When run on its own, `server.py` serves Streamable HTTP at:

```
http://127.0.0.1:18080/mcp
```

Point any MCP client that supports Streamable HTTP at that URL. With the Agents SDK:

```python
MCPServerStreamableHttp(name="echo", params={"url": "http://127.0.0.1:18080/mcp"})
```
