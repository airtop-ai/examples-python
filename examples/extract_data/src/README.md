## Overview

This example demonstrates how to use Airtop to extract data from a website using a prompt. By leveraging Airtop’s live view capabilities, you can have your users log into any of their accounts inside a browser session to provide your agents access to content that requires authentication. Airtop profiles can be used to persist a user’s login state across sessions and avoid the need to have them log in again.

# Quick setup

## Prerequisites

- Python 3.10
- Poetry==1.8.4

## Setup environment

Clone the repository and navigate to this example

`cd examples/extract_data/src`

Install dependencies with poetry

`poetry install`

Initiate the environment

`poetry shell`

## Run the example

Input your Airtop key in the .env file.

Change the variable `TARGET_URL` to your desired target in `extract_data_login.py`.

`python extract_data_login.py`
