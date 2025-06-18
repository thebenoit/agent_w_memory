from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]
  
    
llm = ChatOpenAI(model="gpt-4o-mini")   


def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    
    state["messages"].append(AIMessage(content=response.content))
    
    print(f"\nAI: {response.content}")
    print("CURRENT STATE: ", state["messages"])
    
    return state 

graph = StateGraph(AgentState)

graph.add_node("process", process)

graph.add_edge(START, "process")

graph.add_edge("process",END)

agent = graph.compile()

conversation_history = []

user_input = input("Enter a message: ")

while user_input != "exit":
      conversation_history.append(HumanMessage(content=user_input))
      
      result = agent.invoke({"messages": conversation_history})
      
      conversation_history = result["messages"]
      user_input = input("Enter a message: ")
      
with open("logging.txt","w") as file:
     file.write("Your Conversation Log:\n")
     for message in conversation_history:
         if isinstance(message, HumanMessage):
             file.write(f"You: {message.content}\n")
         elif isinstance(message, AIMessage):
             file.write(f"AI: {message.content}\n")
     file.write("END OF CONVERSATION\n")
             
print("Conversation logged to logging.txt")
     
     
     
     
               
         


     
    
