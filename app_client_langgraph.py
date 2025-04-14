import os
import asyncio
import pathlib
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from mcp_client.tool_loader import load_tools_from_config  # Updated import for modular client

# === Environment Setup ===
SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
CONFIG_FILE = SCRIPT_DIR / "mcp_config.json"
load_dotenv()


def get_model():
    """
    Load OpenAI-compatible model with streaming support.
    """
    llm = os.getenv("MODEL_CHOICE", "gpt-4o")
    os.environ["OPENAI_API_KEY"] = os.getenv("LLM_API_KEY", "no-api-key-provided")

    return ChatOpenAI(
        model=llm,
        streaming=True,
        temperature=0,
    )


async def get_langgraph_ai_agent():
    """
    Initialize tools from MCP and build a LangGraph ReAct agent.
    """
    tools = await load_tools_from_config(str(CONFIG_FILE), tool_type="langgraph")
    console.log(f"[green]{len(tools)} tools loaded.[/green]")
    agent = create_react_agent(
        model=get_model(),
        tools=tools,
    )
    return agent

console = Console()
async def chat_loop(agent):
    """
    Interactive chat loop that streams LangGraph agent responses using Rich.
    """

    message_history = []

    console.print("[bold magenta]MCP AI CLI Chat[/bold magenta]")
    console.print("[cyan]Type your message (type 'exit' to quit)[/cyan]")

    while True:
        user_input = console.input("[bold green]You:[/bold green] ")

        if user_input.lower() in ["exit", "quit"]:
            console.print("\n[bold red]Exiting...[/bold red]")
            break

        message_history.append({"role": "user", "content": user_input})

        try:
            curr_message = ""
            with Live('', console=console, vertical_overflow='visible') as live:
                input_data = {"messages": message_history}

                for chunk in agent.stream(input_data):
                    if "agent" in chunk and "messages" in chunk["agent"]:
                        messages = chunk["agent"]["messages"]
                        if messages and hasattr(messages[-1], "content"):
                            new_content = messages[-1].content
                            if new_content != curr_message:
                                curr_message = new_content
                                live.update(Markdown(curr_message))

            if curr_message:
                message_history.append({"role": "assistant", "content": curr_message})

        except Exception as e:
            print(f"\n[Error] {e}")
            import traceback
            traceback.print_exc()


async def main():
    agent = await get_langgraph_ai_agent()
    await chat_loop(agent)


if __name__ == "__main__":
    asyncio.run(main())