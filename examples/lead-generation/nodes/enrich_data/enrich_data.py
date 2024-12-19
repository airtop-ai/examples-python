from prompts import enrich_therapist_info_prompt, enrich_therapist_info_schema, TherapistInfo
from airtop_client import airtop_client
from airtop import PageQueryConfig
import json

def enrich_therapist_info(therapist: TherapistInfo) -> TherapistInfo:
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
        return TherapistInfo(**model_response_json)
    else:
        return therapist
    