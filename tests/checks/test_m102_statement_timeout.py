import pytest

from migration_linter import parser
from migration_linter.checks.m102_statement_timeout import StatementTimeoutMissingCheck


class TestStatementTimeoutMissingCheck:
    @pytest.mark.parametrize(
        "statement, expected_num_errors",
        [
            ("SET LOCAL statement_timeout = 6", 0),  # TODO: match on number
            ("SET LOCAL statement_timeout = 5", 0),
            ("ALTER TABLE table ADD COLUMN column", 1),
        ],
    )
    def test_errors(self, statement, expected_num_errors):
        tokens = parser.parse_statement(statement)
        parsed_sql = [(statement, tokens)]

        result = StatementTimeoutMissingCheck.errors(parsed_sql)

        assert len(result) == expected_num_errors
