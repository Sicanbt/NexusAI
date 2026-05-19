from dataclasses import dataclass
from nexus.core.config import NexusConfig
from nexus.core.llm import call_llm
from nexus.agents.analyst import AnalysisResult


@dataclass
class SynthesisResult:
    report: str
    confidence: float
    reasoning_steps: int
    tokens_used: int


class SynthesisAgent:
    """
    Final stage. Merges all findings into a structured, investor-grade report.
    """

    def __init__(self, config: NexusConfig):
        self.config = config

    async def run(self, task: str, analysis: AnalysisResult) -> SynthesisResult:
        prompt = f"""You are a senior analyst writing a final decision report.

Task: {task}

Conclusion from analysis:
{analysis.conclusion}

Reasoning chain summary:
{chr(10).join(analysis.reasoning_chain[-8:])}

Write a structured report with:
1. **Executive Summary** (2-3 sentences)
2. **Key Findings** (3-5 bullet points)
3. **Recommendation** (clear, specific, actionable)
4. **Risk Factors** (2-3 items)
5. **Confidence Level** ({analysis.confidence:.0%})

Be specific. Use data. No filler."""

        report = await call_llm(
            self.config, prompt,
            system="You are a senior research analyst. Write clear, structured, data-driven reports."
        )

        return SynthesisResult(
            report=report,
            confidence=analysis.confidence,
            reasoning_steps=analysis.reasoning_steps,
            tokens_used=len(report.split()) * 2,  # rough estimate
        )
