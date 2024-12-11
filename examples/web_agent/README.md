# WEBAGENT

This is an agent that uses python to connect to Airtop, create sessions, execute prompts on the site and store the data in a local database.

## PREREQUISITES

- Python 3.10
- poetry==1.8.4
- poetry-core==1.9.1

To install, just run the following command after downloading the code

`poetry install`

These are the steps necessary to run the code:

## CREATE WORKER

The worker.py is the core script of this agent.
It does the following in order:
- It starts a session. It's necessary to supply your own AIRTOP_API_KEY in the .env file;
- It accesses the target site, defined in TARGET_URL in the worker.py script;
- It uses a prompt defined in the worker.py script to extract information from the site and requests login if needed;
- If it's the first time, the db and the worker are created and the result of running the prompt on the site is exhibited;
- If it's not the first time, then a comparison is made. The instruction for the comparison is on the file prompt_templates.py. If a comparison is made, it's inserted on the local db;
- The result of running the prompt on the site is inserted in the db;

## FETCH RESULTS

In the file utils.py there are methods available to do the following operations:

- describe the existing workers;
- delete a worker;
- retrieve the history of comparisons;

## RUNNING THE EXAMPLE

It's possible to schedule a worker to run regularly. For that it's suggested to create a cron job or some other similar program that is able to run worker.py with the desired recurrence.

To run the worker it's necessary run the command

`python worker.py`

## CHECK RESULTS STORED IN THE DB

To get details from the DB on all previous runs, run the following command:

`python utils.py`
