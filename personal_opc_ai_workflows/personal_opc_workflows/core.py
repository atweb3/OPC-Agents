"""Core utilities for the personal OPC AI workflow kit.

The package intentionally works without network access or paid API keys.  Each
workflow is a deterministic, template-based "AI workflow skeleton" that can be
run immediately, then later connected to OPC-Agents or an LLM service.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from html import escape
import json
from pathlib import Path
import re
from typing import Any, Callable

DEFAULT_OUTPUT_DIR = "opc_workflow_output"


@dataclass(slots=True)
class WorkflowResult:
    """A normalized workflow execution result."""

    name: str
    files: list[Path] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "files": [str(path) for path in self.files],
            "next_actions": self.next_actions,
            "warnings": self.warnings,
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class WorkflowContext:
    """Runtime context shared by all workflows."""

    output_dir: Path
    today: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))

    @classmethod
    def from_output_dir(cls, output_dir: str | Path | None = None) -> "WorkflowContext":
        root = Path(output_dir or DEFAULT_OUTPUT_DIR).expanduser().resolve()
        root.mkdir(parents=True, exist_ok=True)
        return cls(output_dir=root)

    def domain_dir(self, domain: str) -> Path:
        path = self.output_dir / domain
        path.mkdir(parents=True, exist_ok=True)
        return path


def slugify(value: str, max_len: int = 32) -> str:
    """Create a filesystem-safe slug while preserving Chinese characters."""

    cleaned = re.sub(r"[^\w\u4e00-\u9fff-]+", "_", value.strip())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return (cleaned or "untitled")[:max_len]


def read_json(path: str | Path) -> dict[str, Any]:
    with Path(path).expanduser().open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_text(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    return path


def write_json(path: Path, data: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return path


def markdown_to_simple_html(
    title: str, markdown_content: str, subtitle: str = ""
) -> str:
    """Render a lightweight, dependency-free HTML page from Markdown-like text."""

    safe_title = escape(title)
    safe_subtitle = escape(subtitle)
    safe_body = escape(markdown_content)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{safe_title}</title>
  <style>
    :root {{ color-scheme: light; }}
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f8fafc; color: #111827; }}
    .hero {{ padding: 52px 24px; background: linear-gradient(135deg, #111827, #334155); color: white; }}
    .hero-inner, main {{ max-width: 980px; margin: 0 auto; }}
    h1 {{ margin: 0 0 12px; font-size: clamp(30px, 5vw, 56px); line-height: 1.1; }}
    .subtitle {{ color: #dbeafe; font-size: 18px; max-width: 760px; }}
    main {{ background: white; margin-top: -24px; border-radius: 24px; padding: 28px; box-shadow: 0 18px 60px rgba(15, 23, 42, .12); }}
    pre {{ white-space: pre-wrap; word-wrap: break-word; font: 16px/1.75 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    .cta {{ margin-top: 28px; padding: 18px 20px; border-radius: 16px; background: #fef3c7; border: 1px solid #fde68a; }}
  </style>
</head>
<body>
  <section class="hero"><div class="hero-inner"><h1>{safe_title}</h1><div class="subtitle">{safe_subtitle}</div></div></section>
  <main>
    <pre>{safe_body}</pre>
    <div class="cta">下一步：挑选一个输出文件，人工审定事实、隐私和发布边界，然后进入发布/跟进。</div>
  </main>
</body>
</html>"""


class WorkflowRegistry:
    """Small local skill registry mirroring OPC-Agents' skill-first workflow style."""

    def __init__(self) -> None:
        self._handlers: dict[
            str, Callable[[dict[str, Any], WorkflowContext], WorkflowResult]
        ] = {}

    def register(
        self,
        name: str,
        handler: Callable[[dict[str, Any], WorkflowContext], WorkflowResult],
    ) -> None:
        if name in self._handlers:
            raise ValueError(f"workflow already registered: {name}")
        self._handlers[name] = handler

    def names(self) -> list[str]:
        return sorted(self._handlers)

    def run(
        self, name: str, payload: dict[str, Any], context: WorkflowContext
    ) -> WorkflowResult:
        if name not in self._handlers:
            available = ", ".join(self.names())
            raise KeyError(f"unknown workflow: {name}; available: {available}")
        return self._handlers[name](payload, context)
