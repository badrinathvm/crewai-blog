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
    
# JSON Crew Agent Implementation
class SummarizeRequest(BaseModel):
    question: str = Field(..., description="questions to be answered")
    
class JSONAgent:
    def run(self, question: str):
        try:
            file_path = "src/blog_creator/mock.json"
            data = read_json(file_path)
            inputs={'json_content': data, 'questions': question}
            result = JsonCrew().crew().kickoff(inputs=inputs)
            return result.raw
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


def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in the file '{file_path}'.")
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.blog_creator.main:app", host="0.0.0.0", port=8002)

# To run the server, use the command:
# uvicorn main:app --host 0.0.0.0 --port 8002 --reload