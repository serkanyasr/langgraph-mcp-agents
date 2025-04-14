# app_client_adk.py
import asyncio
import pathlib
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich.panel import Panel

from mcp_client.tool_loader import load_tools_from_config  # Updated import from modular client

from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService

# === Setup environment ===
SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
CONFIG_FILE = SCRIPT_DIR / "mcp_config.json"
load_dotenv()
console = Console()


async def get_agent():
    """
    Initializes the LLM agent by loading tools from MCP via tool_loader.
    """
    tools = await load_tools_from_config(str(CONFIG_FILE), tool_type="google")
    console.log(f"[green]{len(tools)} tools loaded [/green]")
    agent = LlmAgent(
        model='gemini-2.0-flash',
        name='cli_assistant',
        instruction='Answer user queries in a helpful manner using available tools.',
        tools=tools,
    )
    return agent


async def chat_loop():
    """
    Main interactive chat loop using Rich CLI.
    Handles input, sends queries to the agent, and displays streamed responses.
    """
    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()

    session = session_service.create_session(
        state={}, app_name='cli_chat_app', user_id='user'
    )

    agent = await get_agent()

    runner = Runner(
        app_name='cli_chat_app',
        agent=agent,
        artifact_service=artifact_service,
        session_service=session_service,
    )

    console.print("[bold magenta]MCP AI CLI Chat[/bold magenta]")
    console.print("[cyan]Type your message (type 'exit' to quit)[/cyan]")

    while True:
        try:
            query = console.input("[bold green]You:[/bold green] ")

            if query.lower() in ["exit", "quit"]:
                console.print("\n[bold red]Exiting...[/bold red]")
                break

            user_content = types.Content(role='user', parts=[types.Part(text=query)])
            events_async = runner.run_async(
                session_id=session.id,
                user_id=session.user_id,
                new_message=user_content,
            )

            response_text = ""
            with Live(console=console, refresh_per_second=4) as live:
                async for event in events_async:
                    if event.is_final_response() and event.content and event.content.parts:
                        response_text = event.content.parts[0].text or ""
                        break
                    else:
                        live.update(Panel("Assistant is thinking...", title="\u23f3"))

            console.print(Panel(Markdown(response_text), title="[bold blue]Assistant[/bold blue]"))

        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")


if __name__ == "__main__":
    try:
        asyncio.run(chat_loop())
    except Exception as e:
        console.print(f"[bold red]Fatal Error:[/bold red] {e}")