EXTRACT_TABLE = "Create a table that extracts information about this webpage with the following columns: FEATURE, DESCRIPTION, VALUE. Return a markdown style format string."

SUMMARY = "Summarize the content of this page in bullet points. Create the following sections: Content, Format, Links to other sites."

SENTIMENT = "What is the sentiment described on this site? Does it mention [TARGET]? Is it positive or negative? Create a report with bullet points in markdown style with the following sections: Positive mentions, Neutral mentions, Negative mentions."

NEWS = "What are the main topics in the news today? Summarize them in bullet points, with each topic in its section. Return a markdown style string"

TWEETS = "Consider these social media mentions. Do they mention [TARGET]? Are they positive or negative? Create a report with bullet points in markdown style with the following sections: Positive mentions, Neutral mentions, Negative mentions."

YOUTUBE = "Consider the titles for YouTube videos on this page. What are the main topics that this content creator explores? What are the videos with the most views? Create a markdown style report and return it as a string."

EMPLOYEES = "This site describes the most important people in this company. Create a markdown style format report with each individual as a section. Create bullet points for each individual with a summary of who they are and their experience."

MILESTONES = "This is the site for a company that's being invested in. What are the biggest milestones they discuss? Create a markdown style report in bullet points."

CONTACT = "What is the contact information for the individuals or organizations on this page? Return it as a JSON."

