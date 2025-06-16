from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

os.getenv("OPENAI_API_KEY")    

class State(TypedDict):
    messages: Annotated[list, add_messages]
    
graph_builder = StateGraph(State)


llm = init_chat_model("openai:gpt-4.1")

#Node Chatbot
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder.add_node("chatbot",chatbot)

graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile()





    