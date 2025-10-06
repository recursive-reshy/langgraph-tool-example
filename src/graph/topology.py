# LangGraph
from langgraph.graph import START, END

from .schemas import State

def _route_tools( state: State):
    if isinstance( state, list ):
        ai_message = state[ -1 ]
    elif messages := state.get( "messages", [] ):
        ai_message = messages[ -1 ]
    else:
        raise ValueError( f"No messages found in input state to tool_edge: { state }" )
    
    if hasattr( ai_message, "tool_calls" ) and len( ai_message.tool_calls ) > 0:
        return "tools"
    
    return END

def register_topology( graph_builder ):
    graph_builder.add_conditional_edges( 
        "chatbot", 
        _route_tools,
        { "tools": "tools", END: END } 
    )
    graph_builder.add_edge( START, "chatbot" )