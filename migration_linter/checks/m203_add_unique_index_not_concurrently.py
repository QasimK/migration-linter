"""
Bad:

CREATE UNIQUE INDEX token_uniq_idx ON large_table (token);

Good:

CREATE UNIQUE INDEX CONCURRENTLY token_uniq_idx ON large_table (token);
ALTER TABLE large_table ADD CONSTRAINT token UNIQUE USING INDEX token_uniq_idx;
"""

from migration_linter import selector
from migration_linter.checks.base import StatementCheck


class CreateUniqueIndexNotConcurrentlyCheck(StatementCheck):

    NAME = "add-unique-index-not-concurrently"
    CODE = "M203"
    EXPLANATION = """
        Adding a new index locks the table, preventing writes including inserts,
        updates, and deletes. (TBD: exact lock.)

        A typical unique index is added like:

            CREATE UNIQUE INDEX token_uniq_idx ON large_table (token);

        This can be resolved by adding a new unique index concurrently, and then
        applying the unique constraint to the column.

            CREATE UNIQUE INDEX CONCURRENTLY token_uniq_idx ON large_table (token);
            ALTER TABLE large_table ADD CONSTRAINT token UNIQUE USING INDEX token_uniq_idx;
    """

    _SELECTORS = [selector.CreateUniqueIndexSelector, selector.NotConcurrentlySelector]
