"""Topology Star-Cluster lexicon writing workflow."""

from __future__ import annotations

from typing import Any

from ..core import WorkflowContext, WorkflowResult, slugify, write_text


def run(payload: dict[str, Any], context: WorkflowContext) -> WorkflowResult:
    term = payload.get("term", "提示词")
    intuitive_definition = payload.get(
        "intuitive_definition", "一种把模糊愿望变成可执行问题的语言接口。"
    )
    ai_context = payload.get(
        "ai_context", "在 AI 时代，提示词不是命令，而是人与模型共同构造任务空间的边界。"
    )
    counter_example = payload.get(
        "counter_example", "把提示词当作万能咒语，忽略事实、上下文和验收标准。"
    )
    related_terms = payload.get("related_terms", ["上下文", "约束", "反馈", "工作流"])
    metaphor = payload.get(
        "metaphor", "提示词像一张星图：它不替你航行，但能帮你确认方向。"
    )
    quote = payload.get("quote", "真正好的提示词，不是让 AI 更听话，而是让问题更清楚。")
    domain_dir = context.domain_dir("topology_lexicon")
    slug = slugify(term)

    related = "、".join(related_terms)
    content = f"""
# {term}

## 直觉定义

{intuitive_definition}

## AI 时代语境

{ai_context}

## 反例

{counter_example}

## 关系网络

相关词条：{related}

## 隐喻

{metaphor}

## 金句

> {quote}

## 下一步扩展

- 给这个词条补一个真实故事。
- 找一个相反词条。
- 把它连接到《拓扑星丛》的 3 个已有词条。
"""
    path = write_text(domain_dir / f"{context.today}_{slug}.md", content)
    return WorkflowResult(
        name="topology-lexicon",
        files=[path],
        next_actions=["补真实故事", "选择是否发布到微信读书", "把相关词条加入索引"],
    )
