from mcp.client.sse import sse_client
from mcp import ClientSession
from mcp.server.fastmcp import FastMCP
from typing import Dict,Any
import httpx
import logging
#from src.blog_creator.server.weather_streamable_http import make_nws_request, format_alert, NWS_API_BASE

logger = logging.getLogger(__name__)

mcp = FastMCP(
    name= "weather",
    host= "127.0.0.1",
    port=8003
)

logger.info("Starting weather SSE server...")
logger.info("Server initialized successfully")

# Your existing constants and functions
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/0.1"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API and return the response data with proper error handling"""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    print("COntrol isndie")
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

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get current weather alerts for a specific state
    
    Args:
        state (str): The two-letter state code (e.g., 'CA', 'NY')
    """
    logger.info(f"Tool called: {state}")
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)
    
    if not data or "features" not in data:
        return "No active alerts found for the given state"
    
    if not data["features"]:
        return "No active alerts found for the given state"
    
    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n\n".join(alerts)

### Client for MCP 
class MCPSSEClientManager:
    def __init__(self) -> None:
        self.url = "http://localhost:8003/sse"
            
    async def list_tools(self):
        try:
            async with sse_client(self.url) as (read_stream, write_stream):
                async with ClientSession(read_stream=read_stream,write_stream=write_stream) as session:
                    # Initialze the connection
                    await session.initialize()
                    
                    tools = await session.list_tools()
                    return tools
        except Exception as e:
            print(f"Exception : {e}")
            
    async def call_tool(self, state):
        try:
            async with sse_client(self.url) as (read_stream, write_stream):
                async with ClientSession(read_stream=read_stream, write_stream=write_stream) as session:
                   # Initialze the connection
                    await session.initialize()
                    
                    # make a tool call
                    result = await session.call_tool("get_alerts", {"state": state})
                    return result
        except Exception as e:
            raise e
        
# Run the server
if __name__ == "__main__":
    mcp.run(
        transport="sse"
    )