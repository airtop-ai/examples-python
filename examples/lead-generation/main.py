
from langgraph.graph import END, START, StateGraph
from nodes.csv_generator import generate_csv_node
from nodes.enrich_data import enrich_data_node
from nodes.info_extractor import info_extractor_node
from nodes.outreach_message_generator import generate_outreach_message_node
from nodes.url_list_input import url_list_input_node
from nodes.url_validator import url_validator_node
from state import State

# Build the graph
builder = StateGraph(State)

builder.add_node("url_input", url_list_input_node)
builder.add_node("url_validator", url_validator_node)
builder.add_node("info_extractor", info_extractor_node)
builder.add_node("enrich_data", enrich_data_node)
builder.add_node("generate_outreach_message", generate_outreach_message_node)
builder.add_node("generate_csv", generate_csv_node)


# Connect the nodes
builder.add_edge(START, "url_input")
builder.add_edge("url_input", "url_validator")
builder.add_edge("url_validator", "info_extractor")
builder.add_edge("info_extractor", "enrich_data")
builder.add_edge("enrich_data", "generate_outreach_message")
builder.add_edge("generate_outreach_message", "generate_csv")
builder.add_edge("generate_csv", END)

# Compile the graph
graph = builder.compile()

# Run the graph
graph.invoke(State(urls=[]))


