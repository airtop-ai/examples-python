import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.remote_connection import ChromeRemoteConnection
from airtop import Airtop
from prompt_templates import comparison_prompt
from dotenv import load_dotenv

from utils import (
    find_workers, 
    create_worker, 
    retrieve_previous_result, 
    insert_result,
    insert_comparison,
)

load_dotenv()

# Setup environment variables
api_key = os.getenv("AIRTOP_API_KEY")
if not api_key:
    print("Error: AIRTOP_API_KEY environment variable must be set.")
    exit(1)

requires_login = os.getenv("requires_login")
TARGET_URL = os.getenv("TARGET_URL")
EXTRACT_DATA_PROMPT = os.getenv("EXTRACT_DATA_PROMPT")
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
session = client.sessions.create()
print(f"Airtop session ready. Session id: {session.data.id}")

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

# How to get window_id? The doc from our site is not clear
# window_info = client.windows.get_window_info(session.data.id, window_id)
if requires_login == "True":
    print(
        f"Please log in to the service before continuing using this link:\n\n {window_info.data.live_view_url}"
    )
    input("Press any key to continue")
workers = find_workers(TARGET_URL, EXTRACT_DATA_PROMPT)

# RETRIEVE DATA FROM USER IN THE DB TO THAT TARGET URL
current_content = client.windows.page_query(
    session.data.id,
    window_info.data.window_id,
    prompt=EXTRACT_DATA_PROMPT,
)
current_result = current_content.data.model_response[:]

if not workers:
    create_worker([(TARGET_URL, EXTRACT_DATA_PROMPT)])
    print("This is the result of running the prompt on the page \n\n")
    print(current_result)

old_content = retrieve_previous_result(TARGET_URL, EXTRACT_DATA_PROMPT)
if old_content:
    promptContentResponse = client.windows.page_query(
        session.data.id,
        window_info.data.window_id,
        prompt=comparison_prompt(old_content, current_result),
    )
    insert_comparison(TARGET_URL, EXTRACT_DATA_PROMPT, promptContentResponse.data.model_response)

insert_result(TARGET_URL, EXTRACT_DATA_PROMPT, current_result)

browser.quit()
# Terminate the Airtop session.
print("Terminating Airtop session...")
client.sessions.terminate(id=session.data.id)