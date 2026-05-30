#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ARCHIVE_NAME="personal-opc-ai-workflows-$(date +%Y%m%d-%H%M%S).zip"
OUTPUT_PATH="${ROOT_DIR}/${ARCHIVE_NAME}"

cd "$ROOT_DIR"

if command -v zip >/dev/null 2>&1; then
  zip -r "$OUTPUT_PATH" . \
    -x 'opc_workflow_output/*' \
    -x 'my_inputs/*' \
    -x '.git/*' \
    -x '__pycache__/*' \
    -x '*/__pycache__/*' \
    -x '.pytest_cache/*' \
    -x '.venv/*' \
    -x 'venv/*' \
    -x '*.pyc'
else
  python - <<'PY'
from pathlib import Path
import time
import zipfile

root = Path.cwd()
archive = root / f"personal-opc-ai-workflows-{time.strftime('%Y%m%d-%H%M%S')}.zip"
exclude_parts = {'.git', '__pycache__', '.pytest_cache', '.venv', 'venv', 'opc_workflow_output', 'my_inputs'}
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as zf:
    for path in root.rglob('*'):
        if path == archive or any(part in exclude_parts for part in path.parts):
            continue
        if path.is_file() and path.suffix != '.pyc':
            zf.write(path, path.relative_to(root))
print(archive)
PY
fi

echo "Created archive: $OUTPUT_PATH"
