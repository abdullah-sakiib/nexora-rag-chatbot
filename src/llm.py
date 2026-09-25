from langchain_groq import ChatGroq
from config import GROQ_API_KEY


def get_llm():
    return ChatGroq(
        model="openai/gpt-oss-120b",
        groq_api_key=GROQ_API_KEY,
        temperature=0.2,
        max_tokens=3000
    )