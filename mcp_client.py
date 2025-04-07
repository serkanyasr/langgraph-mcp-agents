import logging
import json
import asyncio
import shutil
from contextlib import AsyncExitStack
from typing import List, Dict, Any, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.tools import BaseTool

# Configure logging for error tracking
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")


class MCPClient:
    """
    Manages connections to multiple MCP servers as defined in a JSON configuration file.

    Responsibilities:
    - Load MCP servers from configuration.
    - Start MCP servers and initialize tools.
    - Properly clean up resources after execution.
    """

    def __init__(self) -> None:
        self.servers: List[MCPServer] = []  # List of active MCP servers
        self.config: Dict[str, Any] = {}  # Configuration loaded from JSON file
        self.tools: List[BaseTool] = []  # Collected LangChain tools
        self.exit_stack = AsyncExitStack()  # Manages async resource cleanup

    def load_servers(self, config_path: str) -> None:
        """
        Loads server configurations from a JSON file and initializes MCPServer instances.
        
        Args:
            config_path (str): Path to the configuration file.
        """
        try:
            with open(config_path, "r") as file:
                self.config = json.load(file)

            # Create an MCPServer instance for each server defined in the config
            self.servers = [
                MCPServer(name, config) for name, config in self.config.get("mcpServers", {}).items()
            ]
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.error(f"Failed to load MCP configuration: {e}")
            raise

    async def start(self) -> List[BaseTool]:
        """
        Starts all MCP servers and retrieves the tools for use.

        Returns:
            List[BaseTool]: A list of tools provided by the connected MCP servers.
        """
        self.tools = []  # Reset tools before starting
        for server in self.servers:
            try:
                await server.initialize()
                tools = await server.create_langchain_ai_tools()
                self.tools.extend(tools)
            except Exception as e:
                logging.error(f"Failed to initialize server '{server.name}': {e}")
                await self.cleanup_servers()
                return []

        return self.tools

    async def cleanup_servers(self) -> None:
        """
        Ensures that all MCP servers are properly cleaned up.
        """
        for server in self.servers:
            try:
                await server.cleanup()
            except Exception as e:
                logging.warning(f"Warning during cleanup of server '{server.name}': {e}")

    async def cleanup(self) -> None:
        """
        Cleans up all resources, including servers and async exit stack.
        """
        try:
            await self.cleanup_servers()
            await self.exit_stack.aclose()
        except Exception as e:
            logging.warning(f"Warning during final cleanup: {e}")


class MCPServer:
    """
    Represents an individual MCP server connection and manages tool execution.

    Responsibilities:
    - Initialize and connect to an MCP server.
    - Load and provide tools to LangChain.
    - Handle cleanup operations gracefully.
    """

    def __init__(self, name: str, config: Dict[str, Any]) -> None:
        """
        Initializes the MCP server with configuration settings.

        Args:
            name (str): Unique name of the MCP server.
            config (dict): Configuration settings for the server.
        """
        self.name = name
        self.config = config
        self.session: Optional[ClientSession] = None  # Session to communicate with the server
        self._cleanup_lock = asyncio.Lock()  # Ensures safe cleanup in async context
        self.exit_stack = AsyncExitStack()  # Manages async resources

    async def initialize(self) -> None:
        """
        Starts the MCP server and establishes a session for communication.
        """
        command = shutil.which("npx") if self.config.get("command") == "npx" else self.config.get("command")

        if not command:
            raise ValueError("Invalid command: The command must be a valid string and cannot be None.")

        server_params = StdioServerParameters(
            command=command,
            args=self.config.get("args", []),
            env=self.config.get("env")
        )

        try:
            # Start the server using stdio communication
            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            read, write = stdio_transport

            # Establish client session
            session = await self.exit_stack.enter_async_context(ClientSession(read, write))
            await session.initialize()

            self.session = session
        except Exception as e:
            logging.error(f"Error initializing server '{self.name}': {e}")
            await self.cleanup()
            raise

    async def create_langchain_ai_tools(self) -> List[BaseTool]:
        """
        Loads MCP tools and adapts them for use with LangChain.

        Returns:
            List[BaseTool]: The tools retrieved from the MCP server.
        """
        if not self.session:
            raise RuntimeError(f"Cannot create tools: Server '{self.name}' is not initialized.")

        return await load_mcp_tools(session=self.session)

    async def cleanup(self) -> None:
        """
        Properly closes the session and releases resources.
        """
        async with self._cleanup_lock:
            try:
                await self.exit_stack.aclose()
                self.session = None
            except Exception as e:
                logging.error(f"Error during cleanup of server '{self.name}': {e}")
