# Quick Setup

## Setup pipenv

Install pipenv if you haven't already: 
```
pip install pipenv
```

Then, navigate to this example directory:

```
cd examples/simple-interactions/src/
```

Install dependencies:
```
pipenv install
```

Copy the `.env.example` file to `.env`:
```
cp .env.example .env
```

## Usage

An API key is required to use this example. You can get one [here](https://portal.airtop.ai/api-keys) (sign-up required).

Once you have an API key, set it in the `.env` file.

Then to run the recipe:
`pipenv run interaction_recipe`


