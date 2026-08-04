"""Web Dev Agent graph: generate a single-file HTML page from a requirement."""

from typing import Optional, TypedDict
from pathlib import Path

from langgraph.graph import END, StateGraph
from langgraph.checkpoint.memory import MemorySaver

from yineng_factory.llm import chat


class AgentState(TypedDict):
    """State for the web dev agent."""

    requirement: str
    html_code: Optional[str]
    output_path: Optional[str]
    summary: Optional[str]


def _load_system_prompt() -> str:
    prompt_path = Path(__file__).parent.parent / "prompts" / "system.md"
    return prompt_path.read_text(encoding="utf-8")


def _strip_markdown_code_block(text: str) -> str:
    text = text.strip()
    if text.startswith("```html"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


def generate_html(state: AgentState) -> dict:
    """Generate HTML code from the requirement using LLM."""
    system_prompt = _load_system_prompt()
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                "\u8bf7\u6839\u636e\u4ee5\u4e0b\u9700\u6c42\u751f\u6210\u4e00\u4e2a\u5b8c\u6574\u7684\u5355\u6587\u4ef6 HTML \u9875\u9762\uff1a\n\n"
                f"{state['requirement']}\n\n"
                "\u8bf7\u76f4\u63a5\u8f93\u51fa HTML \u4ee3\u7801\uff0c\u5305\u542b\u5185\u8054 CSS \u548c\u5fc5\u8981\u7684 JavaScript\u3002\u53ea\u8f93\u51fa\u4ee3\u7801\uff0c\u4e0d\u8981\u89e3\u91ca\u3002"
            ),
        },
    ]
    html_code = chat(messages)
    html_code = _strip_markdown_code_block(html_code)
    return {"html_code": html_code}


def write_output(state: AgentState) -> dict:
    """Write the generated HTML to outputs/index.html."""
    output_dir = Path(__file__).parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "index.html"
    output_path.write_text(state["html_code"], encoding="utf-8")
    return {
        "output_path": str(output_path),
        "summary": f"\u5df2\u751f\u6210\u9875\u9762\uff1a{output_path}",
    }


def build_graph():
    """Build the web dev agent graph."""
    graph = StateGraph(AgentState)
    graph.add_node("generate_html", generate_html)
    graph.add_node("write_output", write_output)
    graph.set_entry_point("generate_html")
    graph.add_edge("generate_html", "write_output")
    graph.add_edge("write_output", END)
    return graph.compile(checkpointer=MemorySaver())


# Compiled graph for CLI run (graphs.main:app)
app = build_graph()
