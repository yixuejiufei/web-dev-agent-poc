"""Shared pytest fixtures."""

from pathlib import Path

from dotenv import load_dotenv

# Load project .env so tests can pick up AGENT_LITELLM_MASTER_KEY
load_dotenv(Path(__file__).parent.parent / ".env", override=True)
