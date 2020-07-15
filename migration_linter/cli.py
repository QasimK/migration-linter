"""Interface to the linter"""

import platform
import sys

import fire

from migration_linter.linter import DefaultLinter


class MigrationLinterCLI:
    """Lint SQL database migration files."""

    def stdin(self):
        """Lint SQL entered via the terminal, outputting back on to the terminal."""
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

    def files(self, *files):
        """Lint the specified file(s)."""
        for file in files:
            print(file)

    def server(self, host="localhost", port="3123"):
        """Start the Migration Linter REST server."""
        raise NotImplementedError()


def _line_num(error):
    return 0 if error.line is None else error.line


if __name__ == "__main__":
    fire.Fire(MigrationLinterCLI)
