import pytest

from migration_linter import parser
from migration_linter.selector import (
    AddColumnSelector,
    NoDefaultValueSelector,
    NotNullSelector,
)


class TestAddColumnSelector:
    @pytest.mark.parametrize(
        "statement, expected_is_match",
        [
            ("ALTER TABLE ADD COLUMN", True),
            ("ALTER tab ADD COLUMN", False),
            ("ALTER TABLE COLUMN col", False),
        ],
    )
    def test_is_match(self, statement, expected_is_match):
        tokens = parser.parse_statement(statement)
        assert AddColumnSelector.is_match(tokens) is expected_is_match


class TestNotNullSelector:
    @pytest.mark.parametrize(
        "statement, expected_is_match",
        [
            ("ALTER TABLE tab ADD COLUMN col NOT NULL", True),
            ("ALTER TABLE tab ADD COLUMN col NOT NULLABLE", False),
        ],
    )
    def test_is_match(self, statement, expected_is_match):
        tokens = parser.parse_statement(statement)
        assert NotNullSelector.is_match(tokens) is expected_is_match


class TestNoDefaultValueSelector:
    @pytest.mark.parametrize(
        "statement, expected_is_match",
        [
            ("ALTER TABLE tab ADD COLUMN col", True),
            ("ALTER TABLE tab ADD COLUMN col DEFAULT", False),
            ("ALTER TABLE tab ADD COLUMN col DEFAULT 1", False),
            ("ALTER TABLE tab ADD COLUMN col DEFAULT NOT NULL", False),
        ],
    )
    def test_is_match(self, statement, expected_is_match):
        tokens = parser.parse_statement(statement)
        assert NoDefaultValueSelector.is_match(tokens) is expected_is_match
