from typing import List

from migration_linter.parser import split_sql
from migration_linter.checks.base import MigrationError, DEFAULT_CHECKS


def register_default_checks():
    import migration_linter.checks.m201_add_column_not_null_no_default  # noqa


class Linter:
    """Basic interface to find and check given errors."""

    def __init__(self, check_list=None):
        self.check_list = check_list or []

    def check_sql(self, sql) -> List[MigrationError]:
        """Return all errors found."""
        errors = []
        for statement in split_sql(sql):
            errors.extend(list(self.check_statement(statement)))

        return errors

    def check_statement(self, statement):
        checks = (check_cls.build_check(statement) for check_cls in self.check_list)
        errors = (check.error for check in checks if check and check.error)
        return errors


class DefaultLinter(Linter):
    """The interface using the default set of errors."""

    def __init__(self):
        super().__init__()
        register_default_checks()
        self.check_list.extend(DEFAULT_CHECKS)
