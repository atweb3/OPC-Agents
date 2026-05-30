# Personal OPC AI Workflows

[![CI](https://github.com/YOUR_NAME/personal-opc-ai-workflows/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_NAME/personal-opc-ai-workflows/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

年糕爸爸专属的 **OPC 一人公司 AI 工作流中台 MVP**：用 Python 把商业图书、校友会走访、AI 引流内容、信仰查经、亲子陪伴、词典写作、个人硬核建设拆成可运行的自动化/半自动化流程。

这个仓库是 **独立 Python 项目**，不依赖 OPC-Agents 源码运行；它只是参考了 OPC-Agents 的“技能注册 + 工作流产出”思想。当前版本默认不调用外部 API，不需要 OpenAI/MOKA/GLM key，运行后会生成 Markdown、HTML、JSON 成果物。

> 创建到你自己的 GitHub 后，把 README 顶部 badge 里的 `YOUR_NAME` 替换成你的 GitHub 用户名。

---

## 已内置的 7 个工作流

| 工作流 | 命令名 | 解决什么问题 | 输出示例 |
|---|---|---|---|
| 商业图书创作项目 | `business-book` | 公司历史/管理实践产品介绍、HTML 落地页、两套定价系统 | 产品介绍 `.md` + `.html` |
| 校友会企业走访内容 | `alumni-visit` | 浙大校友会走访后生成推文、短视频、私域跟进 | 推文、短视频脚本、私域话术 |
| AI 引流内容矩阵 | `media-growth` | 年糕爸爸 notes、小红书、短视频多平台内容 | 微信 notes、小红书、短视频脚本 |
| 查经与信仰认知 | `faith-study` | 合规短引用、观察/解释/应用、查经问题、祷告草稿 | 查经笔记 `.md` |
| 年糕的今天 | `family-day` | 父子共读、篮球、跳绳、孩子金句、公开短文 | 私密日志、公开短文、JSON 记录 |
| 拓扑星丛词典 | `topology-lexicon` | 《拓扑星丛：AI时代的简明思辨词典》词条生产 | 词条文章 `.md` |
| 个人硬核建设 | `personal-growth` | Vibecoding + Python、跑步、书法、多邻国、查经 | 今日计划 `.md` |

---

## GitHub 发布状态

这个目录已经整理成真正可发布的 GitHub repo MVP，包含：

- `README.md`：项目说明和使用手册
- `LICENSE`：MIT License
- `pyproject.toml`：可安装 Python 包和 `personal-opc` CLI 入口
- `.github/workflows/ci.yml`：GitHub Actions 自动测试
- `CONTRIBUTING.md`：贡献/扩展规则
- `SECURITY.md`：隐私与安全边界
- `CHANGELOG.md`：版本记录
- `docs/GITHUB_SETUP.md`：GitHub 创建仓库步骤
- `docs/ROADMAP.md`：后续路线图
- `data/samples/`：可直接运行的示例输入
- `personal_opc_workflows/data/samples/`：安装后也可读取的打包样例

如果你还没有创建 GitHub 仓库，请先看：[`docs/GITHUB_SETUP.md`](docs/GITHUB_SETUP.md)。

---

## 快速开始：不用改代码，直接跑

### 方式 A：一键运行全部示例

macOS / Linux：

```bash
./start.sh
```

Windows：

```bat
start.bat
```

运行后查看：

```text
opc_workflow_output/
├── alumni_visit/
├── business_book/
├── faith/
├── family/
├── media_growth/
├── personal_growth/
├── topology_lexicon/
└── run_all_summary.json
```

### 方式 B：用 Python 模块运行全部示例

```bash
python -m personal_opc_workflows run-all
```

### 方式 C：只运行一个流程

```bash
python -m personal_opc_workflows run business-book --sample
python -m personal_opc_workflows run alumni-visit --sample
python -m personal_opc_workflows run media-growth --sample
python -m personal_opc_workflows run faith-study --sample
python -m personal_opc_workflows run family-day --sample
python -m personal_opc_workflows run topology-lexicon --sample
python -m personal_opc_workflows run personal-growth --sample
```

### 方式 D：列出所有流程

```bash
python -m personal_opc_workflows list
```

---

## 安装依赖

当前 MVP 只使用 Python 标准库，Python 3.10+ 即可。

```bash
python --version
python -m pip install -r requirements.txt
```

如果你想把命令安装成 `personal-opc`：

```bash
python -m pip install -e .
personal-opc run-all
personal-opc run business-book --sample
```

---

## 想换成你自己的输入，但不改代码

先复制示例输入：

```bash
python -m personal_opc_workflows init-samples --target my_inputs
```

然后编辑 `my_inputs/*.json`，例如：

```text
my_inputs/business-book.json
my_inputs/alumni-visit.json
my_inputs/media-growth.json
my_inputs/family-day.json
```

运行自定义输入：

```bash
python -m personal_opc_workflows run business-book --input my_inputs/business-book.json
python -m personal_opc_workflows run family-day --input my_inputs/family-day.json
```

如果同时传入 `--sample` 和 `--input`，系统会先读取内置示例，再用你的 JSON 覆盖同名字段：

```bash
python -m personal_opc_workflows run business-book --sample --input my_inputs/business-book.json
```

`my_inputs/` 默认被 `.gitignore` 忽略，适合放个人私密输入。

---

## 每个流程怎么用

### 商业图书创作项目

适合你的高 ROI 主线：公司历史、管理实践、估值与故事、股票量化实操、线下工作坊和线上引流课。

```bash
python -m personal_opc_workflows run business-book --sample
```

它会生成：

- 商业图书项目介绍 Markdown
- HTML 产品介绍落地页
- 18万 / 38万 / 58万线下工作坊定价表
- 19.9 / 199 / 1999线上引流课定价表
- 销售 FAQ

建议第一优先级：把生成的 HTML 发给 3 个可信校友/企业主，看他们是否愿意约 30 分钟诊断。

### 校友会企业走访内容

```bash
python -m personal_opc_workflows run alumni-visit --sample
```

输出：

- 企业走访公众号推文
- 60 秒短视频脚本
- 私域跟进话术

发布前请人工确认企业名称、照片、观点和活动主办方的公开边界。

### AI 引流内容矩阵

```bash
python -m personal_opc_workflows run media-growth --sample
```

输出：

- 年糕爸爸 notes 微信内容
- 小红书笔记
- 短视频脚本

建议节奏：每周至少跑 3 次，把评论和私聊问题沉淀为下一轮选题。

### 查经与信仰认知

```bash
python -m personal_opc_workflows run faith-study --sample
```

注意：NIV 是受版权保护的现代译本。本流程不会自动批量翻译或分发 NIV 全文，只做短句合规引用、观察、解释、应用、讨论问题和祷告草稿。你需要自己确认引用范围和使用许可。

### 年糕的今天

```bash
python -m personal_opc_workflows run family-day --sample
```

输出：

- 私密每日记录
- 可公开短文
- 原始 JSON 记录

建议每天睡前 3 分钟记录，不追求文学性，只追求真实和长期复利。

### 《拓扑星丛》词条

```bash
python -m personal_opc_workflows run topology-lexicon --sample
```

每个词条包含：直觉定义、AI 时代语境、反例、关系网络、隐喻和金句。

### 个人硬核可持续建设

```bash
python -m personal_opc_workflows run personal-growth --sample
```

适合把 Vibecoding + Python、跑步、王力、书法、多邻国和周六查经压缩成可执行的每日最小行动。

---

## 本地验证

```bash
python -m personal_opc_workflows run-all --output /tmp/personal_opc_check
PYTHONPATH=. pytest tests -q
python -m compileall personal_opc_workflows
```

如果安装了 Black，也可以运行：

```bash
python -m black --check personal_opc_workflows tests
```

---

## 目录结构

```text
personal-opc-ai-workflows/
├── .github/workflows/ci.yml       # GitHub Actions CI
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── pyproject.toml
├── requirements.txt
├── start.sh
├── start.bat
├── data/samples/                  # 不用改代码，改 JSON 即可换输入
├── docs/                          # GitHub 创建和路线图文档
├── scripts/                       # 常用快捷脚本
├── tests/                         # 基础 CLI 测试
└── personal_opc_workflows/
    ├── cli.py                     # 命令行入口
    ├── core.py                    # 上下文、结果、文件写入、HTML 渲染、注册表
    ├── registry.py                # 注册所有工作流
    ├── data/samples/              # 打包安装后的示例输入
    └── workflows/
        ├── business_book.py
        ├── alumni_visit.py
        ├── media_growth.py
        ├── faith.py
        ├── family.py
        ├── lexicon.py
        └── learning.py
```

---

## 后续升级路线

1. 增加 weekly-review 工作流，汇总一周商业推进、内容发布、亲子记录、查经和学习训练。
2. 增加 AI 出海 / AI 玄幻 / 语文小馆记忆宫殿等专项工作流。
3. 增加可选 LLM adapter，但保留当前离线模板 fallback。
4. 增加 CRM 跟进和发布日历。
5. 未来可选接入 OPC-Agents SkillRegistry，但不是当前运行依赖。

---

## 推荐第一周用法

```text
周一：business-book，生成产品介绍 HTML
周二：media-growth，发布 AI 学习内容
周三：family-day，记录年糕的今天
周四：alumni-visit，准备企业走访内容模板
周五：business-book，迭代销售 FAQ 和私域话术
周六：faith-study，准备查经
周日：personal-growth + topology-lexicon，做周复盘和词条沉淀
```
