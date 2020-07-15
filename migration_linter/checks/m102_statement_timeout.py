from typing import List

from migration_linter.checks.base import Check, MigrationError
from migration_linter.selector import StatementTimeoutSelector


class StatementTimeoutMissingCheck(Check):
    NAME = "statement-timeout-missing"
    CODE = "M102"
    EXPLANATION = """
        There is no global statement timeout set, so certain commands may take
        a long time, causing other queries to block.

        For example:

        TODO: This example is wrong - it applies to lock_timeout.

        READ ... ... ... ... (APP - LONG QUERY TAKING ITS TIME)
            ALTER TABLE  ... (MIGRATION - BLOCKED ON READ)
                READ ... ... (APP - NOW BLOCKED ON ALTER)

        Normally the second READ would execute concurrently with the first.

        A statement timeout will cancel the migration, causing it to rollback,
        and allowing the application to continue to use the database. This
        prevents the application from going down because its access to the
        database is blocked.

        A read requires an ACCESS SHARE lock. The ALTER TABLE requires an
        ACCESS EXCLUSIVE lock. Therefore the migration is blocked while waiting
        to acquire the lock.

        This can be resolved by:

            * Adding `SET LOCAL statement_timeout = '5s';` to the top of the
              migration, or
            * Setting a session statement timeout on the migration's database
              connection. (TODO: how?)

        TODO: The documentation should contain a recipe book.

        Consider setting this for all app queries as well.
    """

    @classmethod
    def errors(cls, parsed_sql) -> List[MigrationError]:
        for statement, tokens in parsed_sql:
            if StatementTimeoutSelector.is_match(tokens):
                return []

        return [cls._create_error()]
