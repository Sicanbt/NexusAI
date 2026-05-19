from dataclasses import dataclass, field
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class NexusConfig:
    model: str = field(default_factory=lambda: os.getenv("DEFAULT_LLM", "openai/gpt-4o"))
    stream: bool = field(default_factory=lambda: os.getenv("STREAM_OUTPUT", "true").lower() == "true")
    enable_validator: bool = field(default_factory=lambda: os.getenv("ENABLE_VALIDATOR", "true").lower() == "true")
    max_reasoning_steps: int = field(default_factory=lambda: int(os.getenv("MAX_REASONING_STEPS", "32")))
    max_iterations: int = field(default_factory=lambda: int(os.getenv("MAX_AGENT_ITERATIONS", "10")))
    chroma_persist_dir: str = field(default_factory=lambda: os.getenv("CHROMA_PERSIST_DIR", "./data/chroma"))
    redis_url: str = field(default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379"))
    openai_api_key: Optional[str] = field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    anthropic_api_key: Optional[str] = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"))
    serper_api_key: Optional[str] = field(default_factory=lambda: os.getenv("SERPER_API_KEY"))
