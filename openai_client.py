from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_client():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("BASE_URL_OPENAI"))
    return client

