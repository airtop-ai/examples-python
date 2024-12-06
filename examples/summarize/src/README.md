## Overview

This example demonstrates how to use Airtop to automate the summarization of a webpage. By leveraging Airtop’s cloud browser capabilities, we can extract a concise summary from any webpage using a simple API.

# Quick setup

## Prerequisites

- Python 3.10
- Poetry==1.8.4

## Setup environment

Clone the repository and navigate to this example

`cd examples/summarize/src`

Install dependencies with poetry

`poetry install`

Initiate the environment

`poetry shell`

## Run the example

Input your Airtop key in the .env file.

Change the variable `TARGET_URL` to your desired target in summarize.py.

`python summarize.py`
