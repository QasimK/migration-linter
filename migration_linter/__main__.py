"""Command Line Interface."""

import platform
import sys
from pathlib import Path
from typing import List

import fire

from migration_linter.linter import DefaultLinter


def main(*files):
    """Check SQL migrations for common problems that can cause downtime

    If no arguments are provided, then you can directly type (or copy-and-paste)
    the SQL you wish to check.

        migration-linter

    Any arguments given should be paths to specific SQL files that you wish to
    check.

        migration-linter migration-1.sql migration-2.sql
    """
    # Fire does not support '-' as a command-line argument (2017-03-09)
    # https://github.com/google/python-fire/issues/15
    # So we use blank arguments to mean stdin
    if files:
        lint_files(*files)
    else:
        stdin()


def stdin():
    """Lint SQL entered via the terminal, outputting back on to the terminal."""
    print("(Use the --help flag for help on using this tool.)")
    stop_cmd = "<CTRL>-<D>"
    if platform.system() == "Windows":
        stop_cmd = "<CTRL>-<Z> <Return>"

    print(f"Enter SQL ({stop_cmd} to finish entering SQL):")
    sql = ""
    try:
        while True:
            sql += input() + "\n"
    except EOFError:
        pass

    linter = DefaultLinter()
    errors = linter.check_sql(sql)
    is_any_error = bool(errors)
    sorted_errors = sorted(errors, key=_line_num)

    print("")

    for error in sorted_errors:
        print(f"Error: {error.name} ({error.code})")
        # TODO: Optional verbose output of explanation

    if is_any_error:
        sys.exit(1)
    else:
        print("No errors.")


def lint_files(*files: List[str]):
    """Lint the specified file(s)."""
    paths = [Path(file) for file in files]
    linter = DefaultLinter()
    is_any_error = False

    for path in paths:
        print(str(path))
        errors = linter.check_sql(path.read_text())
        is_any_error = is_any_error or bool(errors)
        sorted_errors = sorted(errors, key=_line_num)

        print("")
        for error in sorted_errors:
            print(f"Error: {error.name} ({error.code})")

        if not errors:
            print("No errors.")

    if is_any_error:
        sys.exit(1)


def _line_num(error):
    return 0 if error.line is None else error.line


if __name__ == "__main__":
    fire.Fire(main, name="migration-linter")
