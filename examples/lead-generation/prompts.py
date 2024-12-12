from pydantic import BaseModel, Field
from typing import Optional

class BaseSchema(BaseModel):
    error: Optional[str] = Field(
        default=None,
        description="The error message if the webpage does not match the criteria"
    )

class ValidUrlSchema(BaseSchema):
    is_valid: bool

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
      "description": f"Whether the webpage matches the criteria",
    },
    "error": {
      "type": "string",
        "description": "If you cannot fulfill the request, use this field to report the problem.",
    },
  },
  "required": ["is_valid"]
}


