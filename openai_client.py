from openai import OpenAI
from openai.openai_object import OpenAIObject
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OpenAIClient:
    def __init__(self):
        # self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.client = OpenAI(api_key=os.getenv("LOCAL_API_KEY"), base_url=os.getenv("LOCAL_URL"))

    def get_event(self, message: list, response_format: OpenAIObject=None) -> OpenAIObject:
        completion = self.client.Completion.create(
            model=os.getenv("MODEL_NAME"),
            messages=message
        )
        return completion.choices[0].message
