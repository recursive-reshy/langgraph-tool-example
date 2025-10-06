import json
# LangChain
from langchain_core.messages import ToolMessage
# Tools
from ...tools.bright_data import search_serp

class BasicToolNode:
    # self is the instance of the class
    def __init__( self, tools: list ):
        # Create a dictionary mapping tool names to tool objects for fast lookup
        # Example: {"search_serp": <search_serp_tool>}
        # { tool.name: tool for tool in tools } -> Dictionary comprehension, a concise way to create a dictionary
        self.tools_by_name = { tool.name: tool for tool in tools }

    """
        Execute the tools requested by the LLM in the most recent message.
        
        This method is called by LangGraph when the graph reaches this node.
        
        Args:
            inputs: Dictionary containing the graph state, including "messages"
            
        Returns:
            Dictionary with "messages" key containing ToolMessage results
            
        Raises:
            ValueError: If no messages are found in the input state
    """
    def __call__( self, inputs: dict ): # __call__ is a special Python method that makes an object behave like a function
        # Use walrus operator (:=) to get messages and check if they exist
        # := assigns AND returns a value in a single expression
        # If messages exist, assign them to 'messages' variable
        if messages := inputs.get( "messages", [] ):
            message = messages[ -1 ]
        else:
            raise ValueError( "No messages in inputs" )

        # List to collect all tool execution results
        outputs = []
        
        # Loop through each tool the LLM wants to call
        # message.tool_calls is a list like:
        # [ { "name": "search_serp", "args": { "query": "Python programming" }, "id": "call_123" } ]
        for tool_call in message.tool_calls:
            # Look up the actual tool function by name
            # Then invoke it with the arguments the LLM provided
            tool_result = self.tools_by_name[ tool_call[ "name" ] ].invoke(
                tool_call[ "args" ]
            )

            # Create a ToolMessage to send the result back to the LLM
            outputs.append(
                ToolMessage(
                    # Convert the tool result to JSON string format
                    content = json.dumps( tool_result ),
                    # Record which tool was called
                    name = tool_call[ "name" ],
                    # Link this result back to the original tool call request
                    tool_call_id = tool_call[ "id" ],
                )
            )

        # Return the tool results wrapped in a dictionary
        # LangGraph will append these messages to the state's message list
        return { "messages": outputs }

tool_node = BasicToolNode( tools = [ search_serp ] )