from migration_linter.checks.base import GlobalCheck
from migration_linter.selector import NoStatementTimeoutSelector


class StatementTimeoutMissingCheck(GlobalCheck):
    NAME = "statement-timeout-missing"
    CODE = "M102"
    EXPLANATION = """
        There is no global statement timeout set, so certain commands may take
        a long time, causing other queries to block.

        For example.

        READ READ READ (CODE - TAKING ITS TIME)
            ALTER TABLE (MIGRATION - BLOCKED ON READS)
                READ (CODE - NOW BLOCKED ON ALTER)

        A statement timeout will cancel the migration, causing it to rollback,
        and allowing the application to continue to use the database. This
        prevents the application from going down due to its access to the DB
        being blocked.

        This can be resolved by:

            * Adding `SET LOCAL statement_timeout = '5s';` to the top of the
              migration, or
            * Setting a global statement timeout on the migration's database
              connection. (TODO: how?)

        TODO: The documentation should contain a recipe book.
    """

    @property
    def is_error(self):
        return all(
            NoStatementTimeoutSelector(statement).is_match
            for statement in self.statements
        )
