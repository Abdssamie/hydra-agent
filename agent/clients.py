from google import genai
from config import GOOGLE_API_KEY
from huggingface_hub import InferenceClient
from config import HF_AUTH_TOKEN

genai_client = genai.Client(api_key=GOOGLE_API_KEY)
hf_client = InferenceClient(
            provider="fal-ai",
            api_key=HF_AUTH_TOKEN
        )
