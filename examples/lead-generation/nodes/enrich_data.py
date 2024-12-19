import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from airtop import PageQueryConfig
from airtop_client import airtop_client
from prompts import (
    Therapist,
    enrich_therapist_info_prompt,
    enrich_therapist_info_schema,
)
from state import State


def enrich_therapist_info(therapist: Therapist) -> Therapist:
    """Enrich the therapist information with additional data.

    Args:
        therapist (Therapist): the therapist information to enrich

    Returns:
        Therapist: the enriched therapist information
    """
    session = airtop_client.create_session()
    url_window = airtop_client.create_window(session_id=session.data.id, url=therapist.website)

    model_response = airtop_client.client.windows.page_query(
        session_id=session.data.id,
        window_id=url_window.data.window_id,
        prompt=enrich_therapist_info_prompt,
        configuration=PageQueryConfig(output_schema=enrich_therapist_info_schema)
    )

    if isinstance(model_response.data.model_response, str) and len(model_response.data.model_response) > 0:
        model_response_json: dict = json.loads(model_response.data.model_response)
        return Therapist(**model_response_json)
    else:
        return therapist
    
def enrich_data_node(state: State) -> State:
    """Langgraph node that enriches the therapist information with additional data.

    Args:
        state (State): the state containing the list of therapists

    Returns:
        State: the state containing the enriched therapists
    """
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(enrich_therapist_info, therapist) for therapist in state.therapists]
        enriched_therapists = [future.result() for future in as_completed(futures)]

    return State(therapists=enriched_therapists)
