# Overview

This example demonstrates how to use Airtop and CrewAI to extract data from a website using a prompt and analyse it using a crew. By leveraging Airtop’s live view capabilities, you can have your users log into any of their accounts inside a browser session to provide your agents access to content that requires authentication. Airtop profiles can be used to persist a user’s login state across sessions and avoid the need to have them log in again.
This example showcases how to use Ollama with CrewAI. If you prefer to use chatgpt, just change the variables in `main.py` lines 9:11.

# Quick setup

## Prerequisites

- Ollama
- Python 3.10
- pip==0.24
- Poetry==1.8.4

## Setup environment

Install python 3.10 and pip if you haven't already.

To download Ollama, follow instructions [here](https://ollama.com/download).

The best current version to run in a standard pc is Llama 3.2. Pull the model like described [here](https://ollama.com/blog/llama3.2).

Clone the repository and navigate to this example directory:

`cd examples/crewAI/simple_extraction`

Install dependencies with poetry

`poetry install`

Install crewai with pip

`pip install crewai`

Initiate the environment

`poetry shell`

Copy the `.env.example` file to .env:

`cp .env.example .env`

An API key is required to use this example. You can get one [here](https://portal.airtop.ai/api-keys). A sign-up is required.

Once you have an API key, set it in the .env file.

## Usage

Change the variable `TARGET_URL` to your desired target in `extract_data_login.py`.

To run the example:

`python main.py`
