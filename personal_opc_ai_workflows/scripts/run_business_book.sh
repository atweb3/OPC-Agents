#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -m personal_opc_workflows run business-book --sample --output opc_workflow_output
