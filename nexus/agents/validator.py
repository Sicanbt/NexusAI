from dataclasses import dataclass, field
from typing import List
from nexus.core.config import NexusConfig
from nexus.core.llm import call_llm
from nexus.agents.analyst import AnalysisResult


@dataclass
class CritiqueResult:
    has_issues: bool
    summary: str
    issues: List[str]


class ValidatorAgent:
    """
    Adversarial agent. Challenges analyst conclusions.
    Looks for logical fallacies, missing evidence, overconfidence.
    """

    def __init__(self, config: NexusConfig):
        self.config = config

    async def run(self, task: str, analysis: AnalysisResult) -> CritiqueResult:
        prompt = f"""You are a critical reviewer. Your job is to find flaws in this analysis.

Task: {task}

Analyst conclusion:
{analysis.conclusion}

Reasoning chain (last 5 steps):
{chr(10).join(analysis.reasoning_chain[-5:])}

Find issues with:
1. Logical fallacies or leaps
2. Missing counter-evidence
3. Overconfident claims without sufficient data
4. Biases or assumptions

Respond in JSON:
{{
  "has_issues": true/false,
  "summary": "one sentence summary",
  "issues": ["issue 1", "issue 2", ...]
}}"""

        resp = await call_llm(
            self.config, prompt,
            system="You are a rigorous fact-checker and logic critic. Be harsh but fair."
        )

        import json, re
        try:
            match = re.search(r'\{.*\}', resp, re.DOTALL)
            data = json.loads(match.group())
            return CritiqueResult(
                has_issues=data.get("has_issues", False),
                summary=data.get("summary", ""),
                issues=data.get("issues", []),
            )
        except:
            return CritiqueResult(has_issues=False, summary="Validation passed.", issues=[])
