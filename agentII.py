from typing import TypedDict, List, Union, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langchain_core.messages import ToolMessage
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool 
def add(a: int, b:int):
    """this is an addition function that adds 2 number together"""
    return a + b

@tool
def subtract(a: int, b:int):
    """this is a subtraction function that subtracts 2 number together"""
    return a - b

@tool
def multiply(a: int, b:int):
    """this is a multiplication function that multiplies 2 number together"""
    return a * b

@tool
def divide(a: int, b:int):
    """this is a division function that divides 2 number together"""
    return a / b

tools = [add, subtract, multiply, divide]
model = ChatOpenAI(model="gpt-4o").bind_tools(tools)

def model_call(state:AgentState) -> AgentState:
    system_prompt = SystemMessage(content=
        "You are my AI assistant, please answer my query to the best of your ability"
    )
    response = model.invoke([system_prompt] + state["messages"])
    return {"messages":[response]}

def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls: 
        return "end"
    else:
        return "continue"


graph = StateGraph(AgentState)
graph.add_node("our_agent",model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools",tool_node)

graph.set_entry_point("our_agent")

graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END
        
    },
)

graph.add_edge("tools", "our_agent")

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
            
inputs = {"messages": [("user","Add 14 + 4 then multiply by 20 then subtract 100 Also tell me a joke please")]}
print_stream(app.stream(inputs, stream_mode="values"))            
