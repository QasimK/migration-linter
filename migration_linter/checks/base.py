from __future__ import annotations

from typing import List, Optional


class Check:
    NAME = None
    CODE = None
    EXPLANATION = None

    @classmethod
    def errors(cls, parsed_sql) -> List[MigrationError]:
        raise NotImplementedError()

    @classmethod
    def _create_error(cls, line: Optional[int] = None) -> MigrationError:
        return MigrationError(
            name=cls.NAME, code=cls.CODE, explanation=cls.EXPLANATION, line=line
        )


class StatementCheck(Check):
    """Check an individual statement."""

    _SELECTORS = None

    @classmethod
    def errors(cls, parsed_sql) -> List[MigrationError]:
        errors = []
        for line, (statement, tokens) in enumerate(parsed_sql, start=1):
            if cls.is_applicable(tokens):
                errors.append(cls._create_error(line))

        return errors

    @classmethod
    def is_applicable(cls, tokens) -> bool:
        """Return whether this check applies to the given ."""
        return all(selector.is_match(tokens) for selector in cls._SELECTORS)


class MigrationError:
    """An error can apply to a specific line, or globally."""

    def __init__(self, name, code, explanation, line=None):
        self.name = name
        self.code = code
        self.explanation = explanation
        self.line = line

    def __repr__(self):
        return f"<MigrationError(name={self.name}, code={self.code})>"
