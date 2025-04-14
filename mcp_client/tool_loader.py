from .client import MCPClient
from .types import ToolType, ToolUnion

async def load_tools_from_config(config_path: str, tool_type: ToolType = "google") -> list[ToolUnion]:
    """
    High-level helper to initialize MCP client, load servers from config,
    and return tools (Google ADK or langgraph).

    Args:
        config_path (str): Path to the MCP JSON config.
        tool_type (ToolType): Either 'google' or 'langgraph'.

    Returns:
        List[ToolUnion]: List of tool instances ready for agent injection.
    """
    client = MCPClient(tool_type=tool_type)
    client.load_servers(config_path)
    tools = await client.start()
    return tools