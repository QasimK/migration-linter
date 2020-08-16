from __future__ import annotations

from typing import List
from typing import Optional

from migration_linter import types


class Check:
    NAME = None
    CODE = None
    EXPLANATION = None

    @classmethod
    def errors(cls, parsed_sql) -> List[types.MigrationError]:
        raise NotImplementedError()

    @classmethod
    def _create_error(cls, line: Optional[int] = None) -> types.MigrationError:
        return types.MigrationError(
            name=cls.NAME, code=cls.CODE, explanation=cls.EXPLANATION, line=line
        )


class StatementCheck(Check):
    """Check an individual statement."""

    _SELECTORS = None

    @classmethod
    def errors(cls, parsed_sql) -> List[types.MigrationError]:
        errors = []
        for line, (statement, tokens) in enumerate(parsed_sql, start=1):
            if cls.is_applicable(tokens):
                errors.append(cls._create_error(line))

        return errors

    @classmethod
    def is_applicable(cls, tokens) -> bool:
        """Return whether this check applies to the given ."""
        return all(selector.is_match(tokens) for selector in cls._SELECTORS)
