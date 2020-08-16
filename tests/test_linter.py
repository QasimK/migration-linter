import hypothesis
import pytest

from migration_linter.linter import DefaultLinter
from tests import factories


class TestDefaultLinter:
    @pytest.fixture(autouse=True)
    def setup_linter(self):
        self.linter = DefaultLinter()

    @hypothesis.given(factories.good_source)
    def test_check_sql(self, good_source):
        result = self.linter.check_sql(good_source)
        assert len(result) == 0

    @hypothesis.given(factories.bad_source)
    def test_check_sql_with_errors(self, bad_source):
        result = self.linter.check_sql(bad_source)
        assert len(result) > 0
