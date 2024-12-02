Extract data from a webpage requiring login
Overview

This recipe demonstrates how to use Airtop to extract data from a website using a prompt. By leveraging Airtop’s live view capabilities, you can have your users log into any of their accounts inside a browser session to provide your agents access to content that requires authentication. Airtop profiles can be used to persist a user’s login state across sessions and avoid the need to have them log in again.

The instructions below will walk through creating a script that connects to Airtop, provides a live view for a user to log into their Glassdoor account if necessary, and retrieves a list of relevant job postings from the Glassdoor website. Similar logic can be applied to any website that requires authentication.

The full source code is available on GitHub

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

cd 

Install dependencies

Run the following command to install the necessary dependencies, including the Airtop SDK:

`poetry install`

Configure your environment

You will need to provide your Airtop API key in a .env file. First, copy the provided example .env file:

cp .env.example .env

Now edit the .env file to add your Airtop API key (and profile_id if you already have one):

AIRTOP_API_KEY=""
profile_id = ""

Script Walkthrough

The script in extract_data_login.py performs the following steps:

    Initialize the Airtop Client

    First, we initialize the AirtopClient using your provided API key. This client will be used to create browser sessions and interact with the page content.

client = Airtop(api_key=api_key)

Create a Browser Session

Creating a browser session will allow us to connect to and control a cloud-based browser. The API accepts an optional baseProfileId parameter, which can be used to reuse a user’s previously provided credentials. If no baseProfileId is given, the user will be prompted to log in at the provided live view URL (see Step 4).


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

client = Airtop(api_key=api_key)
print("Starting Airtop session...")
session = client.sessions.create(configuration=SessionConfig(persist_profile=True))
if profile_id != "":
    session = client.sessions.create(configuration=SessionConfig(base_profile_id="YOUR_PROFILE_ID"))
else:
    profile_id = session.data.profileId
print(f"Airtop session ready. Session id: {session.data.id}")
print(f"Profile_id: {profile_id}")

Connect to the Browser

The script opens a new page and navigates to the target URL, in this case Glassdoor’s user profile page.

cprint("Starting Selenium...")
browser = webdriver.Remote(
    command_executor=create_airtop_selenium_connection(api_key, session.data),
    options=webdriver.ChromeOptions(),
)
browser.get(TARGET_URL)
time.sleep(2)

Handle Log-in Status

If the user is not logged in, it waits for the user to log in at the provided live view URL. The user is also provided with a profileId that can be used to avoid logging in again on subsequent runs.

If the user is already logged in, they are navigated to the target URL to proceed with data extraction.

window_info = client.windows.get_window_info_for_selenium_driver(
    session.data,
    browser,
)
print(
    f"Please log in to the service before continuing using this link and navigate to the site desired:\n\n {window_info.data.live_view_url}"
)
input("Press any key to continue")

Navigate to the Target URL

After logging in, the script navigates to the target URL, which in this case is a Glassdoor search page for software engineering jobs in San Francisco.

Query the AI to Extract Data

We construct a prompt that asks the AI to extract data about job postings that are related to AI companies. We also define a JSON schema for the output. Note that an optimal prompt will begin by providing context about the webpage and what the model is viewing. It will also include information in the description fields of a provided JSON schema to guide the model’s output.

PROMPT = """
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

Utilizing Airtop’s prompt feature, the script requests data about job postings that are related to AI companies, formatted as per the provided JSON schema. The AI agent can follow pagination links to gather more results on sites with multiple pages or from a feed with infinite scrolling.

// Note that it may take several minutes to receive a response from the AI agent
// as it follows pagination links and gathers data from each page
current_result = current_content.data.model_response[:]
// Print the result to the console or otherwise use it as desired
print(current_result)

Clean Up

Finally, the script closes the browser and terminates the session.

browser.quit()
client.sessions.terminate(id=session.data.id)

Running the Script

To run the script, execute the following command in your terminal:

python extract_data_login.py

Summary

This recipe showcases how Airtop can be used to automate tasks that require authentication and data extraction from dynamic content. By combining Airtop’s live view feature for manual login with automated data extraction via natural language prompts, you can interact with and extract data from complex websites that require user credentials.