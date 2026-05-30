from pathlib import Path

from personal_opc_workflows.cli import main


def test_run_all_generates_summary(tmp_path: Path):
    exit_code = main(["run-all", "--output", str(tmp_path)])
    assert exit_code == 0
    assert (tmp_path / "run_all_summary.json").exists()
    assert any((tmp_path / "business_book").glob("*.html"))


def test_single_faith_workflow_generates_warning(tmp_path: Path, capsys):
    exit_code = main(["run", "faith-study", "--sample", "--output", str(tmp_path)])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "NIV" in captured.out
    assert any((tmp_path / "faith").glob("*.md"))
