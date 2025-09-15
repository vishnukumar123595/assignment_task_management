
# app/agent.py
import operator
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from . import tools

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

# Gemini with full toolset
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
all_tools = [
    tools.create_task,
    tools.list_tasks,
    tools.filter_tasks,
    tools.update_task,
    tools.delete_task,
]
llm_with_tools = llm.bind_tools(all_tools)
tool_executor = tools.ToolExecutor(all_tools)

def call_model(state):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def call_tool(state):
    last_message = state["messages"][-1]
    tool_calls = last_message.tool_calls
    tool_outputs = tool_executor.batch(tool_calls)
    return {"messages": tool_outputs}

def should_continue(state):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "continue"
    return "end"

workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("action", call_tool)
workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue, {"continue": "action", "end": END})
workflow.add_edge("action", "agent")

agent_runnable = workflow.compile()
