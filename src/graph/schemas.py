# Types
from typing import Annotated
from typing_extensions import TypedDict
# LangGraph
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]