import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.remote_connection import ChromeRemoteConnection
from airtop import Airtop, SessionConfig
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
# Prompts used in the TARGET_URL

def create_airtop_selenium_connection(
    airtop_api_key, airtop_session_data, *args, **kwargs
):
    class AirtopRemoteConnection(ChromeRemoteConnection):
        @classmethod
        def get_remote_connection_headers(cls, *args, **kwargs):
            # Call the original class method with any arguments passed
            headers = super().get_remote_connection_headers(*args, **kwargs)
            # Add the Authorization header with Bearer token
            headers["Authorization"] = f"Bearer {airtop_api_key}"
            return headers
    return AirtopRemoteConnection(
        remote_server_addr=airtop_session_data.chromedriver_url, *args, **kwargs
    )

# Initialize AirTop client
client = Airtop(api_key=api_key)

# Start an Airtop browser session and wait for it to be ready.
print("Starting Airtop session...")
session = client.sessions.create(configuration=SessionConfig(persist_profile=True))
if profile_id != "":
    session = client.sessions.create(configuration=SessionConfig(base_profile_id="YOUR_PROFILE_ID"))
else:
    profile_id = session.data.profileId
print(f"Airtop session ready. Session id: {session.data.id}")
print(f"Profile_id: {profile_id}")

# Connect to the Airtop cloud browser with Selenium and navigate to a page.
print("Starting Selenium...")
browser = webdriver.Remote(
    command_executor=create_airtop_selenium_connection(api_key, session.data),
    options=webdriver.ChromeOptions(),
)
browser.get(TARGET_URL)
time.sleep(2)

window_info = client.windows.get_window_info_for_selenium_driver(
    session.data,
    browser,
)
print(
    f"Please log in to the service before continuing using this link and navigate to the site desired:\n\n {window_info.data.live_view_url}"
)
input("Press any key to continue")

current_content = client.windows.page_query(
    session.data.id,
    window_info.data.window_id,
    prompt=EXTRACT_DATA_PROMPT,
)
current_result = current_content.data.model_response[:]
print(current_result)
browser.quit()
# Terminate the Airtop session.
print("Terminating Airtop session...")
client.sessions.terminate(id=session.data.id)