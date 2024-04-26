from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import END, MessageGraph
from visgraph import draw_graph, draw_ascii_graph

model = ChatOpenAI(temperature=0,model="gpt-4-turbo")

graph = MessageGraph()

graph.add_node("oracle", model)
graph.add_edge("oracle", END)

graph.set_entry_point("oracle")

runnable = graph.compile()

result = runnable.invoke(HumanMessage("What is 1 + 1?"))
print(result)

draw_ascii_graph(runnable.get_graph())
draw_graph(runnable.get_graph(), "graph1.png")
