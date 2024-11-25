from chem_agent.agent import Agent
from chem_model.llm import llm
import chem_agent.tools as tools
from langchain_core.messages import BaseMessage
from chem_prompt.prompt import RO_SYSTEM_PROMPT,RO_EXPERTRULE_PROMPT, RO_PROOFREAD_PROMPT,EXAMPLE_PROMPT

# Define a list of tools to be used by the agent
tools_agent = [tools.query_robotAPI_list]
# Initialize the Agent instance with specified configurations
agent = Agent(llm, tools_agent, node_name='RO_agent', system_prompt=RO_SYSTEM_PROMPT,example_prompt=EXAMPLE_PROMPT, thread_id = "1", visualize=True)

# Define a function RO to process user input using the Robot Operator Agent
def RO(message):

    if user_input.lower() in ["quit", "exit", "q"]:
        print("Agent finished!")
        
    for event in agent.graph.stream({"messages": [("user", user_input)]},config=agent.config):
        for value in event.values():
            if isinstance(value["messages"][-1], BaseMessage):
                # if value["messages"][-1].type == "ai" and value["messages"][-1].content != "":
                print("Assistant:", value["messages"][-1].content)
    #print("--------------")

    agent.reset_prompt(node_name="aa",refine_prompt=RO_EXPERTRULE_PROMPT)
    for event in agent.graph.stream({"messages": [("user", value["messages"][-1].content)]},config=agent.config):
        for value in event.values():
            if isinstance(value["messages"][-1], BaseMessage):
                # if value["messages"][-1].type == "ai" and value["messages"][-1].content != "":
                print("Assistant:", value["messages"][-1].content)

    agent.reset_prompt(node_name="aa",refine_prompt=RO_PROOFREAD_PROMPT)
    for event in agent.graph.stream({"messages": [("user", value["messages"][-1].content)]},config=agent.config):
        for value in event.values():
            if isinstance(value["messages"][-1], BaseMessage):
                # if value["messages"][-1].type == "ai" and value["messages"][-1].content != "":
                print("Assistant:", value["messages"][-1].content)

    # At this point, `value["messages"][-1].content` is the proofread robot code, which is sent to the robot's backend control system to control the robot and workstation for automatic experimentation.
    # It need to be replaced with corresponding resources.
    ExecuteRobotCode(value["messages"][-1].content)
    ExperimentalData = GetExperimentalDataPath()

    agent.set_prompt()

if __name__ == '__main__':
    user_input = input("User: ")
    RO(user_input)