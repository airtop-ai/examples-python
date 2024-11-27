# WEBAGENT

This is an agent that uses python to connect to Airtop, create sessions, execute prompts on the site and store the data in a local database.

## CREATE LOCAL DATABASE

To create the local database it's necessary to run

`python connect_database.py`

## CREATE WORKER

The worker.py is the core script of this agent.
It does the following in order:
- It starts a session. It's necessary to supply your own API_KEY in the .env file;
- It accesses the target site, defined in TARGET_URL in the .env file;
- It uses a prompt defined in the .env file to extract information from the site
- If it requires login, something defined in the .env file, you will be prompted to realize the log in manually;
- If it's the first time, a worker is created and the result of running the prompt on the site is exhibited;
- If it's not the first time, then a comparison is made. The instruction for the comparison is on the file prompt_templates.py. If a comparison is made, it's inserted on the local db;
- The result of running the prompt on the site is inserted in the db;

## FETCH RESULTS

In the file utils.py there are methods available to do the following operations:

- describe the exhisting workers;
- delete a worker;
- retireve the history of comparisons;

## SCHEDULE WORKER

It's possible to schedule a worker to run regularly. For that it's suggested to create a cron job or some other similar program that is able to wun worker.py with the desired recurrency.