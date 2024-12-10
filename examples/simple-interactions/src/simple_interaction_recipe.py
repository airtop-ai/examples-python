import os
from airtop import Airtop, PageQueryConfig
import time

ANIMATION_DELAY = 3

STOCK_PERFORMANCE_PROMPT = "This page shows the stock performance for Nvidia. What is the price performance of NVDA over the past 6 months?"

STOCK_PERFORMANCE_OUTPUT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "analysis": {
            "type": "string",
            "description": f"A one sentence analysis of the price performance of NVDA over the past 6 months.",
        },
        "percentChange": {
            "type": "number",
            "description": f"The percentage change in the price of NVDA over the past 6 months.",
        },
        "error": {
            "type": "string",
            "description": "If you cannot fulfill the request, use this field to report the problem.",
        },
    },
}

# Setup environment variables
api_key = os.getenv("AIRTOP_API_KEY")
if not api_key:
    print("Error: AIRTOP_API_KEY environment variable must be set.")
    exit(1)

# Initialize AirTop client
client = Airtop(api_key=api_key)

# Start an Airtop session and wait for it to be ready.
print("Starting Airtop session...")
session = client.sessions.create()
print(f"Airtop session ready. Session id: {session.data.id}")

try:
    # Create and setup window
    print("Creating window")
    window = client.windows.create(session.data.id, url="https://google.com/finance/")
    window_id = window.data.window_id
    if not window_id:
        raise Exception("Window ID not found")

    window_info = client.windows.get_window_info(session.data.id, window_id)
    print(f"Live view url: {window_info.data.live_view_url}")

    time.sleep(ANIMATION_DELAY)  # Animation delay

    # Type NVDA in search box
    print("Searching for Nvidia")
    client.windows.type(
        session_id=session.data.id,
        window_id=window_id,
        element_description="The search box",
        text="NVDA",
        press_enter_key=True,
    )

    time.sleep(ANIMATION_DELAY)  # Animation delay

    # Click 6M button
    print("Clicking on the 6M chart")
    client.windows.click(
        session_id=session.data.id,
        window_id=window_id,
        element_description="The '6M' button at the top of the chart",
    )

    time.sleep(ANIMATION_DELAY)  # Animation delay

    # Query the page about NVDA performance
    print("Querying the page for the price performance of NVDA")
    result = client.windows.page_query(
        session_id=session.data.id,
        window_id=window_id,
        prompt=STOCK_PERFORMANCE_PROMPT,
        configuration=PageQueryConfig(output_schema=STOCK_PERFORMANCE_OUTPUT_SCHEMA),
    )
    print(result.data.model_response)

finally:
    # Terminate the Airtop session.
    print("Terminating Airtop session...")
    client.sessions.terminate(id=session.data.id)
