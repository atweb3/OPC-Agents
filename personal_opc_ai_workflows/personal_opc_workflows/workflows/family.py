"""Family companion workflow for daily father-child logs."""

from __future__ import annotations

from typing import Any

from ..core import WorkflowContext, WorkflowResult, slugify, write_json, write_text


def run(payload: dict[str, Any], context: WorkflowContext) -> WorkflowResult:
    date = payload.get("date", context.today)
    reading = payload.get("reading", "共读 15 分钟")
    basketball = payload.get("basketball", "运球 10 分钟")
    rope_skipping = payload.get("rope_skipping", "跳绳 100 个")
    child_quote = payload.get("child_quote", "今天我还想再读一页。")
    father_reflection = payload.get(
        "father_reflection", "今天更重要的是陪伴的质量，而不是完成多少任务。"
    )
    tomorrow_action = payload.get(
        "tomorrow_action", "明天继续共读，并把篮球练习控制在轻松愉快的节奏。"
    )
    domain_dir = context.domain_dir("family")
    slug = slugify(date)

    data = {
        "date": date,
        "reading": reading,
        "basketball": basketball,
        "rope_skipping": rope_skipping,
        "child_quote": child_quote,
        "father_reflection": father_reflection,
        "tomorrow_action": tomorrow_action,
    }
    note = f"""
# 年糕的今天｜{date}

## 共读
{reading}

## 运动

- 篮球：{basketball}
- 跳绳：{rope_skipping}

## 今天最值得记住的一句话

> {child_quote}

## 爸爸的反思

{father_reflection}

## 明天的小行动

{tomorrow_action}
"""
    public_post = f"""
# 可公开短文｜年糕的今天

今天最好的时刻，不是完成了多少计划，而是他抬头说：『{child_quote}』

共读、篮球、跳绳都只是形式，真正想留下的是：爸爸在场，孩子被看见。
"""
    files = [
        write_json(domain_dir / f"{slug}_原始记录.json", data),
        write_text(domain_dir / f"{slug}_年糕的今天.md", note),
        write_text(domain_dir / f"{slug}_公开短文.md", public_post),
    ]
    return WorkflowResult(
        name="family-day",
        files=files,
        next_actions=[
            "睡前补一句孩子原话",
            "周日汇总本周共读和运动",
            "公开发布前去掉隐私细节",
        ],
    )
