# Overview

This example demonstrates how to use Airtop to automate the summarization of a webpage. By leveraging Airtop’s cloud browser capabilities, we can extract a concise summary from any webpage using a simple API.

# Quick setup

## Prerequisites

- Python 3.10
- pip==0.24
- Poetry==1.8.4

## Setup environment

Clone the repository and navigate to this example directory:

`cd examples/summarize/src`

Install dependencies with poetry

`poetry install`

Initiate the environment

`poetry shell`

Copy the `.env.example` file to .env:

`cp .env.example .env`

An API key is required to use this example. You can get one [here](https://portal.airtop.ai/api-keys). A sign-up is required.

Once you have an API key, set it in the .env file.

## Usage

Change the variable `TARGET_URL` to your desired target in `summarize.py`.

To run the example:

`python summarize.py`
