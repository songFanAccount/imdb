from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
