from typing import List

from migration_linter import parser
from migration_linter.checks.base import MigrationError
from migration_linter.checks.defaults import DEFAULT_CHECKS


class Linter:
    """Basic interface to find and check given errors."""

    def __init__(self, check_list=None):
        self.check_list = check_list or []

    def check_sql(self, sql: str) -> List[MigrationError]:
        """Return all errors found."""
        parsed = []
        for statement in parser.split_sql(sql):
            tokens = parser.parse_statement(statement)
            parsed.append((statement, tokens))

        errors = []
        for check in self.check_list:
            errors.extend(check.errors(parsed))

        return errors


class DefaultLinter(Linter):
    """The interface using the default set of errors."""

    def __init__(self):
        super().__init__(check_list=DEFAULT_CHECKS)
