from dotenv import load_dotenv
# Graph
from src.graph.builder import create_graph

load_dotenv()

graph = create_graph()

def stream_graph_updates( user_input: str ):
    for event in graph.stream( { "messages": [ { "role": "user", "content": user_input } ] } ):
        for value in event.values():
            print( "Assistant:", value[ "messages" ][ -1 ].content )

if __name__ == "__main__":
    while True:
        try:
            user_input = input( "User: " )
            if user_input.lower() in [ "exit", "quit" ]:
                print( "Exiting..." )
                break
            stream_graph_updates( user_input )
        except Exception as e:
            print( f"An error occurred: { e }" )
            break