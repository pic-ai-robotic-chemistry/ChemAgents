from chem_agent.agent import Agent
from chem_model.llm import llm
import chem_agent.tools as tools
from langchain_core.messages import BaseMessage
from chem_prompt.prompt import RO_SYSTEM_PROMPT,RO_SELFREFLECT_PROMPT, RO_EXPERTRULE_PROMPT,EXAMPLE_PROMPT

tools_agent = [tools.query_experiment_template_library]
agent = Agent(llm, tools_agent, node_name='ED_agent', system_prompt=RO_SYSTEM_PROMPT,example_prompt=EXAMPLE_PROMPT, thread_id = "1", visualize=True)

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Agent finished!")
        break
    for event in agent.graph.stream({"messages": [("user", user_input)]},config=agent.config):
        for value in event.values():
            if isinstance(value["messages"][-1], BaseMessage):
                # if value["messages"][-1].type == "ai" and value["messages"][-1].content != "":
                print("Assistant:", value["messages"][-1].content)
    #print("--------------")

    agent.reset_prompt(node_name="aa",refine_prompt=RO_SELFREFLECT_PROMPT)
    for event in agent.graph.stream({"messages": [("user", value["messages"][-1].content)]},config=agent.config):
        for value in event.values():
            if isinstance(value["messages"][-1], BaseMessage):
                # if value["messages"][-1].type == "ai" and value["messages"][-1].content != "":
                print("Assistant:", value["messages"][-1].content)

    agent.reset_prompt(node_name="bb",refine_prompt=RO_EXPERTRULE_PROMPT)
    for event in agent.graph.stream({"messages": [("user", value["messages"][-1].content)]},config=agent.config):
        for value in event.values():
            if isinstance(value["messages"][-1], BaseMessage):
                # if value["messages"][-1].type == "ai" and value["messages"][-1].content != "":
                print("Assistant:", value["messages"][-1].content)
    agent.set_prompt()