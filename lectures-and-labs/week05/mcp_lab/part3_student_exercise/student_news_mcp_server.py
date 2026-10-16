import json
import sys
import asyncio
from datetime import datetime, timezone
import urllib.request
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Terminal colors for logging
CYAN = '\033[96m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def log_message(msg_type, data):
    """Pretty print messages to stderr - helps with debugging"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"\n{BOLD}{CYAN}[{timestamp}] {msg_type}{RESET}", file=sys.stderr)
    print(f"{YELLOW}{'─'*60}{RESET}", file=sys.stderr)
    print(json.dumps(data, indent=2), file=sys.stderr)
    print(f"{YELLOW}{'─'*60}{RESET}\n", file=sys.stderr)
    sys.stderr.flush()

def fetch_top_stories(count: int = 5) -> list:
    """
    Fetch top story IDs from Hacker News API
    
    Args:
        count: Number of story IDs to return (default 5, max 10)
    
    Returns:
        List of story IDs
    
    API Endpoint: https://hacker-news.firebaseio.com/v0/topstories.json
    
    Hint: This returns a large list of IDs. You need to slice it to get the top N.
    """
    if type(count) is not int or count < 1:
        raise ValueError("count must be a positive integer")
    try:
        with urllib.request.urlopen(
            "https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10
        ) as response:
            story_ids = json.load(response)
    except (OSError, ValueError) as exc:
        raise ValueError(f"Could not fetch top stories: {exc}") from exc
    if not isinstance(story_ids, list):
        raise ValueError("The Hacker News API did not return a list of story IDs")
    return story_ids[:min(count, 10)]


def fetch_story_details(story_id: int) -> dict:
    """
    Fetch detailed information about a specific story
    
    Args:
        story_id: The Hacker News story ID
    
    Returns:
        Dictionary with story details (title, author, score, url, time)
    
    API Endpoint: https://hacker-news.firebaseio.com/v0/item/{story_id}.json
    
    The API returns a JSON object with fields like:
    - title: Story title
    - by: Author username
    - score: Number of upvotes
    - url: Link to the story (might be None for Ask HN posts)
    - time: Unix timestamp
    """
    if type(story_id) is not int or story_id < 1:
        raise ValueError("story_id must be a positive integer")
    try:
        with urllib.request.urlopen(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", timeout=10
        ) as response:
            story = json.load(response)
    except (OSError, ValueError) as exc:
        raise ValueError(f"Could not fetch story {story_id}: {exc}") from exc
    if not story or story.get("deleted") or story.get("dead"):
        raise ValueError(f"Story {story_id} was not found")
    return {
        "title": story.get("title", "Untitled"),
        "author": story.get("by", "Unknown"),
        "score": story.get("score", 0),
        "url": story.get("url") or f"https://news.ycombinator.com/item?id={story_id}",
        "time": (
            datetime.fromtimestamp(story["time"], timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            if story.get("time") is not None else "Unknown"
        ),
    }


# Create the MCP server
app = Server("news-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Define the tools that this server provides.
    
    You need to define two tools:
    1. get_top_stories
    2. get_story_details
    
    Each tool needs:
    - name: The tool's name (string)
    - description: What the tool does (string)
    - inputSchema: JSON Schema defining the parameters
    
    Hint: Look at the examples in Part 1 and Part 2 for reference.
    """
    log_message("📋 LIST TOOLS REQUEST", {"method": "tools/list"})
    
    tools = [
        Tool(
            name="get_top_stories",
            description="Get the top Hacker News story IDs. Use to find current popular stories, then get_story_details for each ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "count": {"type": "integer", "default": 5, "minimum": 1, "maximum": 10},
                },
            },
        ),
        Tool(
            name="get_story_details",
            description="Get a Hacker News story's title, author, score, URL and time. Use with a story ID from get_top_stories.",
            inputSchema={
                "type": "object",
                "properties": {
                    "story_id": {"type": "integer", "minimum": 1},
                },
                "required": ["story_id"],
            },
        ),
    ]
    
    log_message("✅ LIST TOOLS RESPONSE", {
        "tools": [{"name": t.name, "description": t.description} for t in tools]
    })
    
    return tools

@app.call_tool(validate_input=False)
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool execution.
    
    This function is called when a client wants to use one of your tools.
    
    Args:
        name: The name of the tool to execute
        arguments: Dictionary of arguments passed to the tool
    
    Returns:
        List containing a TextContent object with the result
    """
    log_message("🔧 TOOL CALL REQUEST", {
        "tool": name,
        "arguments": arguments
    })
    
    # Validate here so invalid arguments receive an explanatory Error: result.
    try:
        if name == "get_top_stories":
            count = arguments.get("count", 5)
            if type(count) is not int or not 1 <= count <= 10:
                raise ValueError("count must be an integer from 1 to 10")
            story_ids = fetch_top_stories(count)
            text = f"Top {len(story_ids)} Hacker News story IDs:\n" + "\n".join(
                f"{index}. {story_id}" for index, story_id in enumerate(story_ids, 1)
            )
        elif name == "get_story_details":
            story_id = arguments.get("story_id")
            if type(story_id) is not int or story_id < 1:
                raise ValueError("story_id is required and must be a positive integer")
            story = fetch_story_details(story_id)
            text = (
                f"Title: {story['title']}\n"
                f"Author: {story['author']}\n"
                f"Score: {story['score']}\n"
                f"URL: {story['url']}\n"
                f"Time: {story['time']}"
            )
        else:
            raise ValueError(f"Unknown tool: {name}")
    except ValueError as exc:
        text = f"Error: {exc}"

    result = [TextContent(type="text", text=text)]
    log_message("✅ TOOL CALL RESPONSE", {"text": text})
    return result


async def main():
    """Main entry point for the server"""
    print(f"\n{BOLD}{GREEN}🚀 News MCP Server Starting...{RESET}", file=sys.stderr)
    print(f"{CYAN}📰 Using Hacker News API{RESET}\n", file=sys.stderr)
    sys.stderr.flush()
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
