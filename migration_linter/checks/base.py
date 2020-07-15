class BaseCheck:
    SELECTORS = None
    NAME = None
    CODE = None
    EXPLANATION = None

    @classmethod
    def build_check(cls, statement):
        """Return the check, or None, for the given statement."""
        if cls.applies_to(statement):
            return cls(statement)

    @classmethod
    def applies_to(cls, statement):
        """Return whether this check applies to the given statement."""
        return all(selector.is_match for selector in cls._get_selectors(statement))

    def __init__(self, statement):
        self.statement = statement

    @property
    def error(self):
        return MigrationError(
            name=self.NAME, code=self.CODE, explanation=self.EXPLANATION, line=1
        )

    @classmethod
    def _get_selectors(cls, statement):
        return (selector_cls(statement) for selector_cls in cls.SELECTORS)


class StatementCheck(BaseCheck):
    """Check an individual statement."""


# TODO: This
# How does this work?
# Needs all the statements
# Can run its own selectors and stuff
# Quite bespoke logic
# error will give the error IF any
# rename to get_error
# build_check does nothing.
class GlobalCheck:
    NAME = None
    CODE = None
    EXPLANATION = None

    def __init__(self, statements):
        self.statements = statements

    @property
    def is_error(self):
        raise NotImplementedError()

    @property
    def error(self):
        if self.is_error:
            return MigrationError(
                name=self.NAME, code=self.CODE, explanation=self.EXPLANATION
            )


class MigrationError:
    """An error can apply to a specific line, or globally."""

    def __init__(self, name, code, explanation, line=None):
        self.name = name
        self.code = code
        self.explanation = explanation
        self.line = line
