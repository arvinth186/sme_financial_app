import os
from dotenv import load_dotenv

load_dotenv()

"""
This function is used to load the environment variables
It is used in the llm/config.py file to load the environment variables
"""

LLM_PROVIDER = os.getenv("LLM_PROVIDER")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MODEL_NAME = os.getenv("MODEL_NAME")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
