import json
import logging
import asyncio
import shutil
from typing import List, Dict, Any, Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from .types import ToolType, ToolUnion
from google.adk.tools.mcp_tool.mcp_tool import MCPTool


class MCPServer:
    """
    Represents a single MCP server instance.
    Responsible for:
    - Starting a subprocess with given command
    - Establishing session via stdio
    - Loading tools (langgraph or Google ADK)
    """

    def __init__(self, name: str, config: Dict[str, Any], tool_type: ToolType = "google") -> None:
        self.name = name
        self.config = config
        self.tool_type = tool_type
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self._cleanup_lock = asyncio.Lock()

    async def initialize(self) -> None:
        """
        Launches the MCP tool process and sets up a session over stdio.
        """
        command = shutil.which("npx") if self.config.get("command") == "npx" else self.config.get("command")

        if not command:
            raise ValueError("Invalid command: must not be None.")

        server_params = StdioServerParameters(
            command=command,
            args=self.config.get("args", []),
            env=self.config.get("env")
        )

        try:
            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            read, write = stdio_transport
            session = await self.exit_stack.enter_async_context(ClientSession(read, write))
            await session.initialize()
            self.session = session
        except Exception as e:
            logging.error(f"Error initializing server '{self.name}': {e}")
            await self.cleanup()
            raise

    async def create_tools(self) -> List[ToolUnion]:
        """
        Loads tools from the MCP session depending on the tool type.

        Returns:
            List[ToolUnion]: List of usable tools.
        """
        if not self.session:
            raise RuntimeError(f"Cannot create tools: Server '{self.name}' is not initialized.")

        if self.tool_type == "langgraph":
            return await load_mcp_tools(session=self.session)

        tools_response = await self.session.list_tools()
        return [MCPTool(mcp_tool=tool, mcp_session=self.session) for tool in tools_response.tools]

    async def cleanup(self) -> None:
        """
        Clean up the session and close the subprocess.
        """
        async with self._cleanup_lock:
            try:
                await self.exit_stack.aclose()
                self.session = None
            except Exception as e:
                logging.error(f"Error during cleanup of server '{self.name}': {e}")


class MCPClient:
    """
    Manages multiple MCP server instances.
    Loads configuration, starts servers, and collects tools.
    """

    def __init__(self, tool_type: ToolType = "google") -> None:
        self.servers: List[MCPServer] = []
        self.config: Dict[str, Any] = {}
        self.tools: List[ToolUnion] = []
        self.exit_stack = AsyncExitStack()
        self.tool_type = tool_type

    def load_servers(self, config_path: str) -> None:
        """
        Parses the config JSON file and prepares server objects.

        Args:
            config_path (str): Path to mcp_config.json
        """
        try:
            with open(config_path, "r") as file:
                self.config = json.load(file)

            self.servers = [
                MCPServer(name, cfg, tool_type=self.tool_type)
                for name, cfg in self.config.get("mcpServers", {}).items()
            ]
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.error(f"Failed to load MCP configuration: {e}")
            raise

    async def start(self) -> List[ToolUnion]:
        """
        Starts all configured servers and collects tools.

        Returns:
            List[ToolUnion]: List of tools from all servers.
        """
        self.tools = []
        for server in self.servers:
            try:
                await server.initialize()
                tools = await server.create_tools()
                self.tools.extend(tools)
            except Exception as e:
                logging.error(f"Failed to initialize server '{server.name}': {e}")
                await self.cleanup_servers()
                return []
        return self.tools

    async def cleanup_servers(self) -> None:
        """
        Gracefully shuts down all running MCP servers.
        """
        for server in self.servers:
            try:
                await server.cleanup()
            except Exception as e:
                logging.warning(f"Warning during cleanup of server '{server.name}': {e}")

    async def cleanup(self) -> None:
        """
        Performs global cleanup including exit stack closure.
        """
        try:
            await self.cleanup_servers()
            await self.exit_stack.aclose()
        except Exception as e:
            logging.warning(f"Warning during final cleanup: {e}")