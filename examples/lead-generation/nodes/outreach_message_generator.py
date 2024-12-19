import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from env_config import env_config
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from prompts import Therapist, outreach_message_prompt
from state import State

model = ChatOpenAI(model="gpt-4o-mini", api_key=env_config.OPENAI_API_KEY)

def generate_outreach_message(therapist: Therapist) -> Therapist:
    """
    Generate an outreach message for a therapist.

    Args:
        therapist (Therapist): The therapist to generate an outreach message for.

    Returns:
        Therapist: The therapist with the generated outreach message.
    """
    prompt = outreach_message_prompt(therapist)
    messages = [
        SystemMessage(content="You are an AI assistant that generates outreach messages for therapists."),
        HumanMessage(content=prompt)
    ]
    response = model.invoke(messages)

    # Read the response as JSON
    result = json.loads(response.content)

    # Check if there is a message in the response and add  it to the therapist info
    if "message" in result:
        therapist.outreach_message = result["message"]
   
    return therapist

def generate_outreach_message_node(state: State) -> State:
    """
    Langgraph node that generates outreach messages for a list of therapists.

    Args:
        state (State): The state containing the list of therapists.

    Returns:
        State: The state containing the list of therapists with the generated outreach messages.
    """
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate_outreach_message, therapist) for therapist in state.therapists]
        therapists_with_outreach_message = [future.result() for future in as_completed(futures)]

    return State(therapists=therapists_with_outreach_message)
   