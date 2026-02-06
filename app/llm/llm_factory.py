from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from app.llm.config import (
    LLM_PROVIDER,
    GROQ_API_KEY,
    OPENAI_API_KEY,
    MODEL_NAME,
    TEMPERATURE
)

"""
This function is used to get the LLM
It is used in the llm/llm_factory.py file to get the LLM
"""

def get_llm():
    if LLM_PROVIDER == "groq":
        return ChatGroq(
            api_key=GROQ_API_KEY,
            model=MODEL_NAME,
            temperature=TEMPERATURE
        )

    elif LLM_PROVIDER == "openai":
        return ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model=MODEL_NAME,
            temperature=TEMPERATURE
        )

    else:
        raise ValueError("Unsupported LLM provider")
