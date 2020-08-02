import subprocess
from pathlib import Path


def _file(name: str) -> Path:
    return (Path(__file__).parent / "data_main" / name).absolute()


def _sql(name: str) -> str:
    return _file(name).read_text()


def test_main_stdin_with_no_errors():
    result = subprocess.run(
        ["python", "migration_linter"],
        input=_sql("safe_migration.sql"),
        capture_output=True,
        encoding="utf-8",
        timeout=1,
    )

    assert result.returncode == 0
    assert "No errors." in result.stdout
    assert result.stderr == ""


def test_main_stdin_with_errors():
    result = subprocess.run(
        ["python", "migration_linter"],
        input=_sql("unsafe_migration.sql"),
        capture_output=True,
        encoding="utf-8",
        timeout=1,
    )

    assert result.returncode == 1
    assert "M102" in result.stdout
    assert result.stderr == ""


def test_main_files_with_no_errors():
    result = subprocess.run(
        ["python", "migration_linter", _file("safe_migration.sql")],
        capture_output=True,
        encoding="utf-8",
        timeout=1,
    )

    assert result.returncode == 0
    assert "safe_migration.sql" in result.stdout
    assert "No errors." in result.stdout
    assert result.stderr == ""


def test_main_files_with_errors():
    result = subprocess.run(
        ["python", "migration_linter", _file("unsafe_migration.sql")],
        capture_output=True,
        encoding="utf-8",
        timeout=1,
    )

    assert result.returncode == 1
    assert "M102" in result.stdout
    assert result.stderr == ""
