from .nodes.chatbot import chatbot

def register_nodes( graph_builder ):
    graph_builder.add_node( "chatbot", chatbot )