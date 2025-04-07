import os
import asyncio
import pathlib
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent
import mcp_client

# Get the directory where the script is located
SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
CONFIG_FILE = SCRIPT_DIR / "mcp_config.json"

# Load environment variables from .env file
load_dotenv()

def get_model():
    """
    Retrieves the language model specified in the environment variables.
    If no model is specified, it defaults to 'gpt-4o-mini'.
    Also ensures that the OpenAI API key is set.
    
    Returns:
        ChatOpenAI: An instance of the ChatOpenAI model with streaming enabled.
    """
    llm = os.getenv('MODEL_CHOICE', 'gpt-4o-mini')  # Get model choice from env variables
    os.environ["OPENAI_API_KEY"] = os.getenv('LLM_API_KEY', 'no-api-key-provided')  # Set API key
    
    return ChatOpenAI(
        model=llm,
        streaming=True,  # Enable real-time streaming of responses
        temperature=0,  # Ensure deterministic responses
    )

async def get_langgraph_ai_agent():
    """
    Initializes the MCP client and starts the AI agent by loading necessary tools.
    
    The function first loads server configurations from the config file and then
    initializes the AI agent using the selected model and the available tools.
    
    Returns:
        tuple: (MCPClient instance, AI agent instance)
    """
    client = mcp_client.MCPClient()
    client.load_servers(str(CONFIG_FILE))  # Load server configurations from the JSON file
    tools = await client.start()  # Start MCP client and retrieve available tools
    print("{} tools installed with {} servers".format(len(tools), len(client.servers)))
    agent = create_react_agent(
        model=get_model(),  # Load AI model
        tools=tools,  # Pass available tools to the agent
    )
    
    return client, agent

async def chat_loop(mcp_client, mcp_agent):
    """
    Main chat loop that continuously accepts user input and generates AI responses.
    
    This function keeps running until the user decides to exit. It handles user input,
    sends it to the AI model, and displays real-time responses using Rich's Markdown support.
    
    Args:
        mcp_client (MCPClient): The initialized MCP client.
        mcp_agent: The AI agent instance that processes user input.
    """
    console = Console()  # Initialize console for Rich text display
    message_history = []  # Store conversation history
    
    print("=== Langgraph AI MCP CLI Chat ===")  # Welcome message
    
    try:
        while True:
            user_input = input("\n[You] ")  # Prompt user for input
            
            # Exit condition: If user types any of the exit commands
            if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                print("Goodbye!")
                break
            
            try:
                message_history.append({"role": "user", "content": user_input})  # Store user message
                
                print("\n[Assistant]")
                with Live('', console=console, vertical_overflow='visible') as live:
                    input_data = {"messages": message_history}  # Prepare input data for AI agent
                    
                    curr_message = ""  # Store the current AI response
                    for chunk in mcp_agent.stream(input_data):  # Stream AI response
                        if "agent" in chunk and "messages" in chunk["agent"]:
                            messages = chunk["agent"]["messages"]
                            if messages and hasattr(messages[-1], "content"):
                                new_content = messages[-1].content
                                if new_content != curr_message:
                                    curr_message = new_content  # Update current message
                                    live.update(Markdown(curr_message))  # Display updated message
                    
                # Store AI response in conversation history
                if curr_message:
                    message_history.append({"role": "assistant", "content": curr_message})
                
            except Exception as e:
                print(f"\n[Error] An error occurred: {str(e)}")
                import traceback
                traceback.print_exc()  # Print full error traceback for debugging
    
    finally:
        await mcp_client.cleanup()  # Cleanup resources when the chat ends

async def main():
    """
    Entry point of the application.
    
    This function initializes the AI agent and starts the chat loop.
    """
    mcp_client, mcp_agent = await get_langgraph_ai_agent()  # Initialize AI agent
    await chat_loop(mcp_client, mcp_agent)  # Start chat session

if __name__ == "__main__":
    asyncio.run(main())  # Run the main function asynchronously
