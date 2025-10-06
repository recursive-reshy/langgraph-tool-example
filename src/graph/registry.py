from .nodes.chatbot import chatbot
from .nodes.tools import tool_node

def register_nodes( graph_builder ):
    graph_builder.add_node( "chatbot", chatbot )
    graph_builder.add_node( "tools", tool_node )