from crewai import Agent, Task, Crew, Process, LLM
import os
from dotenv import load_dotenv
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
import yaml

@CrewBase
class BlogCrew():
    """
    A Crew for managing blog posts.
    """

    @before_kickoff
    def before_kickoff(self, inputs):
        """This method will be called before the crew starts"""
        print(f"Before kickoff: {inputs}")
        return inputs
    
    @after_kickoff
    def after_kickoff(self, results):
        """This method will be called after the crew finishes"""
        print(f"After kickoff: {results}")
        return results
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def blog_writer(self) -> Agent:
        """
        Agent responsible for writing blog posts.
        """
        self.llama = LLM(
            model="ollama/llama3.2:latest",
            base_url="http://127.0.0.1:11434")
        
        return Agent(
            config=self.agents_config['blog_writer'],
            llm=self.llama,
            verbose=True
        )
    
    @agent
    def title_generator(self) -> Agent:
        """
        Agent responsible for generating a title for a blog post.
        """
        return Agent(
            config=self.agents_config['title_generator'],
            llm=self.llama,
            verbose=True
        )

    @task
    def write_content_task(self) -> Task:
        """
        Task to write a blog post on a given topic.
        """
        return Task(
            config=self.tasks_config['write_content_task']
        )
        
    # @task
    # def compile_blog_task(self) -> Task:
    #     """
    #     Task to compile the title and content into a structured format.
    #     """
    #     return Task(
    #         description="""
    #         Compile the generated title and content into a JSON format.
    #         Use the title from the title generation task and the content from the content writing task.
            
    #         Return the result in this exact JSON format:
    #         {
    #             "title": "The generated title here",
    #             "content": "The generated content here"
    #         }
            
    #         Make sure the JSON is valid and properly formatted.
    #         """,
    #         expected_output="A JSON object with 'title' and 'content' fields",
    #         agent=self.blog_writer(),
    #         context=[self.generate_title_task(), self.write_content_task()]
    #     )
    
    @task
    def generate_title_task(self) -> Task:
        """
        Task to generate a title for a blog post on a given topic.
        """
        return Task(
            config=self.tasks_config['generate_title_task']
        )

    @crew
    def crew(self):
        """
        Crew that manages the blog writing process.
        """
        return Crew(
            name="Blog Crew",
            agents= self.agents, # Automatically created by the @agent decorator
            tasks= self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
        )