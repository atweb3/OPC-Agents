# GitHub repository setup guide

This guide turns this MVP workflow kit into a real GitHub repository under your account.

## 1. Create an empty GitHub repository

1. Open <https://github.com/new>.
2. Repository name: `personal-opc-ai-workflows`.
3. Visibility: start with **Private** if your future inputs may include business, family, or faith notes.
4. Do **not** add a README, `.gitignore`, or license on GitHub; this project already includes them.
5. Click **Create repository**.

## 2. Push from your computer

From the standalone project directory:

```bash
git init
git add .
git commit -m "Initial commit: personal OPC AI workflows"
git branch -M main
git remote add origin https://github.com/YOUR_NAME/personal-opc-ai-workflows.git
git push -u origin main
```

Replace `YOUR_NAME` with your GitHub user name.

## 3. Verify the repository page

After pushing, confirm GitHub shows:

- `README.md`
- `pyproject.toml`
- `personal_opc_workflows/`
- `data/samples/`
- `.github/workflows/ci.yml`
- `LICENSE`

Generated outputs should **not** be present:

- `opc_workflow_output/`
- `my_inputs/`
- `.env`

They are ignored by `.gitignore`.

## 4. Run it after cloning

```bash
git clone https://github.com/YOUR_NAME/personal-opc-ai-workflows.git
cd personal-opc-ai-workflows
python -m pip install -e .
python -m personal_opc_workflows run-all
```

## 5. Optional GitHub CLI path

If you use the GitHub CLI:

```bash
gh auth login
gh repo create personal-opc-ai-workflows --private --source=. --remote=origin --push
```
