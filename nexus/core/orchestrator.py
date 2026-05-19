import asyncio
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from nexus.core.config import NexusConfig
from nexus.agents.research import ResearchAgent
from nexus.agents.analyst import AnalystAgent
from nexus.agents.validator import ValidatorAgent
from nexus.agents.synthesis import SynthesisAgent
from nexus.memory.store import MemoryStore

console = Console()

class Orchestrator:
    """
    Central coordinator. Decomposes tasks, routes to specialized agents,
    manages inter-agent communication, and drives convergence.
    """

    def __init__(self, config: NexusConfig):
        self.config = config
        self.memory = MemoryStore(config)
        self.research = ResearchAgent(config)
        self.analyst = AnalystAgent(config)
        self.validator = ValidatorAgent(config) if config.enable_validator else None
        self.synthesis = SynthesisAgent(config)

    async def run(self, task: str) -> str:
        console.print(Panel(f"[bold cyan]NEXUSAI[/bold cyan] — Task received", subtitle=task))

        # Step 1: Decompose task into subtasks
        console.print("[bold yellow][ORCHESTRATOR][/bold yellow] Decomposing task...")
        subtasks = await self._decompose(task)
        for i, s in enumerate(subtasks, 1):
            console.print(f"  [dim]Subtask {i}:[/dim] {s}")

        # Step 2: Research phase (parallel)
        console.print("\n[bold blue][RESEARCH][/bold blue] Gathering data...")
        research_results = await asyncio.gather(*[
            self.research.run(subtask) for subtask in subtasks
        ])

        # Step 3: Analysis with chain-of-thought
        console.print("\n[bold green][ANALYST][/bold green] Reasoning through findings...")
        analysis = await self.analyst.run(task, research_results, self.config.max_reasoning_steps)

        # Step 4: Validation (optional but recommended)
        if self.validator:
            console.print("\n[bold red][VALIDATOR][/bold red] Challenging conclusions...")
            critique = await self.validator.run(task, analysis)
            if critique.has_issues:
                console.print(f"  [red]Issues found:[/red] {critique.summary}")
                console.print("\n[bold green][ANALYST][/bold green] Revising based on critique...")
                analysis = await self.analyst.revise(analysis, critique)
            else:
                console.print("  [green]No critical issues found.[/green]")

        # Step 5: Synthesize final output
        console.print("\n[bold magenta][SYNTHESIS][/bold magenta] Generating final report...")
        result = await self.synthesis.run(task, analysis)

        # Store in memory for future sessions
        await self.memory.store(task, result)

        console.print(Panel(result.report, title="[bold]FINAL REPORT[/bold]", border_style="green"))
        console.print(f"\n[dim]Confidence: {result.confidence:.0%} | Reasoning steps: {result.reasoning_steps} | Tokens: {result.tokens_used}[/dim]")

        return result.report

    async def _decompose(self, task: str) -> List[str]:
        """Break a complex task into parallel researchable subtasks."""
        from nexus.core.llm import call_llm
        prompt = f"""Break this task into 2-4 specific, parallel research subtasks.
Return ONLY a JSON array of strings. No explanation.

Task: {task}"""
        response = await call_llm(self.config, prompt, system="You are a task decomposition expert.")
        import json, re
        match = re.search(r'\[.*?\]', response, re.DOTALL)
        if match:
            return json.loads(match.group())
        return [task]
