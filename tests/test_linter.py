import pytest

from migration_linter.linter import DefaultLinter

EXAMPLE_GOOD = """
SET LOCAL statement_timeout = 5;
ALTER TABLE table ADD COLUMN column;
"""

EXAMPLE_VERY_BAD = """
ALTER TABLE table ADD COLUMN column NOT NULL;
"""


class TestDefaultLinter:
    @pytest.fixture(autouse=True)
    def setup_linter(self):
        self.linter = DefaultLinter()

    def test_check_sql(self):
        result = self.linter.check_sql(EXAMPLE_GOOD)
        assert len(result) == 0

    def test_check_sql_with_errors(self):
        result = self.linter.check_sql(EXAMPLE_VERY_BAD)
        assert len(result) == 2
