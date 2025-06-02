from crewai import Agent, Task, Crew, Process, LLM
import os 
from dotenv import load_dotenv
from crewai.project import CrewBase, agent, task, crew, before_kickoff
from fastmcp import FastMCP
import httpx
from typing import Any
from mcp import ClientSession
from mcp.client.sse import sse_client
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp import Client
import uvicorn

# Initialize the FASTMCP server
mcp = FastMCP(name="weather")

# Your existing constants and functions
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/0.1"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API and return the response data with proper error handling"""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try: 
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            mcp.log.error(f"Error fetching data from NWS: {e}")
            return None

def format_alert(feature: dict) -> str:
    """Format a weather alert feature into a readable string"""
    props = feature["properties"]
    return f"""
        Event: {props.get('event', 'Unknown')}
        Area: {props.get('areaDesc', 'Unknown')}
        Severity: {props.get('severity', 'Unknown')}
        Description: {props.get('description', 'No description available')}
        Instructions: {props.get('instruction', 'No specific instructions provided')}
    """

# Your existing MCP tool - THIS IS WHERE @mcp.tool() IS USED
@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get current weather alerts for a specific state
    
    Args:
        state (str): The two-letter state code (e.g., 'CA', 'NY')
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)
    
    if not data or "features" not in data:
        return "No active alerts found for the given state"
    
    if not data["features"]:
        return "No active alerts found for the given state"
    
    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n\n".join(alerts)

@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo message as a resource"""
    return f"Resource Echo: {message}"


### Client for MCP 
class MCPStreamableTTPClientManager:
    def __init__(self):
        self.transport = StreamableHttpTransport(
            "http://127.0.0.1:8002/mcp/",
             headers= {
                "Accept": "text/event-stream, application/json",
                "Content-Type": "application/json",
                "User-Agent": "MCP-Client/1.0" 
        })
        
    async def list_tools(self):
        try:
            async with Client(transport=self.transport) as client:
                # Test Connection 
                await client.ping()
                print("Ping Successful")
                return await client.list_tools()
        except Exception as e:
            print(f"Error Occured {e}")
            
    async def call_tool(self, state):
        try:
            async with Client(transport=self.transport) as client:
                # Test Connection 
                await client.ping()
                print("Ping Successful")
                return await client.call_tool("get_alerts", {"state": state})
        except Exception as e:
            print(f"Error Occured {e}")
        
            
# Run the server
if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host= "127.0.0.1",
        port= 8002
    )