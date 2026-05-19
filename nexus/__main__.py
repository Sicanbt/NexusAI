from nexus.core.orchestrator import Orchestrator
from nexus.core.config import NexusConfig
import typer
import asyncio
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def run(
    task: str = typer.Argument(..., help="The task or question for NexusAI to solve"),
    model: str = typer.Option("openai/gpt-4o", help="LLM backend to use"),
    stream: bool = typer.Option(True, help="Stream reasoning output in real-time"),
    no_validator: bool = typer.Option(False, help="Skip validator agent (faster, less accurate)"),
):
    """Run NexusAI on a task. Deploys multi-agent swarm to research, reason, and decide."""
    config = NexusConfig(
        model=model,
        stream=stream,
        enable_validator=not no_validator,
    )
    orchestrator = Orchestrator(config)
    asyncio.run(orchestrator.run(task))

@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="API server host"),
    port: int = typer.Option(8000, help="API server port"),
):
    """Start the NexusAI REST API server."""
    import uvicorn
    from api.server import app as api_app
    uvicorn.run(api_app, host=host, port=port)

if __name__ == "__main__":
    app()
