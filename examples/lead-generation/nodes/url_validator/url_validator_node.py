from airtop_client import airtop_client
from airtop import PageQueryConfig
from prompts import validate_url_prompt, validate_url_schema
import json

def validate_url(url: str) -> bool:
    """Uses Airtop's Page Query API to validate a URL based on its content.

    Args:
        url (str): the URL to validate

    Returns:
        bool: True if the URL is valid, False otherwise
    """
    session = airtop_client.create_session()
    url_window = airtop_client.create_window(session_id=session.data.id, url=url)

    model_response = airtop_client.client.windows.page_query(
        session_id=session.data.id,
        window_id=url_window.data.window_id,
        prompt=validate_url_prompt,
        configuration=PageQueryConfig(
            output_schema=validate_url_schema
        )
    )

    if isinstance(model_response.data.model_response, str) and len(model_response.data.model_response) > 0:
        model_response_json = json.loads(model_response.data.model_response)
        return model_response_json.get("is_valid", False)
    else:
        return False


    



