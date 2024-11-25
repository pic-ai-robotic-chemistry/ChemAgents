from chem_agent.agent import Agent
from chem_model.llm import llm
import chem_agent.tools as tools
from langchain_core.messages import BaseMessage
from chem_prompt.prompt import CP_SYSTEM_PROMPT,EXAMPLE_PROMPT

# Define a list of tools to be used by the agent
tools_agent = [tools.query_pretrained_model_library, tools.fuse_the_model, tools.Bayesian_optimizer]
# Initialize the Agent instance with specified configurations
agent = Agent(llm, tools_agent, node_name='CP_agent', system_prompt=CP_SYSTEM_PROMPT,example_prompt=EXAMPLE_PROMPT, thread_id = "1", visualize=True)

# Define a function CP to process user input using the Computation Performer Agent
def CP(message):

    if user_input.lower() in ["quit", "exit", "q"]:
        print("Agent finished!")
        
    for event in agent.graph.stream({"messages": [("user", user_input)]},config=agent.config):
        for value in event.values():
            if isinstance(value["messages"][-1], BaseMessage):
                # if value["messages"][-1].type == "ai" and value["messages"][-1].content != "":
                print("Assistant:", value["messages"][-1].content)

    # At this point, `value["messages"][-1].content` is the code program for predicting new data, which is sent to the Computing Platform.
    # It need to be replaced with corresponding resources.
    NewParameter = ExecutePredictionCode(value["messages"][-1].content)
    

if __name__ == '__main__':
    user_input = input("User: ")
    CP(user_input)