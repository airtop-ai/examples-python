import os
from airtop import Airtop, SessionConfigV1
from dotenv import load_dotenv

load_dotenv()

# Setup environment variables
api_key = os.getenv("AIRTOP_API_KEY")
if not api_key:
    print("Error: AIRTOP_API_KEY environment variable must be set.")
    exit(1)

TARGET_URL = "https://en.wikipedia.org/wiki/A.I._Artificial_Intelligence"
EXTRACT_DATA_PROMPT = "Summarize the content of this page in one paragraph."
# Prompts used in the TARGET_URL

client = None
session_id = None
window = None

try:
    # Initialize AirTop client
    client = Airtop(api_key=api_key)

    # Create a session configuration
    configuration = SessionConfigV1(
        timeout_minutes=10,
    )
    # Create a session
    session = client.sessions.create(configuration=configuration)
    if not session or hasattr(session, "errors") and session.errors:
        raise Exception(f"Failed to create session: {session.errors}")

    session_id = session.data.id if session.data else None
    
    # Create a browser window
    window = client.windows.create(session_id, url=TARGET_URL)
    if not window.data:
        raise Exception("Failed to create window")
        
    # Get the window ID
    window_id = window.data.window_id

    current_content = client.windows.page_query(
        session.data.id,
        window_id,
        prompt=EXTRACT_DATA_PROMPT,
    )
    current_result = current_content.data.model_response[:]
    print(current_result)
except Exception as e:
    print(e)
finally:
    # Clean up
    if client is not None and session_id is not None:
        if window is not None and window.data is not None and window.data.window_id is not None:
            client.windows.close(session_id, window.data.window_id)
        client.sessions.terminate(session_id)
