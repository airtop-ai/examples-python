# Lead Generation Recipe

A Python application that automates lead generation for therapists using LangChain and Airtop. The app extracts therapist information from websites, enriches the data, generates personalized outreach messages, and creates a CSV output with the therapist info and outreach messages.

## Prerequisites

- Python 3.12.4
- pipenv

## Installation

1. Install pipenv if you haven't already:

```bash
pip install pipenv
```

2. Install the dependencies:

```bash
pipenv install
```

3. Configure a .env file following the .env.example file.

## Running the app

```bash
pipenv run lead_generation_recipe
```

The application will:

1. Prompt you to enter URLs containing therapist information
2. Validate each URL
3. Extract therapist information
4. Enrich the data with additional details
5. Generate personalized outreach messages
6. Create a CSV file with the results

The output will be saved as `therapists.csv` in the current directory.

## Output Format

The generated CSV file will contain the following columns:

- Name
- Phone
- Email
- Website
- Source
- Outreach Message
