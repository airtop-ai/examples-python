# Read env variables
import os
from dotenv import load_dotenv

load_dotenv()

test = os.getenv("LANGCHAIN_API_KEY")
print("LALA")
print(test)
