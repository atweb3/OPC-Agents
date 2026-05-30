"""Business book creation and product-page workflow."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..core import (
    WorkflowContext,
    WorkflowResult,
    markdown_to_simple_html,
    slugify,
    write_text,
)


@dataclass(slots=True)
class BusinessBookProject:
    company_name: str
    themes: list[str]
    target_client: str
    offline_prices: list[int]
    online_prices: list[float]
    core_principle: str
    practice_base: str
    proof_points: list[str]

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "BusinessBookProject":
        return cls(
            company_name=payload.get("company_name", "示例企业"),
            themes=payload.get("themes", ["公司历史", "管理实践"]),
            target_client=payload.get("target_client", "创始人/品牌负责人/董秘"),
            offline_prices=payload.get("offline_prices", [180000, 380000, 580000]),
            online_prices=payload.get("online_prices", [19.9, 199, 1999]),
            core_principle=payload.get("core_principle", "估值与故事"),
            practice_base=payload.get("practice_base", "股票量化实操"),
            proof_points=payload.get(
                "proof_points", ["访谈", "大事记", "案例", "经营数据"]
            ),
        )


def _pricing_section(project: BusinessBookProject) -> str:
    offline = project.offline_prices
    online = project.online_prices
    return f"""
## 二、两套成交定价系统

### 线下工作坊成交

| 档位 | 价格 | 适合对象 | 核心交付 |
|---|---:|---|---|
| 标准版 | {offline[0]:,} 元 | 想启动企业叙事项目的创始团队 | 1天工作坊、全书目录、访谈提纲、样章方向 |
| 增长版 | {offline[1]:,} 元 | 已有材料但缺少结构化表达的企业 | 2天工作坊、3章样稿、传播主题、项目排期 |
| 战略版 | {offline[2]:,} 元 | 用于融资、品牌升级、组织传承的企业 | 3天工作坊、全书蓝图、创始人叙事、传播矩阵 |

### 线上引流课成交

| 档位 | 价格 | 定位 | 转化目标 |
|---|---:|---|---|
| 体验课 | {online[0]} 元 | 唤醒企业故事资产意识 | 获得低门槛线索 |
| 方法课 | {online[1]} 元 | 讲清楚企业图书创作方法 | 筛选高意向客户 |
| 训练营 | {online[2]} 元 | 完成一个企业叙事样章 | 转化线下工作坊 |
"""


def _sales_faq(project: BusinessBookProject) -> str:
    return f"""
## 五、销售 FAQ

**Q1：这和普通代写公司史有什么不同？**
A：我们不是简单写材料，而是围绕「{project.core_principle}」重构企业叙事，把历史、管理实践、创始人判断和未来价值连接起来。

**Q2：AI 会不会让内容很空？**
A：AI 只负责整理、初稿、改写和版本迭代；事实、判断、敏感边界和最终表达由人审定。

**Q3：为什么你们适合做这个？**
A：项目的实践基础是「{project.practice_base}」，强调数据、结构、复盘和可验证的商业推理。

**Q4：企业需要准备什么？**
A：准备公司大事记、创始人访谈、典型项目、组织制度、客户案例、公开报道等材料即可。
"""


def run(payload: dict[str, Any], context: WorkflowContext) -> WorkflowResult:
    project = BusinessBookProject.from_payload(payload)
    domain_dir = context.domain_dir("business_book")
    slug = slugify(project.company_name)
    theme_text = "、".join(project.themes)
    proof_text = "、".join(project.proof_points)

    markdown = f"""
# {project.company_name} 商业图书创作项目介绍

## 一、一句话定位

用 AI + 访谈 + 商业叙事方法，把企业的「{theme_text}」转化为可传播、可销售、可沉淀的图书资产。

## 项目适合谁

- {project.target_client}
- 正在做品牌升级、融资沟通、组织传承或管理实践沉淀的企业
- 希望把创始人经验、企业历史和管理方法论变成长期资产的团队

## 底层原理

- **{project.core_principle}**：企业的价值不仅在财务表里，也在它如何讲清楚过去、现在和未来。
- **{project.practice_base}**：用结构化、数据化、复盘化的方式增强商业叙事可信度。
- **AI 降本增效**：访谈整理、章节规划、初稿生成、版本迭代、内容分发形成流水线。

## 证据素材池

{proof_text}

{_pricing_section(project)}

## 三、标准交付流程

1. 诊断：明确企业叙事目标和读者对象。
2. 采集：访谈创始人/高管/员工，整理历史节点和管理实践。
3. 结构：生成图书目录、章节摘要、传播主题。
4. 成稿：AI 初稿 + 人工事实校验 + 风格统一。
5. 发布：PDF、HTML 落地页、推文、短视频和销售话术同步生成。

## 四、下一步行动

- 预约 30 分钟企业叙事诊断。
- 提供 3 个企业关键节点和 1 个典型管理案例。
- 选择线上课或线下工作坊作为第一步。

{_sales_faq(project)}
"""

    md_path = write_text(domain_dir / f"{context.today}_{slug}_产品介绍.md", markdown)
    html = markdown_to_simple_html(
        title=f"{project.company_name} 商业图书创作项目",
        subtitle="公司历史 × 管理实践 × 估值故事 × AI 降本增效",
        markdown_content=markdown,
    )
    html_path = write_text(domain_dir / f"{context.today}_{slug}_产品介绍.html", html)

    return WorkflowResult(
        name="business-book",
        files=[md_path, html_path],
        next_actions=[
            "补充一个真实企业案例，替换示例素材",
            "把 HTML 发给潜在客户或校友会联系人做 A/B 反馈",
            "从 FAQ 中挑 3 个问题生成朋友圈连续文案",
        ],
        metadata={"company_name": project.company_name, "themes": project.themes},
    )
