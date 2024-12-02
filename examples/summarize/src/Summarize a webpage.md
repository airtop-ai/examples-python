Summarize a webpage
Overview

This recipe demonstrates how to use Airtop to automate the summarization of a webpage. By leveraging Airtop’s cloud browser capabilities, we can extract a concise summary from any webpage using a simple API.

The instructions below will walk through creating a script that connects to Airtop, opens a webpage in a cloud browser session, and retrieves a summary of its content. The full source code is available on GitHub

for your reference.
Prerequisites

To get started, ensure you have:

    Python installed on your system.
    An Airtop API key. You can get one for free

    .

Getting Started

    Clone the repository

    Start by cloning the source code from GitHub

:

git clone 

cd airtop-web_agent

Install dependencies with poetry

Run the following command to install the necessary dependencies, including the Airtop SDK:

`poetry install`

Configure your environment

You will need to provide your Airtop API key in a .env file. First, copy the provided example .env file:

cp .env.example .env

Now edit the .env file to add your Airtop API key:

`AIRTOP_API_KEY=<YOUR_API_KEY>`

Script Walkthrough

The script in main.py performs the following steps:

    Initialize the Airtop Client

    First, we initialize the AirtopClient using your provided API key. This client will be used to create browser sessions and interact with the page content.

`api_key = os.getenv("AIRTOP_API_KEY")`
`client = Airtop(api_key=api_key)`

Choose a target site

`TARGET_URL = ""`

Create a Browser Session

Creating a browser session will allow us to connect to and control a cloud-based browser.

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


Connect to the Browser

The script opens a new page and navigates to the target URL. In this example we use a a Wikipedia page, however you can replace this with the URL of your choice.

print("Starting Airtop session...")
session = client.sessions.create()
print(f"Airtop session ready. Session id: {session.data.id}")

print("Starting Selenium...")
browser = webdriver.Remote(
    command_executor=create_airtop_selenium_connection(api_key, session.data),
    options=webdriver.ChromeOptions(),
)
browser.get(TARGET_URL)
time.sleep(2)

Summarize the Content

Leverage Airtop to summarize the webpage’s content using natural language. We utilize the pageQuery API to specify how the summary should be structured.

Here we instruct Airtop to summarize the content of the page in 1 paragraph, however you can customize this prompt to suit your needs (i.e. asking it to provide bullet points).

current_content = client.windows.page_query(
    session.data.id,
    window_info.data.window_id,
    prompt=EXTRACT_DATA_PROMPT,
)
current_result = current_content.data.model_response[:]
// Print the summary to the console or otherwise use it as desired

`print(current_result)`

Clean Up

Finally, the script closes the window and terminates the session.

browser.quit()

print("Terminating Airtop session...")
client.sessions.terminate(id=session.data.id)


Running the Script

To run the script, execute the following command in your terminal:

python summarize.py

Summary

Airtop makes extracting key information from web pages as simple as writing a few lines of code. By combining the power of cloud browser automation with AI summarization, you can efficiently gather and understand content from any website on the internet.