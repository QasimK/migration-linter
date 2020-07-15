from migration_linter.checks.base import BaseCheck
from migration_linter.selector import (
    AddColumnSelector,
    NotNullSelector,
    NoDefaultValueSelector,
)


class AddColumnNotNullNoDefaultCheck(BaseCheck):
    """Verify new columns will not result in a table re-write."""

    SELECTORS = [AddColumnSelector, NotNullSelector, NoDefaultValueSelector]

    NAME = "add-column-not-null-no-default"
    CODE = "M201"
    EXPLANATION = """
        Adding a new non-nullable column can cause INSERT statements from
        currently-running code to fail.

        Currently-running code will not provide a value for the new column,
        raising an exception.

        This can be resolved by:

            * Adding NOT NULL to the statement, or
            * Adding a default value for the column.

        Please note, that you can only add a default value for Postgres 10.0+
        otherwise, you will have issue default-value-table-rewrite (M002).

        TODO: settings to specify dialect.
    """
