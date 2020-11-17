import pytest

from migration_linter import parser
from migration_linter.checks.m203_add_unique_index_not_concurrently import (
    CreateUniqueIndexNotConcurrentlyCheck,
)


class TestCreateIndexNotConcurrentlyCheckCheck:
    @pytest.mark.parametrize(
        "statement, expected_is_match",
        [
            ("CREATE UNIQUE INDEX column_idx ON table (column)", True),
            ("CREATE UNIQUE INDEX CONCURRENTLY column_idx ON table (column)", False),
            ("CREATE INDEX column_idx ON table (column)", False),
        ],
    )
    def test_is_applicable(self, statement, expected_is_match):
        tokens = parser.parse_statement(statement)
        assert (
            CreateUniqueIndexNotConcurrentlyCheck.is_applicable(tokens)
            is expected_is_match
        )

    def test_errors(self):
        statement = "CREATE UNIQUE INDEX column_idx ON table (column)"
        tokens = parser.parse_statement(statement)
        parsed_sql = [(statement, tokens)]

        [error] = CreateUniqueIndexNotConcurrentlyCheck.errors(parsed_sql)

        assert error.code == "M203"
        assert error.line == 1
