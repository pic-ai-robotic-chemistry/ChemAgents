import sys
sys.path.append("../") 
import chem_env.environ
from chem_proc.proc import State
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from chem_memory.memory import memory

class Agent():
    def __init__(self, llm, tools_agent, node_name, system_prompt, example_prompt, thread_id, visualize=False):
        self.llm = llm
        self.tools = tools_agent
        self.system_prompt = system_prompt
        self.example_prompt = example_prompt
        self.config = {"configurable": {"thread_id": thread_id}}
        self.graph = None
        self.llm_with_tools = None
        self.node_name = node_name
        self.final_system_prompt = None
        self.set_prompt()
        self.set_llm_with_tools()
        self.set_node_edges(self.node_name)
        if visualize == True:
            self.vis_graph()

    def set_llm_with_tools(self):
        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def chatbot(self, state: State):
        chain = self.final_system_prompt | self.llm_with_tools
        # chain = self.llm_with_tools
        # return {"messages": [chain.invoke(self.final_prompt + state["messages"])]}
        return {"messages": [chain.invoke({"messages":state["messages"]})]}
    
    def set_node_name(self, node_name):
        self.node_name = node_name

    def reset_prompt(self, node_name, refine_prompt):
        self.set_node_name(node_name)
        self.system_prompt = refine_prompt
        self.set_prompt()
        self.set_llm_with_tools()
        print(self.system_prompt)
        # self.llm_with_tools = self.llm
        self.set_node_edges(self.node_name)
        # self.vis_graph()

    def set_back_prompt(self):
        self.set_prompt()
        self.set_llm_with_tools()
        self.set_node_edges(self.node_name)

    def set_prompt(self):

        self.final_system_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", self.system_prompt),
    ] + self.example_prompt + [
        MessagesPlaceholder(variable_name="messages"),
    ]
)
        # self.final_prompt = [SystemMessage(content=self.prompt)]
        
    def set_node_edges(self, node_name):
        graph_builder = StateGraph(State)
        graph_builder.add_node(node_name, self.chatbot)
        tool_node = ToolNode(tools=self.tools)
        graph_builder.add_node("tools", tool_node)

        graph_builder.add_conditional_edges(
            node_name,
            tools_condition,
        )

        graph_builder.add_edge("tools", node_name)
        graph_builder.set_entry_point(node_name)
        self.graph = graph_builder.compile(checkpointer=memory)

    def vis_graph(self):
        png_data = self.graph.get_graph(xray=True).draw_mermaid_png()
        # display(Image(png_data))
        # 我的路径出错，改为绝对路径可以!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        with open("C:/Users/ASUS/Desktop/GPT/chem_langgraph620/chem_langgraph/vis_graph/graph_visualization" + self.node_name + ".png", "wb") as f:
            f.write(png_data)
        print("Graph visualization saved as graph_visualization.png")
