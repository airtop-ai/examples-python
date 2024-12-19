import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from airtop import PageQueryConfig
from airtop_client import airtop_client
from prompts import validate_url_prompt, validate_url_schema
from state import State


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
        model_response_json: dict = json.loads(model_response.data.model_response)
        return model_response_json.get("is_valid", False)
    else:
        return False
    

def url_validator_node(state: State):
    """Langgraph node that validates a list of URLs.

    Args:
        state (State): the state containing the list of URLs to validate

    Returns:
        State: the state containing the list of validated URLs
    """
    validated_urls = []

    with ThreadPoolExecutor() as executor:
        # Create a dictionary to keep track of future to URL mapping
        future_to_url = {executor.submit(validate_url, url): url for url in state.urls}
        
        for future in as_completed(future_to_url):
            url = future_to_url[future]  # Get the URL associated with this future

            try:
                is_valid = future.result()
                if is_valid:
                    validated_urls.append(url)
                else:
                    print(f"Invalid URL: {url}")
            except Exception as e:
                print(f"Error validating URL {url}: {e}")
                continue

    return State(urls=validated_urls)
    


    



