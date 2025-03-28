import os
import json
import asyncio
from airtop import Airtop, SessionConfigV1, PageQueryConfig
from dotenv import load_dotenv

load_dotenv()

AIRTOP_API_KEY = os.getenv("AIRTOP_API_KEY")
LOGIN_URL = "https://www.glassdoor.com/member/profile"
IS_LOGGED_IN_PROMPT = "This browser is open to a page that either display's a user's Glassdoor profile or prompts the user to login.  Please give me a JSON response matching the schema below."
IS_LOGGED_IN_OUTPUT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "isLoggedIn": {
            "type": "boolean",
            "description": "Use this field to indicate whether the user is logged in.",
        },
        "error": {
            "type": "string",
            "description": "If you cannot fulfill the request, use this field to report the problem.",
        },
    },
}
TARGET_URL = "https://www.glassdoor.com/Job/san-francisco-ca-software-engineer-jobs-SRCH_IL.0,16_IC1147401_KO17,34.htm"
EXTRACT_DATA_PROMPT = "This browser is open to a page that lists available job roles for software engineers in San Francisco. Please provide 10 job roles that appear to be posted by the AI-related companies."
EXTRACT_DATA_OUTPUT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "companies": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "companyName": {"type": "string"},
                    "jobTitle": {"type": "string"},
                    "location": {"type": "string"},
                    "salary": {
                        "type": "object",
                        "properties": {
                            "min": {"type": "number", "minimum": 0},
                            "max": {"type": "number", "minimum": 0},
                        },
                        "required": ["min", "max"],
                    },
                },
                "required": ["companyName", "jobTitle", "location", "salary"],
            },
        },
        "error": {
            "type": "string",
            "description": "If you cannot fulfill the request, use this field to report the problem.",
        },
    },
}


async def run():
    client = None
    session_id = None
    window = None

    try:
        if not AIRTOP_API_KEY:
            raise ValueError("AIRTOP_API_KEY is not set")

        client = Airtop(api_key=AIRTOP_API_KEY)

        profile_name = input(
            "Enter a profile name.  If no profile exists with this name, one will be created: "
        ).strip()
        if profile_name:
            print(f'Profile "{profile_name}" will be used for this session')
        else:
            print("Proceeding without a profile")
            profile_name = None

        print("Creating session...")
        configuration = SessionConfigV1(timeout_minutes=10, profile_name=profile_name)
        session = client.sessions.create(configuration=configuration)

        if profile_name:
            client.sessions.save_profile_on_termination(session.data.id, profile_name)

        if not session.data.cdp_ws_url:
            raise ValueError("Unable to get cdp url")

        session_id = session.data.id if session.data else None
        print("Created airtop session", session_id)

        # Create a new window and navigate to the URL
        window = client.windows.create(session_id, url=LOGIN_URL)
        window_info = client.windows.get_window_info(session_id, window.data.window_id)

        # Check whether the user is logged in
        print("Determining whether the user is logged in...")
        logged_in_schema = IS_LOGGED_IN_OUTPUT_SCHEMA
        is_logged_in_response = client.windows.page_query(
            session_id,
            window.data.window_id,
            prompt=IS_LOGGED_IN_PROMPT,
            configuration=PageQueryConfig(output_schema=logged_in_schema),
        )

        parsed_response = json.loads(is_logged_in_response.data.model_response)
        if "error" in parsed_response:
            raise ValueError(parsed_response.error)
        is_user_logged_in = parsed_response["isLoggedIn"]

        # Prompt the user to log in if not already logged in
        if not is_user_logged_in:
            print(
                f"Log into your Glassdoor account on the live view of your browser window.  Press `Enter` once you have logged in.\nLive view URL: {window_info.data.live_view_url}"
            )
            input()
            if profile_name:
                print(
                    f"Your login credentials will be saved to profile '{profile_name}' for future executions"
                )
        else:
            print(
                f"User is already logged in.\nLive view URL: {window_info.data.live_view_url}"
            )

        # Navigate to the target URL
        print("Navigating to target URL...")
        client.windows.load_url(session_id, window.data.window_id, url=TARGET_URL)
        print("Prompting the AI agent, waiting for a response...")

        extract_data_response = client.windows.page_query(
            session_id,
            window.data.window_id,
            prompt=EXTRACT_DATA_PROMPT,
            configuration=PageQueryConfig(output_schema=EXTRACT_DATA_OUTPUT_SCHEMA),
        )
        formatted_json = json.dumps(
            json.loads(extract_data_response.data.model_response), indent=2
        )
        print("Response:\n\n", formatted_json)

    except Exception as e:
        try:
            print(e.status_code, e.message, e.body)
        except:
            print(e)

    finally:
        # Clean up
        if client is not None and session_id is not None:
            if (
                window is not None
                and window.data is not None
                and window.data.window_id is not None
            ):
                client.windows.close(session_id, window.data.window_id)
            client.sessions.terminate(session_id)
            print("Session terminated")


if __name__ == "__main__":
    asyncio.run(run())
