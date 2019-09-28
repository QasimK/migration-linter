import pytest

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
    def test_applies_to(self, statement, expected_is_match):
        assert AddColumnNotNullNoDefaultCheck.applies_to(statement) is expected_is_match

    def test_error(self):
        statement = "ALTER TABLE ADD COLUMN NOT NULL"
        check = AddColumnNotNullNoDefaultCheck(statement)

        error = check.error

        assert error.code == "M201"
        assert error.line == 1
