# Overview

This example demonstrates how to use Airtop to extract data from a website using a prompt. By leveraging Airtop’s live view capabilities, you can have your users log into any of their accounts inside a browser session to provide your agents access to content that requires authentication. Airtop profiles can be used to persist a user’s login state across sessions and avoid the need to have them log in again.

# Quick setup

## Prerequisites

- Python 3.10
- pip==0.24
- Poetry==1.8.4

## Setup environment

Install python 3.10 and pip if you haven't already.

Clone the repository and navigate to this example directory:

`cd examples/extract_data/src`

Install dependencies with poetry

`poetry install`

Initiate the environment

`poetry shell`

Copy the `.env.example` file to .env:

`cp .env.example .env`

An API key is required to use this example. You can get one [here](https://portal.airtop.ai/api-keys). A sign-up is required.

Once you have an API key, set it in the .env file.

## Usage

Change the variable `TARGET_URL` to your desired target in `extract_data_login.py`.

To run the example:

`python extract_data_login.py`
