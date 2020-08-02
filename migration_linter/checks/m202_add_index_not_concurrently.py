from migration_linter.checks.base import StatementCheck
from migration_linter.selector import CreateIndexSelector
from migration_linter.selector import NotConcurrentlySelector


class CreateIndexNotConcurrentlyCheck(StatementCheck):
    """Verify new columns will not result in a table re-write."""

    NAME = "add-index-not-concurrently"
    CODE = "M202"
    EXPLANATION = """
        Adding a new index locks the table, preventing writes including inserts,
        updates, and deletes. (TBD: exact lock.)

        This can be resolved by adding a new index concurrently:

            CREATE INDEX CONCURRENTLY my_column_idx ON my_table (my_column);
    """

    _SELECTORS = [CreateIndexSelector, NotConcurrentlySelector]
