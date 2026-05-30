# Contributing

This repository is intentionally small and MVP-oriented. Contributions should keep the workflows easy to run without paid APIs or external services.

## Local checks

```bash
python -m pip install -e .
python -m personal_opc_workflows run-all --output /tmp/personal_opc_check
PYTHONPATH=. pytest tests -q
python -m compileall personal_opc_workflows
```

## Style

- Use Python 3.10+ syntax.
- Prefer standard library modules unless a dependency is clearly worth the setup cost.
- Keep workflow outputs deterministic by default; optional LLM integrations should have a local fallback.
- Do not commit private inputs, `.env`, `my_inputs/`, or generated `opc_workflow_output/` files.

## Adding a workflow

1. Add a module under `personal_opc_workflows/workflows/`.
2. Expose a `run(payload: dict, context: WorkflowContext) -> WorkflowResult` function.
3. Register it in `personal_opc_workflows/registry.py`.
4. Add a sample JSON under both `data/samples/` and `personal_opc_workflows/data/samples/`.
5. Document the command in `README.md`.
6. Add or update tests.
