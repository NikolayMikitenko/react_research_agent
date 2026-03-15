tools = [
    {
        "type": "function",
        "function": {
            "name":"web_search",
            "description":"Search in the web and return compact results with title, url, and snippet.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for web search"
                    }
                }, 
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name":"read_url",
            "description":"Fetch a URL and extract the page content. Returns a compact, truncated text payload or a readable error.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL for web page which will be called.",
                        "format": "uri"
                    }
                }, 
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name":"write_report",
            "description":"Write the final Markdown report to the output directory and return the absolute path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name of file where Markdown report will be saved."
                    },
                    "content": {
                        "type": "string",
                        "description": "Markdown report which will be saved."
                    }
                }, 
                "required": ["filename", "content"]
            }
        }
    }
]