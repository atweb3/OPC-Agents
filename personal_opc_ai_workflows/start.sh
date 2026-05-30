#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python -m personal_opc_workflows run-all --output opc_workflow_output
printf '\n✅ 全部示例工作流已运行。请查看：%s\n' "$(pwd)/opc_workflow_output"
