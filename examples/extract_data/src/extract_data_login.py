import os
from airtop import AsyncAirtop, SessionConfigV1
from dotenv import load_dotenv

load_dotenv()

# Setup environment variables
api_key = os.getenv("AIRTOP_API_KEY")
profile_id = os.getenv("profile_id")

if not api_key:
    print("Error: AIRTOP_API_KEY environment variable must be set.")
    exit(1)

TARGET_URL = ""
EXTRACT_DATA_PROMPT = """
This browser is open to a page that lists available job roles for software engineers in San Francisco. Please provide 10 job roles that appear to be posted by the AI-related companies.
Return the result as a json object following this structure:
{
    "companies":[
        {
            "companyName":"",
            "jobTitle":"",
            "location":"",
            "salary":"",
        }
    ],
}
"""

try:
    # Initialize AirTop client
    client = AsyncAirtop(api_key=api_key)

    # Create a session configuration
    if profile_id != "":
        configuration = SessionConfigV1(
            timeout_minutes=10,
            persist_profile=True,
        )
    else:
        configuration = SessionConfigV1(
            timeout_minutes=10,
            persist_profile=True,
            base_profile_id=profile_id,
        )

    # Create a session
    session = await client.sessions.create(configuration=configuration)
    if not session or hasattr(session, "errors") and session.errors:
        raise Exception(f"Failed to create session: {session.errors}")

    session_id = session.data.id if session.data else None
    
    # Create a browser window
    window = await client.windows.create(session_id, url=TARGET_URL)
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
finally:
    print("Terminating Airtop session...")
    await client.sessions.terminate(id=session.data.id)