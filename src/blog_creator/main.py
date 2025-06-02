from fastapi import FastAPI, HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
import os 
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, task, crew
from src.blog_creator.crew import BlogCrew
from src.blog_creator.json_crew import JsonCrew
import json
from src.blog_creator.agents.json_agent import JSONAgent, SummarizeRequest
from src.blog_creator.server.weather_streamable_http import MCPStreamableTTPClientManager
from src.blog_creator.server.weather_sse import MCPSSEClientManager
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp import Client
from mcp_use import MCPAgent, MCPClient
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq

app = FastAPI(
    title="Blog Crew API",
    description="API for managing blog posts using CrewAI", 
    version="1.0.0"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request for the 
class BlogRequest(BaseModel):
    topic: str = Field(..., description="The topic of the blog post to be written")
    
# Response for the blog post
class BlogResponse(BaseModel):
   # title: str = Field(..., description="The title of the blog post")
    content: str = Field(..., description="The content of the blog post")
    
class BlogAgent:
    def __init__(self, topic: str):
        load_dotenv()
        self.topic = topic
    
    def run(self):
        try:
            inputs={'topic': self.topic}
            result = BlogCrew().crew().kickoff(inputs=inputs)
            return result.raw
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.post("/write_post", response_model=BlogResponse)
async def write_post(request: BlogRequest):
    """
    Endpoint to write a blog post on a given topic.
    """
    crew = BlogAgent(topic=request.topic)
    try:
        result = crew.run()
        return BlogResponse(content=result)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/summarize")
async def summarize(request: SummarizeRequest):
    """
    Endpoint to summarize a given type.
    """
    try:
        crew = JSONAgent()
        result = crew.run(question=request.question)
        return {"content": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


class WeatherRequest(BaseModel):
    type: str = Field(..., description="Type of the mcp connection either sse or streamable-http")
    state: str = Field(..., description="Provide the state for eg: CA")
    

@app.post("/weather")
async def get_weather(request: WeatherRequest):
    """List available MCP tools"""
    try:
        if request.type == "streamable-http":
            mcp_streamable_http_client = MCPStreamableTTPClientManager()
            tools = await mcp_streamable_http_client.list_tools()
            result = await mcp_streamable_http_client.call_tool(state=request.state)
            return {
                "tools": tools,
                "result": result
            }
        elif request.type == "sse":
            mcp_sse_client = MCPSSEClientManager()
            tools = await mcp_sse_client.list_tools()
            result = await mcp_sse_client.call_tool(state=request.state)
            return {
                "tools": tools,
                "result": result
            }
        elif request.type == "config":
            load_dotenv()
            current_dir = Path(__file__).parent
            # IF we want to debug mcp server use weather_debug.json , make sure to run the weather_sse file in debug mode.
            # However if we use weather.json a seeprate process will be triggered wont be able to debug
            config_file = current_dir / "config" / "weather.json"
            client = MCPClient.from_config_file(config_file)
            llm = ChatGroq(model="qwen-qwq-32b")
            
            agent = MCPAgent(llm=llm, client=client,  max_steps=15, memory_enabled=True)
            result = await agent.run(request.state)
            return {
                "result": result
            }
    except Exception as e:
        raise e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.blog_creator.main:app", host="0.0.0.0", port=8001)

# To run the server, use the command:
# uvicorn main:app --host 0.0.0.0 --port 8002 --reload