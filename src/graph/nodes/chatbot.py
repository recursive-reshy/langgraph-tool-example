# Schemas
from ..schemas import State
# LLM
from ...llm.client import get_llm
# Tools
from ...tools.bright_data import search_serp

def chatbot( state: State ):
    llm = get_llm().bind_tools( [ search_serp ] )
    
    return { "messages": [ llm.invoke( state["messages"] ) ] }