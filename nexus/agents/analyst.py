from dataclasses import dataclass, field
from typing import List, Optional
from rich.console import Console
from nexus.core.config import NexusConfig
from nexus.core.llm import call_llm
from nexus.agents.research import ResearchResult

console = Console()

@dataclass
class AnalysisResult:
    conclusion: str
    reasoning_chain: List[str]
    reasoning_steps: int
    confidence: float
    tokens_used: int = 0


class AnalystAgent:
    """
    Chain-of-thought reasoning engine.
    Iteratively reasons through research findings up to max_steps.
    """

    def __init__(self, config: NexusConfig):
        self.config = config

    async def run(self, task: str, research: List[ResearchResult], max_steps: int) -> AnalysisResult:
        # Compile research into context
        context = "\n\n".join([
            f"### Subtask: {r.subtask}\n{r.findings}"
            for r in research
        ])

        reasoning_chain = []
        current_thought = ""

        for step in range(1, max_steps + 1):
            prompt = self._build_step_prompt(task, context, reasoning_chain, step)
            thought = await call_llm(
                self.config, prompt,
                system="You are an expert analyst. Reason step by step. Be precise and critical."
            )
            reasoning_chain.append(f"Step {step}: {thought.strip()}")

            if self.config.stream:
                console.print(f"  [dim]Step {step}:[/dim] {thought.strip()[:120]}...")

            # Check if reasoning has converged
            if any(marker in thought.lower() for marker in ["final conclusion:", "therefore:", "in conclusion:"]):
                break

        # Extract final conclusion
        conclusion = await self._extract_conclusion(task, reasoning_chain)
        confidence = await self._estimate_confidence(task, reasoning_chain)

        return AnalysisResult(
            conclusion=conclusion,
            reasoning_chain=reasoning_chain,
            reasoning_steps=len(reasoning_chain),
            confidence=confidence,
        )

    async def revise(self, analysis: AnalysisResult, critique) -> AnalysisResult:
        """Revise analysis based on validator critique."""
        prompt = f"""Your previous analysis has been challenged. Revise your conclusion.

Original conclusion:
{analysis.conclusion}

Critique:
{critique.summary}

Specific issues:
{chr(10).join(critique.issues)}

Provide a revised, more accurate conclusion."""

        revised = await call_llm(
            self.config, prompt,
            system="You are an expert analyst. Accept valid criticism and improve your reasoning."
        )
        analysis.conclusion = revised
        analysis.reasoning_chain.append(f"[REVISION] {revised}")
        return analysis

    def _build_step_prompt(self, task: str, context: str, chain: List[str], step: int) -> str:
        prior = "\n".join(chain[-3:]) if chain else "None yet."
        return f"""Task: {task}

Research findings:
{context[:3000]}

Prior reasoning steps:
{prior}

Step {step}: Continue reasoning. If you have enough to conclude, start with "Final conclusion:".
"""

    async def _extract_conclusion(self, task: str, chain: List[str]) -> str:
        reasoning = "\n".join(chain)
        prompt = f"""Based on this reasoning chain, write a clear, specific final conclusion for:
Task: {task}

Reasoning:
{reasoning[-4000:]}

Write the conclusion in 2-4 sentences. Be specific, not generic."""
        return await call_llm(self.config, prompt, system="You are a synthesis expert.")

    async def _estimate_confidence(self, task: str, chain: List[str]) -> float:
        reasoning = "\n".join(chain[-5:])
        prompt = f"""Rate your confidence in this conclusion from 0.0 to 1.0.
Return ONLY a number like 0.85. Nothing else.

Task: {task}
Final reasoning: {reasoning[-1000:]}"""
        resp = await call_llm(self.config, prompt)
        try:
            import re
            match = re.search(r'0\.\d+|1\.0', resp)
            return float(match.group()) if match else 0.75
        except:
            return 0.75
