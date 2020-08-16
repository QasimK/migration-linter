"""Command Line Interface."""

import platform

import click

from migration_linter import types
from migration_linter.linter import DefaultLinter


@click.command()
@click.argument("files", type=click.File(), nargs=-1)
def main(files):
    """Check SQL migrations for common problems that can cause downtime.

    FILES are paths to specific SQL files, or from standard input using a
    hyphen "-". For example:

    \b
        migration-linter -
        migration-linter migration-1.sql
        migration-linter migration-1.sql - migration-3.sql
    """
    if not files:
        click.echo(click.get_current_context().get_help())
        return

    linter = DefaultLinter()
    is_any_error = False
    for file in files:
        _show_filename(file)
        source = types.Source(filename=file.name, sql=file.read())
        errors = linter.check_sql(source)
        errors = sorted(errors, key=_line_num)
        is_any_error |= bool(errors)

        click.echo("")
        for error in errors:
            click.echo(f"Error: {error.name} ({error.code})")

        if not errors:
            click.echo("No errors.")

    if is_any_error:
        click.get_current_context().exit(1)


def _show_filename(file: click.File):
    if file.isatty():
        text = _user_input_help()
    else:
        text = file.name

    click.echo(text)


def _user_input_help():
    stop_cmd = "<CTRL>-<D>"
    if platform.system() == "Windows":
        stop_cmd = "<CTRL>-<Z> <Return>"

    return f"Enter SQL ({stop_cmd} to finish entering SQL):"


def _line_num(error):
    return 0 if error.line is None else error.line


if __name__ == "__main__":
    main()
