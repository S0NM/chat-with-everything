import json
import os

import requests
from langchain.tools import tool

os.environ["SERPER_API_KEY"] = "799fab83ac762e2f1780d5076ba824087a771b21"

class SearchTools():

    @tool("search_internet")
    def search_internet(query):
        """Useful to search the internet
        about a given topic and return relevant results"""
        print(f"DEBUG:SearchTools:{query}")
        top_result_to_return = 5

        try:
            url = "https://google.serper.dev/search"
            payload = json.dumps({"q": query})
            headers = {
                'X-API-KEY': os.environ['SERPER_API_KEY'],
                'content-type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            # check if there is an organic key
            if 'organic' not in response.json():
                return "Sorry, I couldn't find anything about that, there could be an error with you serper api key."
            else:
                results = response.json()['organic']
                string = []
                for result in results[:top_result_to_return]:
                    try:
                        string.append('\n'.join([
                            f"Title: {result['title']}", f"Link: {result['link']}",
                            f"Snippet: {result['snippet']}", "\n-----------------"
                        ]))
                    except KeyError:
                        next

                return '\n'.join(string)
        except Exception as e:
            return f"SearchTools:Exception:{e}"

