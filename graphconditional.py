# from https://python.langchain.com/docs/langgraph/

import json
from langchain_core.messages import ToolMessage, BaseMessage, HumanMessage
from langchain_core.tools import tool
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, MessageGraph
from typing import TypedDict, Annotated, List, Union

from visgraph import draw_graph, draw_ascii_graph

@tool
def multiply(first_number: int, second_number: int):
    """Multiplies two numbers together."""
    return first_number * second_number

model = ChatOpenAI(temperature=0,model="gpt-4-turbo") # defaults to gpt-3.5-turbo
model_with_tools = model.bind(tools=[convert_to_openai_tool(multiply)])

graph = MessageGraph()

def invoke_model(state: List[BaseMessage]):
    return model_with_tools.invoke(state)

graph.add_node("oracle", invoke_model)

def invoke_tool(state: List[BaseMessage]):
    tool_calls = state[-1].additional_kwargs.get("tool_calls", [])
    multiply_call = None

    for tool_call in tool_calls:
        if tool_call.get("function").get("name") == "multiply":
            multiply_call = tool_call

    if multiply_call is None:
        raise Exception("No adder input found.")

    res = multiply.invoke(
        json.loads(multiply_call.get("function").get("arguments"))
    )

    return ToolMessage(
        tool_call_id=multiply_call.get("id"),
        content=res
    )

graph.add_node("multiply", invoke_tool)

graph.add_edge("multiply", END)

graph.set_entry_point("oracle")

def router(state: List[BaseMessage]):
    tool_calls = state[-1].additional_kwargs.get("tool_calls", [])
    if len(tool_calls):
        return "multiply"
    else:
        return "end"

graph.add_conditional_edges("oracle", router, {
    "multiply": "multiply",
    "end": END,
})

runnable = graph.compile()

result = runnable.invoke(HumanMessage("What is 123 * 456?"))
print(result)

draw_ascii_graph(runnable.get_graph())
#draw_graph(runnable.get_graph(), "graph2.png")

