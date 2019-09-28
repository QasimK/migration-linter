import pytest

from migration_linter.filters.base import (
    AddColumnSelector,
    NotNullSelector,
    NoDefaultValueSelector,
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
    def test_selector(self, statement, expected_is_match):
        assert AddColumnSelector(statement).is_match is expected_is_match


class TestNotNullSelector:
    @pytest.mark.parametrize(
        "statement, expected_is_match",
        [
            ("ALTER TABLE tab ADD COLUMN col NOT NULL", True),
            ("ALTER TABLE tab ADD COLUMN col NOT NULLABLE", False),
        ],
    )
    def test_is_match(self, statement, expected_is_match):
        assert NotNullSelector(statement).is_match is expected_is_match


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
        assert NoDefaultValueSelector(statement).is_match is expected_is_match
