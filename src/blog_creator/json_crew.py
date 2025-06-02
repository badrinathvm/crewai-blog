from crewai import Agent, Task, Crew, Process, LLM
import os 
from dotenv import load_dotenv
from crewai.project import CrewBase, agent, task, crew, before_kickoff

load_dotenv()

@CrewBase
class JsonCrew():
    def __init__(self):
        #os.environ["G"] = "http://127.0.0.1:11434"
        os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        #self.llm = LLM(model="groq/qwen-qwq-32b")
        self.llm = LLM(model="ollama/llama3.2:latest", base_url="http://127.0.0.1:11434")
        #self.llm = LLM(model="gpt-4o-mini")
        
    agents_config = 'config/json_agents.yaml'
    tasks_config = 'config/json_tasks.yaml'
    
    @before_kickoff
    def before_kickoff(self, inputs):
        """This method will be called before the crew starts"""
        print(f"Before kickoff: {inputs}")
        return inputs
    
    @agent
    def json_reader(self) -> Agent:
        """
        Agent responsible for reading a JSON file.
        """
        return Agent(
            config=self.agents_config['json_reader'],
            llm=self.llm,
            verbose=True
        )
        
    @task
    def generate_summary_task(self) -> Task:
        """
        Task to generate a summary of the content of the JSON file.
        """
        return Task(
            config=self.tasks_config['generate_summary_task']
        )
    
        
    @crew
    def crew(self):
        """
        Crew to read a JSON file and return the content.
        """
        return Crew(
            name="Json Crew",
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )