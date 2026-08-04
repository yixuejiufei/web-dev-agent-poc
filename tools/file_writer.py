"""File writer tool for the web dev agent."""

from pathlib import Path

from yineng_factory.runtime import register_tool


@register_tool
def write_file(path: str, content: str) -> str:
    """Write content to a file.

    Args:
        path: Relative or absolute file path.
        content: File content to write.

    Returns:
        Confirmation message with the written path.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    return f"\u5df2\u5199\u5165\u6587\u4ef6\uff1a{file_path.resolve()}"
