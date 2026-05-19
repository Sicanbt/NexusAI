from dataclasses import dataclass
from typing import List, Optional
from nexus.core.config import NexusConfig
from nexus.core.llm import call_llm


@dataclass
class ResearchResult:
    subtask: str
    findings: str
    sources: List[str]


class ResearchAgent:
    """
    Gathers raw data for a given subtask.
    Uses web search (Serper) + document parsing when available.
    Falls back to LLM knowledge if no search key configured.
    """

    def __init__(self, config: NexusConfig):
        self.config = config

    async def run(self, subtask: str) -> ResearchResult:
        if self.config.serper_api_key:
            raw = await self._web_search(subtask)
        else:
            raw = await self._llm_knowledge(subtask)

        return ResearchResult(
            subtask=subtask,
            findings=raw["content"],
            sources=raw.get("sources", []),
        )

    async def _web_search(self, query: str) -> dict:
        import httpx
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": self.config.serper_api_key, "Content-Type": "application/json"},
                json={"q": query, "num": 5},
                timeout=15,
            )
            data = resp.json()

        snippets = []
        sources = []
        for item in data.get("organic", [])[:5]:
            snippets.append(f"- {item.get('title', '')}: {item.get('snippet', '')}")
            sources.append(item.get("link", ""))

        content = "\n".join(snippets) if snippets else "No results found."
        return {"content": content, "sources": sources}

    async def _llm_knowledge(self, query: str) -> dict:
        prompt = f"""Research the following topic and provide key facts, data points, and insights.
Be specific. Include numbers, names, and dates where relevant.

Topic: {query}"""
        content = await call_llm(
            self.config, prompt,
            system="You are a research specialist. Provide factual, data-rich findings."
        )
        return {"content": content, "sources": ["LLM knowledge base"]}
