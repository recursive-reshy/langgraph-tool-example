# LangGraph
from langgraph.graph import START, END

def register_topology( graph_builder ):
    graph_builder.add_edge( START, "chatbot" )
    graph_builder.add_edge( "chatbot", END )