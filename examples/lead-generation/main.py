from nodes.url_list_input.url_list_input_node import get_url_list_input
from env_config import env_config
from nodes.url_validator.url_validator_node import validate_url
from nodes.info_extractor.info_extractor import extract_therapist_info
from nodes.enrich_data.enrich_data import enrich_therapist_info
from nodes.generate_outreach.outreach_message_generator import generate_outreach_message
from nodes.csv_generator.csv_generator import generate_csv
from prompts import TherapistInfo
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel

class State(BaseModel):
    url: str
    therapist_info: TherapistInfo
    enriched_therapist: TherapistInfo
    therapist_with_outreach_message: TherapistInfo


urls = get_url_list_input()


is_valid_url = validate_url(urls[0])

therapist_info = extract_therapist_info(urls[0])
print("OUTPUT FROM EXTRACTING THERAPIST INFO", therapist_info)

# Lets take the first therapist and work with it
therapist = TherapistInfo(**therapist_info[0])

# Enrich the therapist info
enriched_therapist = enrich_therapist_info(therapist)

# Generate an outreach message for the therapist
therapist_with_outreach_message = generate_outreach_message(enriched_therapist)

# Generate a CSV file with the therapist info
generate_csv([therapist_with_outreach_message])
print("Successfully generated CSV file")

