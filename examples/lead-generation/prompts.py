from typing import Optional

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    error: Optional[str] = Field(
        default=None,
        description="The error message if the webpage does not match the criteria"
    )

class ValidUrlSchema(BaseSchema):
    is_valid: bool
  
class Therapist(BaseSchema):
    name: str
    email: Optional[str] = None 
    phone: Optional[str] = None
    source: Optional[str] = None
    website: Optional[str] = None
    summary: Optional[str] = None
    outreach_message: Optional[str] = None

validate_url_prompt = """
You are looking at a webpage.
Your task is to determine if the webpage matches the following criteria:
- The webpage is a valid website
- The webpage contains a list of therapists
- The list of therapists is not empty
- The therapist contain at least one of the following fields:
    - Name
    - Email
    - Phone
    - Website
"""

validate_url_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "is_valid": {
      "type": "boolean",
      "description": "Whether the webpage matches the criteria",
    },
    "error": {
      "type": "string",
      "description": "If you cannot fulfill the request, use this field to report the problem.",
    },
  },
  "required": ["is_valid"]
}

extract_therapist_info_prompt = """
You are looking at a webpage that contains a list of therapists.
Your task is to try to extract the following information from the webpage:
For each therapist, extract the following information:
- Name
- Email
- Phone
- Personal website or detail page about the therapist in the webpage.
- Source of the webpage
Some of the information may not be available in the webpage, in that case just leave it blank.
For example, if the webpage does not contain any email address, you should leave the email field blank.

For the personal website or detail page about the therapist, you should extract the URL of the website.
Only extract the first 5 therapists in the list.


If you cannot find the information, use the error field to report the problem.
If no errors are found, set the error field to an empty string.
"""

extract_therapist_info_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "therapists": {
      "type": "array",
      "description": "The list of therapists",
      "items": {
        "type": "object",
        "properties": {
          "name": {
              "type": "string", 
              "description": "The name of the therapist"
          },
          "email": {
              "type": "string", 
              "description": "The email address of the therapist"
          },
          "phone": {
              "type": "string", 
              "description": "The phone number of the therapist"
          },
          "website": {
            "type": "string", 
            "description": "The personal website or detail page about the therapist"
          },
          "source": {
            "type": "string", 
            "description": "The name of the website that contains the therapist information"
          },
        },
        "required": ["name", "source"],
      },  
    },
    "error": {
      "type": "string",
      "description": "If you cannot fulfill the request, use this field to report the problem.",
    },
  },
  "required": ["therapists"]
}

enrich_therapist_info_prompt = """
You are looking at a webpage that contains info about a specific therapist.
Your task is to enrich the therapist information with the following information:
- Name
- Email
- Phone
- Personal website of the therapist
- Summary of the therapist's information from the webpage
- Source of the webpage
Some of the information may not be available in the webpage, in that case just leave it blank.
For example, if the webpage does not contain any email address, you should leave the email field blank.

For the personal website of the therapist, you should extract the URL of the website.

If you cannot find the information, use the error field to report the problem.
If no errors are found, set the error field to an empty string.
"""

enrich_therapist_info_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object", 
    "properties": {
        "name": {"type": "string", "description": "The name of the therapist"},
        "email": {"type": "string", "description": "The email address of the therapist"},
        "phone": {"type": "string", "description": "The phone number of the therapist"},
        "website": {"type": "string", "description": "The personal website of the therapist"},
        "summary": {"type": "string", "description": "The summary of the therapist's information"},
        "source": {"type": "string", "description": "The name of the website that contains the therapist information"},
        "error": {
            "type": "string", 
            "description": "If you cannot fulfill the request, use this field to report the problem."
        },
    },
    "required": ["name", "email", "phone", "website", "summary"]
}

def outreach_message_prompt(therapist: Therapist) -> str:
    return f"""
Generate a small outreach message for the following therapist:
{therapist.name}

Use the following information to generate the message:
{therapist.summary}

The message should be a small message that is 100 words or less.
The goal of the message is to connect with the therapist to sell them an app that serves as a 
companion for their practice.

Return the message in the following JSON format:
{{
    "message": "The outreach message for the therapist",
    "error": "If you cannot fulfill the request, use this field to report the problem."
}}
"""



