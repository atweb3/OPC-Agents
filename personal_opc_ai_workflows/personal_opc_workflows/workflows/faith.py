"""Faith study workflow with NIV copyright-safe guardrails."""

from __future__ import annotations

from typing import Any

from ..core import WorkflowContext, WorkflowResult, slugify, write_text

NIV_WARNING = (
    "NIV 是受版权保护的现代译本。本工作流只做短句合规引用、主题摘要、观察/解释/应用和查经问题，"
    "不自动批量翻译或分发 NIV 全文。"
)


def run(payload: dict[str, Any], context: WorkflowContext) -> WorkflowResult:
    passage_ref = payload.get("passage_ref", "John 15:1-8")
    allowed_quote = payload.get(
        "allowed_quote", "请在这里放入你有权使用的短段经文引用。"
    )
    theme = payload.get("theme", "住在基督里")
    life_context = payload.get("life_context", "近期在工作、家庭和学习之间寻找秩序。")
    group_context = payload.get("group_context", "周六查经")
    domain_dir = context.domain_dir("faith")
    slug = slugify(passage_ref.replace(":", "_"))

    note = f"""
# 查经笔记：{passage_ref}

> 合规引用片段：
> {allowed_quote}

## 版权与使用边界

{NIV_WARNING}

## 一、观察：经文直接呈现了什么？

- 主要人物/对象是谁？
- 动词、命令、应许和警告有哪些？
- 重复出现的词是什么？
- 这段经文中的张力是什么？

## 二、解释：这段经文可能在回应什么问题？

主题：{theme}

建议从三个层面理解：

1. 上下文：前后段落如何连接？
2. 关键词：核心词的含义是什么？
3. 救赎历史：这段如何指向神的属性、人的处境与回应？

## 三、应用：和我现在的生活有什么关系？

我的处境：
{life_context}

可以反思：

- 我在哪些地方依靠自己的判断多过依靠神？
- 我在哪些地方需要悔改、信靠或顺服？
- 本周一个具体行动是什么？

## 四、{group_context}讨论问题

1. 这段经文最触动你的是哪一句？为什么？
2. 如果把这段经文放进你本周的处境，你会看到什么提醒？
3. 这段经文挑战了我们哪一种常见的生活方式？
4. 本周你愿意实践一个什么小行动？

## 五、祷告草稿

主啊，求你帮助我不是只理解这段经文，而是在真实生活中回应你。也求你帮助我在工作、家庭、学习和服事中，更清楚地认识你的心意。阿们。
"""

    path = write_text(domain_dir / f"{context.today}_{slug}_查经笔记.md", note)
    return WorkflowResult(
        name="faith-study",
        files=[path],
        next_actions=[
            "补充上下文观察",
            "向小组确认讨论问题是否合适",
            "记录本周一个可执行的顺服行动",
        ],
        warnings=[NIV_WARNING],
    )
