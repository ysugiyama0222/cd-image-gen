from openai import OpenAI
from config import get_api_key

def get_openai_client():
    api_key = get_api_key()
    return OpenAI(api_key=api_key)
