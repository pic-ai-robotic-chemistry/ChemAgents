import json
import os
from langchain_core.messages import HumanMessage, AIMessage

current_dir = os.path.dirname(os.path.abspath(__file__))

with open(current_dir + '/example.json', 'r' , encoding='utf-8') as json_file:
    dialogue_list = json.load(json_file)

example_list = []
for item in dialogue_list:
    if 'HumanMessage' in item:
        example_list.append(HumanMessage(content=item['HumanMessage']['content']))
    elif 'AIMessage' in item:
        example_list.append(AIMessage(content=item['AIMessage']['content']))

