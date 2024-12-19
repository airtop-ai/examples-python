from airtop_client import airtop_client
from airtop import PageQueryConfig
from prompts import extract_therapist_info_prompt, extract_therapist_info_schema
import json

def extract_therapist_info(url: str) -> list[dict]:
    """Uses Airtop's Page Query API to extract therapist information from a webpage.

    Args:
        url (str): the URL to extract therapist information from

    Returns:
        list[dict]: the list of therapist information
    """
    session = airtop_client.create_session()
    url_window = airtop_client.create_window(session_id=session.data.id, url=url)

    model_response = airtop_client.client.windows.page_query(
        session_id=session.data.id,
        window_id=url_window.data.window_id,
        prompt=extract_therapist_info_prompt,
        configuration=PageQueryConfig(
            output_schema=extract_therapist_info_schema
        )
    )


    if isinstance(model_response.data.model_response, str) and len(model_response.data.model_response) > 0:
        model_response_json: dict = json.loads(model_response.data.model_response)
        return model_response_json.get("therapists", [])
    else:
        return []