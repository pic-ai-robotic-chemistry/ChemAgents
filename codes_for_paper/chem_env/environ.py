import os
import getpass
def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")        

os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_PROJECT"] = "LangGraph_Agent"

#
# Please configure the relevant information of the API for the LLM to be used here
#
# For example：(Need to fill in your configuration)
#

"""
ChatGPT
"""
os.environ["OPENAI_API_KEY"] = " "
os.environ["OPENAI_API_BASE"] = " "

"""
llama-3.1-70B
"""
os.environ["llama3_1_model"] = " "
os.environ["llama3_1_URL"] = " "
os.environ["llama3_1_API_KEY"] = " "

# os.environ["LANGSMITH_API_KEY"] = ""
# os.environ["TAVILY_API_KEY"] = ""