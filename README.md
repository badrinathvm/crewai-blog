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

## License

Blog Generator is open-sourced under the MIT License.
