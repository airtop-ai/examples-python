import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from airtop import PageQueryConfig
from airtop_client import airtop_client
from prompts import Therapist, extract_therapist_info_prompt, extract_therapist_info_schema
from state import State


def extract_therapist_info(url: str) -> list[Therapist]:
    """Uses Airtop's Page Query API to extract therapist information from a webpage.

    Args:
        url (str): the URL to extract therapist information from

    Returns:
        list[Therapist]: the list of therapist information
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
        return [Therapist(**therapist) for therapist in model_response_json.get("therapists", [])]
    else:
        return []


def info_extractor_node(state: State):
    """Langgraph node that extracts therapist information from a list of URLs in parallel.

    Args:
        state (State): the state containing the list of URLs

    Returns:
        State: the state containing the list of therapists
    """
    therapists = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(extract_therapist_info, url): url 
                        for url in state.urls}
        
        for future in as_completed(future_to_url):
            try:
                therapist_info = future.result()
                therapists.extend(therapist_info)
            except Exception as e:
                print(f"Error processing URL {future_to_url[future]}: {str(e)}")

    return State(therapists=therapists)
