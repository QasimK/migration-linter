import pytest

from migration_linter import parser
from migration_linter.checks.m202_add_index_not_concurrently import (
    CreateIndexNotConcurrentlyCheck,
)


class TestCreateIndexNotConcurrentlyCheckCheck:
    @pytest.mark.parametrize(
        "statement, expected_is_match",
        [
            ("CREATE INDEX column_idx ON table (column)", True),
            ("CREATE INDEX CONCURRENTLY column_idx ON table (column)", False),
        ],
    )
    def test_is_applicable(self, statement, expected_is_match):
        tokens = parser.parse_statement(statement)
        assert (
            CreateIndexNotConcurrentlyCheck.is_applicable(tokens) is expected_is_match
        )

    def test_errors(self):
        statement = "CREATE INDEX column_idx ON table (column)"
        tokens = parser.parse_statement(statement)
        parsed_sql = [(statement, tokens)]

        [error] = CreateIndexNotConcurrentlyCheck.errors(parsed_sql)

        assert error.code == "M202"
        assert error.line == 1
