# Security and privacy

This MVP stores generated files locally and does not call external APIs by default.

## Do not commit private data

The following paths are ignored and should stay local:

- `.env`
- `my_inputs/`
- `opc_workflow_output/`
- virtual environments and caches

## Sensitive workflow areas

- Business visit notes may include company names, quotes, photos, and non-public context. Review before publishing.
- Family logs may include child-related personal details. Keep them private unless deliberately edited for public sharing.
- Faith study notes may include copyrighted Bible quotations. Keep quotes short and verify permission requirements.

## Reporting issues

For a private personal repo, open a private issue or fix directly. For a public fork, avoid posting secrets or private family/business details in issues.
