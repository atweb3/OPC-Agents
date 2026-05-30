"""Media matrix workflow for WeChat notes, Xiaohongshu, and short video."""

from __future__ import annotations

from typing import Any

from ..core import WorkflowContext, WorkflowResult, slugify, write_text


def run(payload: dict[str, Any], context: WorkflowContext) -> WorkflowResult:
    pillar = payload.get("pillar", "AI学习")
    core_idea = payload.get("core_idea", "用 AI 降低学习成本")
    target_audience = payload.get("target_audience", "想用 AI 提升学习和工作的朋友")
    source_notes = payload.get(
        "source_notes", "今天记录一个小实验：用 Python 把重复内容生产流程自动化。"
    )
    cta = payload.get("cta", "如果你也在用 AI 做学习和成长，欢迎一起交流。")
    domain_dir = context.domain_dir("media_growth")
    slug = slugify(f"{pillar}_{core_idea}")

    wechat = f"""
# {pillar}｜{core_idea}

## 今天的一个触发点

{source_notes}

## 我的理解

这件事对「{target_audience}」的意义是：

- 它不是一个孤立知识点，而是一种长期能力。
- 它可以通过 AI 辅助降低练习成本。
- 它最终要回到真实生活和真实行动。

## 可以马上做的一件事

请今天只做一个小动作：围绕「{core_idea}」写下 3 个问题，并用 AI 生成一个 20 分钟练习计划。

## 结尾

{cta}
"""

    xhs = f"""
# 小红书笔记：{core_idea}

## 标题备选

1. 孩子/大人学习卡住？先别急着刷题
2. 我用 AI 做学习陪练，发现了这个关键
3. {core_idea}：普通人也能马上开始

## 正文

很多人不是不努力，而是不知道怎么把知识放进每天的行动里。

今天我做了一个小实验：

{source_notes}

适合马上试的 3 步：

1. 把问题写清楚。
2. 让 AI 生成一个最小练习。
3. 只做 20 分钟，然后复盘。

#{pillar} #AI学习 #个人成长 #高效学习 #年糕爸爸notes
"""

    video = f"""
# 短视频脚本：{core_idea}

## 0-3 秒
你以为 AI 是帮你偷懒，其实它更适合帮你开始练习。

## 3-20 秒
今天我用 AI 做了一个小实验：{source_notes}

## 20-45 秒
我的方法很简单：先让 AI 拆步骤，再让它给练习，最后用 3 个问题复盘。

## 45-60 秒
如果你也想从 Vibecoding + Python 开始系统学习 AI，可以先从今天这个 20 分钟练习开始。
"""

    files = [
        write_text(domain_dir / f"{context.today}_{slug}_微信notes.md", wechat),
        write_text(domain_dir / f"{context.today}_{slug}_小红书.md", xhs),
        write_text(domain_dir / f"{context.today}_{slug}_短视频脚本.md", video),
    ]
    return WorkflowResult(
        name="media-growth",
        files=files,
        next_actions=[
            "选一个平台今天发布",
            "把评论问题收集到下一轮选题",
            "每周复盘哪类内容更容易带来私聊",
        ],
    )
