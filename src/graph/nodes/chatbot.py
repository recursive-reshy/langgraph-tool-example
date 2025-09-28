# Schemas
from ..schemas import State
# LLM
from ...llm.client import get_llm

def chatbot( state: State ):
    llm = get_llm()
    return { "messages": [ llm.invoke( state["messages"] ) ] }