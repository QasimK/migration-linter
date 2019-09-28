import pytest

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
    def test_applies_to(self, statement, expected_is_match):
        assert (
            CreateIndexNotConcurrentlyCheck.applies_to(statement) is expected_is_match
        )

    def test_error(self):
        statement = "CREATE INDEX column_idx ON table (column)"
        check = CreateIndexNotConcurrentlyCheck(statement)

        error = check.error

        assert error.code == "M202"
        assert error.line == 1
