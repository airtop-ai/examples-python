import csv

from state import State


def generate_csv_node(state: State) -> None:
    """Langgraph node that generates a CSV file from a list of therapists."""
    # Create a CSV file
    with open("therapists.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Phone", "Email", "Website", "Source", "Outreach Message"])
        for therapist in state.therapists:
            writer.writerow([
                therapist.name,
                therapist.phone,
                therapist.email,
                therapist.website,
                therapist.source,
                therapist.outreach_message
            ])
  