from crewai import Agent, Crew, Task
from crewai_tools import TXTSearchTool
from extract_data_login import run
import asyncio
import os

os.environ['OPENAI_API_BASE'] = 'http://localhost:11434'
os.environ['OPENAI_MODEL_NAME'] = 'ollama/llama3.2'
os.environ['OPENAI_API_KEY'] = 'NA'

def main():
    result = asyncio.run(run())
    data_analyst = Agent(
        role="HR Analyst",
        goal=f"Based on the context provided, analyse what are the job postings currently available. Where are this postings? What's the salary for them? What are they requiring? Are they compatible? - Context: {str(result)}",
        backstory="You are a HR expert",
        verbose=True,
        allow_delegation=False,
    )

    test_task = Task(
        description="Understand the topic and give the correct response",
        agent=data_analyst,
        expected_output="Give a correct response",
    )

    crew = Crew(agents=[data_analyst], tasks=[test_task])
    output = crew.kickoff()
    print("Result :\n\n",output)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)