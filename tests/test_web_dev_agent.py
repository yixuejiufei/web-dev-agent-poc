"""Tests for web-dev-agent-poc.

Run:
    pytest tests/ -v

Environment:
    Set AGENT_LITELLM_MASTER_KEY and AGENT_LITELLM_BASE_URL in .env
    to run the end-to-end LLM test. Otherwise that test is skipped.
"""

import os
from pathlib import Path

import pytest
import yaml

from yineng_factory.runtime import AgentRuntime


@pytest.fixture
def project_dir() -> Path:
    return Path(__file__).parent.parent


def test_agent_yaml_is_valid(project_dir: Path):
    """agent.yaml must pass schema validation."""
    from yineng_factory.schemas.agent import AgentConfigSchema

    data = yaml.safe_load((project_dir / "agent.yaml").read_text(encoding="utf-8"))
    schema = AgentConfigSchema(**data)
    assert schema.name == "web-dev-agent"
    assert schema.version == "0.1.0"
    assert schema.graph_entry == "graphs.main:app"
    assert schema.input_schema[0].name == "requirement"


def test_graph_loadable(project_dir: Path):
    """Graph entry point must import and compile."""
    import sys

    if str(project_dir) not in sys.path:
        sys.path.insert(0, str(project_dir))

    from graphs.main import app, build_graph

    graph = build_graph()
    assert graph is not None
    assert app is not None


def test_file_writer_tool(tmp_path: Path) -> None:
    """file_writer tool writes content to disk."""
    import sys

    project_dir = Path(__file__).parent.parent
    if str(project_dir) not in sys.path:
        sys.path.insert(0, str(project_dir))

    from tools.file_writer import write_file

    target = tmp_path / "subdir" / "test.txt"
    result = write_file(str(target), "hello")
    assert target.exists()
    assert target.read_text(encoding="utf-8") == "hello"
    assert "已写入文件" in result


def test_system_prompt_exists(project_dir: Path):
    """System prompt file must exist."""
    prompt_path = project_dir / "prompts" / "system.md"
    assert prompt_path.exists()
    content = prompt_path.read_text(encoding="utf-8")
    assert "HTML" in content
    assert "CSS" in content


@pytest.mark.skipif(
    not os.environ.get("AGENT_LITELLM_MASTER_KEY"),
    reason="AGENT_LITELLM_MASTER_KEY not set",
)
def test_dev_agent_end_to_end(project_dir: Path, tmp_path: Path, monkeypatch) -> None:
    """Run the full agent via AgentRuntime and verify it writes a valid HTML file."""
    # Use a temporary outputs directory so tests do not pollute the repo.
    outputs_dir = tmp_path / "outputs"
    outputs_dir.mkdir()

    # Load runtime and override output directory by patching the graph node.
    runtime = AgentRuntime.from_yaml(project_dir / "agent.yaml")

    # Patch Path in graphs.main so generated file goes to tmp_path, not repo.
    real_path = Path

    class MockPath:
        def __init__(self, *args):
            joined = real_path(*args)
            if str(joined) == "outputs" or str(joined).endswith("/outputs"):
                self._path = tmp_path / "outputs"
            else:
                self._path = joined

        def __getattr__(self, name):
            return getattr(self._path, name)

        def __truediv__(self, other):
            return self._path / other

        def __str__(self):
            return str(self._path)

    monkeypatch.setattr("graphs.main.Path", MockPath)

    requirement = "创建一个包含标题和段落的极简 HTML 页面"
    result = runtime.run(
        {"requirement": requirement},
    )

    assert "html_code" in result
    assert "output_path" in result
    assert result["summary"].startswith("已生成页面")

    html = result["html_code"]
    assert "<!DOCTYPE html>" in html or "<html" in html
    assert "</html>" in html

    output_path = Path(result["output_path"])
    assert output_path.exists()
    assert output_path.stat().st_size > 500


def test_agent_config_reads_agent_prefixed_env(project_dir: Path):
    """AgentConfig uses AGENT_ env prefix (regression test for engine usability)."""
    from yineng_factory.config.settings import AgentConfig

    # The conftest loads .env which sets AGENT_LITELLM_MASTER_KEY.
    config = AgentConfig()
    assert config.litellm_master_key is not None
    assert len(config.litellm_master_key) > 10

    # Base URL should also be picked up from AGENT_LITELLM_BASE_URL
    assert "localhost:4000" in config.litellm_base_url or "4000" in config.get_litellm_url()
