![CrewAI](https://miro.medium.com/v2/resize:fit:1400/0*-7HC-GJCxjn-Dm7i.png)

## Introduction

Blog Generator leverages the CrewAI framework to generate blog content using FASTAPI.

## CrewAI Framework

CrewAI simplifies the orchestration of role-playing AI agents. In VacAIgent, these agents collaboratively decide on cities and craft a complete itinerary for your trip based on specified preferences, all accessible via a streamlined Streamlit user interface.


## Details & Explanation

- **Components**:
  - `./crew.py`: Contains agents and task leveraging crew decorators


## Using LLM Models

To switch LLMs from differnet Providers

```python
    self.llm = LLM(model="gemini/gemini-2.0-flash")
    return Agent(
            config=self.agents_config['blog_writer'],
            llm=self.llm,
            verbose=True
        )
```
[Connect to LLMs](https://docs.crewai.com/how-to/llm-connections#connect-crewai-to-llms)



### Integrating Ollama with CrewAI

Pass the Ollama model to agents in the CrewAI framework:

```python
    self.ollama = LLM(
            model="ollama/llama3.2:latest",
            base_url="http://127.0.0.1:11434")
    
    agent = Agent(
        role='Local AI Expert',
        goal='Process information using a local model',
        backstory="An AI assistant running on local hardware.",
        llm=self.ollama
    )
```

### Integrating MCP servers

# Weather MCP Server

This project demonstrates different approaches to connecting and debugging MCP (Model Context Protocol) servers for weather data retrieval.

## 📁 Project Structure

```
/server/          # MCP server implementations
/config/          # Configuration files for MCP connections
├── weather.json        # Production config (spawns separate process)
├── weather_debug.json  # Debug config (connects to running server)
```

## 🌐 FastAPI Endpoint

The project exposes a `/weather` endpoint that supports multiple connection types:

```bash
POST curl --location 'http://127.0.0.1:8001/weather' \
--header 'Content-Type: application/json' \
--data '{
    "type": "sse/streamable-http/config",
    "state": "CA"
}'
```

### Connection Types

| Type | Description | Use Case |
|------|-------------|----------|
| `sse` | Server-Sent Events connection | Real-time streaming |
| `streamable-http` | HTTP streaming connection | HTTP-based streaming |
| `config` | Configuration file-based connection | Production deployment |

## 🔧 MCP Server Connections

### 1. SSE (Server-Sent Events)
Direct connection to MCP server using Server-Sent Events protocol.

### 2. Streamable HTTP
HTTP-based connection with streaming capabilities for real-time data.

### 3. Config-Based Connection
Reads configuration from `/config` directory and establishes MCP server connection based on the settings.

## 🐛 Debugging Guide

### For Development/Debugging

1. **Use `weather_debug.json` configuration**
   - This connects to an already running MCP server
   - Allows breakpoints and debugging in your MCP server code

2. **Run the MCP server manually in debug mode**
   ```bash
   # Start weather_sse.py in VS Code debug mode or terminal
   python server/weather_sse.py
   ```

3. **Configuration for debugging**
   ```json
   {
     "_comment": "Debug configuration - connects to running server",
     "mcpServers": {
       "weather": {
         "url": "http://127.0.0.1:8003/sse"
       }
     }
   }
   ```

### For Production

1. **Use `weather.json` configuration**
   - Automatically spawns a separate MCP server process
   - No debugging capabilities (separate process)

2. **Configuration for production**
   ```json
   {
     "_comment": "Production configuration - spawns separate process",
     "mcpServers": {
       "weather": {
         "command": "/path/to/uv",
         "args": [
           "run",
           "--with", "mcp[cli]",
           "mcp", "run",
           "/path/to/weather_sse.py"
         ]
       }
     }
   }
   ```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
uv add "mcp[cli]"
# or
pip install "mcp[cli]"
```

### 2. For Development (with debugging)
```bash
# Terminal 1: Start MCP server in debug mode
python server/weather_sse.py

# Terminal 2: Use debug config
curl "http://localhost:8000/weather?type=config&location=CA"
# Make sure to use weather_debug.json
```

### 3. For Production
```bash
# Uses weather.json - spawns separate process automatically
curl --location 'http://127.0.0.1:8000/weather' \
--header 'Content-Type: application/json' \
--data '{
    "type": "config",
    "state": "CA"
}'
```

### 4. Direct Connection Examples
```bash
# SSE connection
curl --location 'http://127.0.0.1:8000/weather' \
--header 'Content-Type: application/json' \
--data '{
    "type": "sse",
    "state": "CA"
}'

# Streamable HTTP connection
curl --location 'http://127.0.0.1:8000/weather' \
--header 'Content-Type: application/json' \
--data '{
    "type": "streamable-http",
    "state": "CA"
}'
```

## ⚠️ Important Notes

- **Debugging**: Only possible with `weather_debug.json` + manually running the MCP server
- **Production**: Use `weather.json` for automatic process management (no debugging)
- **Process Separation**: `weather.json` spawns a separate process, making breakpoints ineffective
- **Development Flow**: Always use debug configuration during development for proper debugging experience

## 🔍 Troubleshooting

### Breakpoints Not Working?
- ✅ Check you're using `weather_debug.json`
- ✅ Ensure MCP server is running manually in debug mode
- ✅ Verify the debug config points to the correct URL/port

### Connection Refused?
- ✅ Confirm MCP server is running on the expected port
- ✅ Check firewall/network settings
- ✅ Verify configuration file paths and settings

### Process Not Found?
- ✅ When using `weather.json`, ensure all paths in the config are correct
- ✅ Check that `uv` and dependencies are properly installed
- ✅ Verify file permissions for the MCP server script

## 📝 Configuration Reference

### Debug Configuration (`weather_debug.json`)
```json
{
  "mcpServers": {
    "weather": {
      "url": "http://127.0.0.1:8003/sse"
    }
  }
}
```

### Production Configuration (`weather.json`)
```json
{
  "mcpServers": {
    "weather": {
      "command": "/usr/local/bin/uv",
      "args": [
        "run",
        "--with", "mcp[cli]",
        "mcp", "run",
        "/absolute/path/to/weather_sse.py"
      ]
    }
  }
}
```


## License

Blog Generator is open-sourced under the MIT License.
