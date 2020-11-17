import pytest

from migration_linter import parser
from migration_linter.checks.m201_add_column_not_null_no_default import (
    AddColumnNotNullNoDefaultCheck,
)


class TestAddColumnNotNullNoDefaultCheck:
    @pytest.mark.parametrize(
        "statement, expected_is_match",
        [
            ("ALTER TABLE table ADD COLUMN col NOT NULL", True),
            ("ALTER TABLE table ADD COLUMN col", False),
            ("ALTER TABLE table ADD COLUMN col NOT NULL DEFAULT 1", False),
        ],
    )
    def test_is_applicable(self, statement, expected_is_match):
        tokens = parser.parse_statement(statement)
        assert AddColumnNotNullNoDefaultCheck.is_applicable(tokens) is expected_is_match

    def test_errors(self):
        statement = "ALTER TABLE ADD COLUMN NOT NULL"
        tokens = parser.parse_statement(statement)
        parsed_sql = [(statement, tokens)]

        [error] = AddColumnNotNullNoDefaultCheck.errors(parsed_sql)

        assert error.code == "M201"
        assert error.line == 1
