"""Personal hard-core sustainable growth planning workflow."""

from __future__ import annotations

from typing import Any

from ..core import WorkflowContext, WorkflowResult, slugify, write_text


def run(payload: dict[str, Any], context: WorkflowContext) -> WorkflowResult:
    energy = payload.get("energy", "中")
    available_minutes = int(payload.get("available_minutes", 90))
    focus = payload.get("focus", "Vibecoding + Python")
    skills = payload.get("skills", ["跑步", "王力", "书法", "多邻国（日语+法语+英语）"])
    social = payload.get("social", "周六查经")
    domain_dir = context.domain_dir("personal_growth")
    slug = slugify(f"{context.today}_{focus}")

    blocks = [
        (
            "身体",
            min(30, max(15, available_minutes // 3)),
            "跑步/拉伸/跳绳，目标是保持长期可持续。",
        ),
        (
            "心智",
            min(45, max(25, available_minutes // 2)),
            f"{focus}：写一个最小 Python 脚本或复盘一个 AI 概念。",
        ),
        (
            "灵性/关系",
            max(
                10,
                available_minutes
                - min(30, max(15, available_minutes // 3))
                - min(45, max(25, available_minutes // 2)),
            ),
            f"{social} / 亲子共读 / 给一个朋友发消息。",
        ),
    ]
    block_md = "\n".join(
        f"- **{name} {minutes} 分钟**：{task}" for name, minutes, task in blocks
    )
    skills_md = "\n".join(f"- {item}" for item in skills)

    content = f"""
# 今日硬核可持续建设｜{context.today}

## 今日状态

- 精力：{energy}
- 可用时间：{available_minutes} 分钟
- 主焦点：{focus}

## 今日三件事

{block_md}

## 技能池

{skills_md}

## 20 分钟 Python/Vibecoding 练习

1. 选一个重复任务。
2. 写出输入、处理、输出。
3. 用 Python 标准库完成最小版本。
4. 记录一个 bug 和一个改进点。

## 晚间复盘

- 今天真正完成了什么？
- 哪件事最值得明天延续？
- 哪个计划应该删掉或降级？
"""
    path = write_text(domain_dir / f"{slug}_今日计划.md", content)
    return WorkflowResult(
        name="personal-growth",
        files=[path],
        next_actions=[
            "晚上用 3 分钟填写复盘",
            "只保留明天最重要的 1 个技能动作",
            "每周日汇总一次趋势",
        ],
    )
