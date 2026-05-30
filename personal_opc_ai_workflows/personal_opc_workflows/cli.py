"""Command-line interface for the personal OPC workflow kit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys
from typing import Any

from .core import WorkflowContext, read_json, write_json
from .registry import build_registry

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
PROJECT_SAMPLE_DIR = PACKAGE_ROOT / "data" / "samples"
PACKAGE_SAMPLE_DIR = Path(__file__).resolve().parent / "data" / "samples"
DEFAULT_OUTPUT_DIR = PACKAGE_ROOT / "opc_workflow_output"


def _sample_dir() -> Path:
    """Prefer repo-level samples, fall back to packaged samples after installation."""

    if PROJECT_SAMPLE_DIR.exists():
        return PROJECT_SAMPLE_DIR
    return PACKAGE_SAMPLE_DIR


def _load_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if args.sample:
        sample_path = _sample_dir() / f"{args.workflow}.json"
        payload.update(read_json(sample_path))
    if args.input:
        payload.update(read_json(args.input))
    return payload


def _print_result(result: dict[str, Any]) -> None:
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_list(_: argparse.Namespace) -> int:
    registry = build_registry()
    print("可用工作流：")
    for name in registry.names():
        print(f"- {name}")
    return 0


def cmd_init_samples(args: argparse.Namespace) -> int:
    target = Path(args.target).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    for sample in _sample_dir().glob("*.json"):
        shutil.copy2(sample, target / sample.name)
    print(f"已复制示例输入到：{target}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    registry = build_registry()
    context = WorkflowContext.from_output_dir(args.output)
    payload = _load_payload(args)
    result = registry.run(args.workflow, payload, context)
    _print_result(result.to_dict())
    return 0


def cmd_run_all(args: argparse.Namespace) -> int:
    registry = build_registry()
    context = WorkflowContext.from_output_dir(args.output)
    summary: dict[str, Any] = {"output_dir": str(context.output_dir), "results": []}
    for workflow in registry.names():
        payload = read_json(_sample_dir() / f"{workflow}.json")
        result = registry.run(workflow, payload, context)
        summary["results"].append(result.to_dict())
    summary_path = write_json(context.output_dir / "run_all_summary.json", summary)
    summary["summary_file"] = str(summary_path)
    _print_result(summary)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="personal-opc",
        description="年糕爸爸专属 OPC 一人公司 AI 工作流：商业、内容、信仰、亲子、学习、写作。",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="列出全部可运行工作流")
    list_parser.set_defaults(func=cmd_list)

    init_parser = sub.add_parser(
        "init-samples", help="把示例 JSON 输入复制到指定目录，便于无代码修改测试"
    )
    init_parser.add_argument(
        "--target", default=str(PACKAGE_ROOT / "my_inputs"), help="示例输入复制目录"
    )
    init_parser.set_defaults(func=cmd_init_samples)

    run_parser = sub.add_parser("run", help="运行单个工作流")
    run_parser.add_argument(
        "workflow", choices=build_registry().names(), help="工作流名称"
    )
    run_parser.add_argument("--sample", action="store_true", help="使用内置示例输入")
    run_parser.add_argument(
        "--input", help="使用自定义 JSON 输入；会覆盖示例中的同名字段"
    )
    run_parser.add_argument(
        "--output", default=str(DEFAULT_OUTPUT_DIR), help="输出目录"
    )
    run_parser.set_defaults(func=cmd_run)

    all_parser = sub.add_parser("run-all", help="用内置示例一次性运行全部工作流")
    all_parser.add_argument(
        "--output", default=str(DEFAULT_OUTPUT_DIR), help="输出目录"
    )
    all_parser.set_defaults(func=cmd_run_all)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except Exception as exc:  # CLI boundary: convert errors to actionable messages.
        print(f"错误：{exc}", file=sys.stderr)
        return 1
