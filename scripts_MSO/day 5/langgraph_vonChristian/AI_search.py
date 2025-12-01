from __future__ import annotations
from typing import Annotated, Sequence, TypedDict, Optional
import ast
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
)
from langchain.tools import tool
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
 
 
from dotenv import load_dotenv, find_dotenv
 
from langchain_community.tools import DuckDuckGoSearchRun
 
load_dotenv(find_dotenv())
 
 
 
search = DuckDuckGoSearchRun()
 
@tool
def calculator(query: str) -> str:
    """A simple calculator too, input should be a mathematical expression."""
    return ast.literal_eval(query)
 
 
summarizer_llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.0
)
 

@tool
def summarizer(query: str) -> str:
    """A tool that is good in summarizing an article"""
    prompt = (
        "You are an expert summarization assistant.\n"
        "Summarize the following text in clear, concise language.\n"
        "Avoid unnecessary details, keep only the key points.\n\n"
        f"TEXT TO SUMMARIZE:\n{query}\n"
    )
 
    result = summarizer_llm.invoke(prompt)
    print("===== Summarizer was called =====")
    return result.content
 
 
TOOLS = [search, summarizer]
 
 
# Init LLM
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.0).bind_tools(TOOLS)
 
 
def model_node(state: AgentState) -> AgentState:
    res= llm.invoke(state["messages"])
    return {"messages": res}
 
 
 
def summarizer_condition(msgs):
    last = msgs["messages"][-1]
    if isinstance(last, ToolMessage) and last.name == "summarizer":
        return "end"
    return "model"
 
 
 
 
# -------------------------------
# AGENT STATE
# -------------------------------
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
 
 
# -------------------------------
# GRAPH
# -------------------------------
def construct_graph():
    g = StateGraph(AgentState)
    g.add_node("model", model_node)
    g.add_node("tools", ToolNode(TOOLS))
    g.add_edge(START, "model")
    g.add_conditional_edges("model", tools_condition)
    g.add_conditional_edges("tools", summarizer_condition)
    
    return g.compile()
 
 
graph = construct_graph()
 
 
input = {
    "messages": [
        HumanMessage(content="Please find in the internet an article about llm and give me a summary with your tool and the source."),
    ]
}
for c in graph.stream(input):
    print(c)
    print("--------------------------------------------------")
    
 
 