"""Alumni association company-visit content workflow."""

from __future__ import annotations

from typing import Any

from ..core import WorkflowContext, WorkflowResult, slugify, write_text


def run(payload: dict[str, Any], context: WorkflowContext) -> WorkflowResult:
    company = payload.get("company", "走访企业")
    event_name = payload.get("event_name", "浙大校友会求是创业帮走访企业活动")
    observations = payload.get(
        "key_observations",
        ["创始人长期主义", "组织管理实践", "产品与客户之间的真实连接"],
    )
    quotes = payload.get("quotes", ["企业最重要的资产，是一路做选择留下来的经验。"])
    business_angle = payload.get(
        "business_angle", "企业历史与管理实践如何转化为可传播的图书资产"
    )
    domain_dir = context.domain_dir("alumni_visit")
    slug = slugify(company)

    obs_md = "\n".join(f"- {item}" for item in observations)
    quote_md = "\n".join(f"> {item}" for item in quotes)

    article = f"""
# 从 {company} 的企业现场，看见故事资产的价值

今天参加「{event_name}」，走访了 {company}。

## 一、现场最打动我的几个细节

{obs_md}

## 二、企业真正有价值的，不只是产品，还有走过的路

{quote_md}

一家企业的历史，往往藏在创始人的选择、团队的冲突、关键节点的取舍里。

## 三、从公司历史到管理实践

这些故事如果只留在内部，就只是记忆；如果被结构化整理，就会变成品牌资产、组织资产和资本故事。

## 四、我的观察

{business_angle}

## 五、延伸：商业图书创作项目

我最近正在推动一个项目：用 AI + 访谈 + 商业叙事，帮助企业把公司历史、管理实践、创始人思想整理成一本真正有价值的商业图书。

如果你也想系统梳理企业故事，欢迎交流。
"""

    video = f"""
# 短视频脚本：{company} 走访观察

## 0-3 秒
今天走访 {company}，我最大的感受是：企业最值钱的资产，不一定写在财报里。

## 3-20 秒
我观察到三个细节：
{chr(10).join(f'{idx + 1}. {item}' for idx, item in enumerate(observations[:3]))}

## 20-40 秒
这些细节背后，是企业的历史、管理实践和创始人的判断力。

## 40-55 秒
如果把这些内容系统整理，就可能变成一本企业图书、一套组织教材，甚至是一套资本故事。

## 55-60 秒
我是年糕爸爸，最近在做 AI 商业图书创作项目，欢迎交流。
"""

    followup = f"""
# 私域跟进话术：{company}

1. 今天走访很受启发，尤其是「{observations[0]}」。我在想，这类企业经验如果系统整理，可能会成为很好的组织资产。
2. 我最近在做一个 AI 商业图书创作项目，可以把企业历史和管理实践整理成图书/内训/传播素材。方便的话我可以发你一页介绍。
3. 如果你们内部也有类似公司史、管理实践或创始人叙事需求，我可以免费做一次 30 分钟初步诊断。
"""

    files = [
        write_text(domain_dir / f"{context.today}_{slug}_推文.md", article),
        write_text(domain_dir / f"{context.today}_{slug}_短视频脚本.md", video),
        write_text(domain_dir / f"{context.today}_{slug}_私域跟进.md", followup),
    ]
    return WorkflowResult(
        name="alumni-visit",
        files=files,
        next_actions=[
            "确认企业名称、观点和照片是否可公开",
            "选 3 张照片配推文",
            "把私域话术发给 3 个高信任联系人",
        ],
        warnings=["发布前请人工确认活动主办方和企业方的公开边界。"],
    )
