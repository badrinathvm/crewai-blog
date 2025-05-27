![CrewAI](https://miro.medium.com/v2/resize:fit:1400/0*-7HC-GJCxjn-Dm7i.png)

## Introduction

Blog Generator leverages the CrewAI framework to generate blog content using FASTAPI.

## CrewAI Framework

CrewAI simplifies the orchestration of role-playing AI agents. In VacAIgent, these agents collaboratively decide on cities and craft a complete itinerary for your trip based on specified preferences, all accessible via a streamlined Streamlit user interface.


## Running the Application

To experience the VacAIgent app:

- **Configure Environment**: Set up the environment variables for [Browseless](https://www.browserless.io/), [Serper](https://serper.dev/), and [OpenAI](https://openai.com/). Use the `secrets.example` as a guide to add your keys then move that file (`secrets.toml`) to `.streamlit/secrets.toml`.

- **Install Dependencies**: Execute `pip install -r requirements.txt` in your terminal.
- **Launch the CLI Mode**: Run `python cli_app.py -o "Bangalore, India" -d "Krabi, Thailand" -s 2024-05-01 -e 2024-05-10 -i "2 adults who love swimming, dancing, hiking, shopping, food, water sports adventures, rock climbing"` to start the CLI Mode.
- **Launch the FASTAPI**: Run `uvicorn api_app:app --reload` to start the FASTAPI server.
- **Launch the Streamlit App**: Run `streamlit run streamlit_app.py` to start the Streamlit interface.

★ **Disclaimer**: The application uses GEMINI by default. Ensure you have access to GEMINI's API and be aware of the associated costs.

## Details & Explanation

- **Streamlit UI**: The Streamlit interface is implemented in `streamlit_app.py`, where users can input their trip details.
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
