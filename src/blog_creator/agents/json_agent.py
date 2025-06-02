from pydantic import BaseModel, Field
from fastapi import HTTPException
from src.blog_creator.json_crew import JsonCrew
import json

class SummarizeRequest(BaseModel):
    question: str = Field(..., description="questions to be answered")
    
class JSONAgent:
    def read_json(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON in the file '{file_path}'.")
        return None
    
    def run(self, question: str):
        try:
            file_path = "src/blog_creator/mock.json"
            data = self.read_json(file_path)
            inputs={'json_content': data, 'questions': question}
            result = JsonCrew().crew().kickoff(inputs=inputs)
            return result.raw
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
   