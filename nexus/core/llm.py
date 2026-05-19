import os
from typing import Optional
from nexus.core.config import NexusConfig

async def call_llm(config: NexusConfig, prompt: str, system: str = "You are a helpful AI assistant.", stream: bool = False) -> str:
    """Unified LLM caller. Routes to OpenAI or Anthropic based on config.model prefix."""

    if config.model.startswith("openai/") or config.model.startswith("gpt"):
        return await _call_openai(config, prompt, system, stream)
    elif config.model.startswith("anthropic/") or config.model.startswith("claude"):
        return await _call_anthropic(config, prompt, system, stream)
    else:
        raise ValueError(f"Unsupported model: {config.model}. Use openai/* or anthropic/*")


async def _call_openai(config: NexusConfig, prompt: str, system: str, stream: bool) -> str:
    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=config.openai_api_key)
    model_name = config.model.replace("openai/", "")

    response = await client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        stream=False,
    )
    return response.choices[0].message.content


async def _call_anthropic(config: NexusConfig, prompt: str, system: str, stream: bool) -> str:
    import anthropic
    client = anthropic.AsyncAnthropic(api_key=config.anthropic_api_key)
    model_name = config.model.replace("anthropic/", "")

    message = await client.messages.create(
        model=model_name,
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
