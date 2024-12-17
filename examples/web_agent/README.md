# Overview

This is an agent that uses python to connect to Airtop, create sessions, execute prompts on the site and store the data in a local database.

# Quick setup

## Prerequisites

- Python 3.10
- pip==0.24
- Poetry==1.8.4
- poetry-core==1.9.1

## Setup environment

Clone the repository and navigate to this example directory:

`cd examples/web_agent`

Install dependencies with poetry

`poetry install`

Initiate the environment

`poetry shell`

Copy the `.env.example` file to .env:

`cp .env.example .env`

An API key is required to use this example. You can get one [here](https://portal.airtop.ai/api-keys). A sign-up is required.

Once you have an API key, set it in the .env file.


## Usage

The `worker.py` is the core script of this agent.
It does the following in order:
- It accesses the target site, defined in TARGET_URL in the `worker.py` script;
- It uses a prompt defined in the `worker.py` script to extract information from the site and requests login if needed;
- If it's the first time, the db and the worker are created and the result of running the prompt on the site is exhibited;
- If it's not the first time, then a comparison is made. The instruction for the comparison is on the file `prompt_templates.py`. If a comparison is made, it's inserted on the local db;
- The result of running the prompt on the site is inserted in the db;

To run the example:

`python worker.py`

## Analyze results

In the file `utils.py` there are methods available to do the following operations:

- describe the existing workers;
- delete a worker;
- retrieve the history of comparisons;

To get details from the DB on all previous runs, run the following command:

`python utils.py`

## Schedule worker

It's possible to schedule a worker to run regularly. For that it's suggested to create a cron job or some other similar program that is able to run `worker.py` with the desired recurrence.

See details in `How to schedule worker.md`