from prompts import TherapistInfo
import csv
def generate_csv(therapists: list[TherapistInfo]) -> None:
    """Generates a CSV file from a list of therapists."""
    # Create a CSV file
    with open("therapists.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Phone", "Email", "Website", "Outreach Message"])
        for therapist in therapists:
            writer.writerow([therapist.name, therapist.phone, therapist.email, therapist.website, therapist.outreach_message])
    
    return None
  
