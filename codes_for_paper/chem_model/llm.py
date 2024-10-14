
from langchain_openai import ChatOpenAI
import os 

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.1,
    max_tokens=None,
    timeout=None,
    max_retries=3,
    base_url=os.environ.get("OPENAI_API_BASE"),
)