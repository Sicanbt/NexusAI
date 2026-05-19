"""
NexusAI — Example usage scripts
"""

import asyncio
from nexus.core.orchestrator import Orchestrator
from nexus.core.config import NexusConfig


async def example_investment_research():
    """Example: AI infrastructure investment analysis"""
    config = NexusConfig(stream=True, enable_validator=True)
    orchestrator = Orchestrator(config)
    await orchestrator.run(
        "Analyze the top 5 AI infrastructure companies and recommend the best investment target for 2025"
    )


async def example_market_analysis():
    """Example: Crypto market decision"""
    config = NexusConfig(stream=True)
    orchestrator = Orchestrator(config)
    await orchestrator.run(
        "Should I allocate to ETH or SOL in Q3 2025? Analyze on-chain metrics, developer activity, and macro trends."
    )


async def example_competitive_intel():
    """Example: Competitive intelligence"""
    config = NexusConfig(stream=True, enable_validator=True, max_reasoning_steps=16)
    orchestrator = Orchestrator(config)
    await orchestrator.run(
        "Compare OpenAI, Anthropic, and Google DeepMind on: model capability, enterprise adoption, and 12-month outlook"
    )


if __name__ == "__main__":
    asyncio.run(example_investment_research())
