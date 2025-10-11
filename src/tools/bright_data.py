import requests
from urllib.parse import quote_plus
import os
# Langchain
from langchain_core.tools import tool

BASE_URL = "https://www.google.com/search"
BRIGHT_DATA_URL = "https://api.brightdata.com/request"

def _make_api_request( url: str, **kwargs ):
    headers = {
        "Authorization": f"Bearer { os.getenv( 'BRIGHTDATA_API_KEY' ) }",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post( url, headers = headers, **kwargs )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print( f"Error making API request: {e}" )
        return None
    except Exception as e:
        print( f"Unexpected error: {e}" )
        return None

# Decorator needs a docstring so that the LLM knows what the tool does
@tool
def search_serp( query: str ) -> str:
    """Search the web using SERP API via Bright Data.
    
    This tool searches the internet and returns relevant results including
    knowledge panels and organic search results for the given query.
    
    Args:
        query: The search query string to look up on the web
    
    Returns:
        A dictionary containing knowledge panel data and organic search results,
        or None if the search fails
    """
    try:
        print( f"Searching for query: { query }" )
        payload = {
            "zone": "langgraph_advance_example",
            # quote_plus function is used to encode the query string so that it can be used in the URL
            # brd_json=1 is used to get the response in JSON format from Bright Data
            "url": f"{ BASE_URL }?q={ quote_plus( query ) }&brd_json=1",
            "format": "raw",
        }

        full_response = _make_api_request( BRIGHT_DATA_URL, json = payload )

        if not full_response:
            print( "No response from Bright Data" )
            return None

        extracted_data = {
            "knowledge": full_response.get( "knowledge", {} ),
            "organic": full_response.get( "organic", [] ),
        }

        return extracted_data
        
    except Exception as e:
        print( f"Unexpected error: {e}" )
        return None