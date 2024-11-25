from chem_agent.agent import Agent
from chem_model.llm import llm
import chem_agent.tools as tools
from langchain_core.messages import BaseMessage
from chem_prompt.prompt import TM_SYSTEM_PROMPT,EXAMPLE_PROMPT

# Define a list of tools to be used by the agent
tools_agent = [tools.LiteratureReader, tools.ExperimentDesigner, tools.RobotOperator, tools.ComputationPerformer]
# Initialize the Agent instance with specified configurations
agent = Agent(llm, tools_agent, node_name='RO_agent', system_prompt=TM_SYSTEM_PROMPT,example_prompt=EXAMPLE_PROMPT, thread_id = "1", visualize=True)

# Define a function TM to process user input using the Task Manager Agent
def TM(message):
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Agent finished!")
    for event in agent.graph.stream({"messages": [("user", user_input)]},config=agent.config):
        for value in event.values():
            if isinstance(value["messages"][-1], BaseMessage):
                # if value["messages"][-1].type == "ai" and value["messages"][-1].content != "":
                print("Assistant:", value["messages"][-1].content)

if __name__ == '__main__':
    user_input = input("User: ")
    TM(user_input)
