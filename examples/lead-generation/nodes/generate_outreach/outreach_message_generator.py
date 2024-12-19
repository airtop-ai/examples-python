from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from prompts import outreach_message_prompt, TherapistInfo
import json

model = ChatOpenAI(model="gpt-4o-mini")

def generate_outreach_message(therapist: TherapistInfo) -> TherapistInfo:
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
   
