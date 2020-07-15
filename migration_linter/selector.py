"""Selectors. Called filters due to an import problem with fire."""

from migration_linter import parser


class BaseSelector:
    SELECTOR = None
    INVERT = False

    def __init__(self, statement):
        self.statement = statement

    @property
    def is_match(self):
        result = matches_statement(self.SELECTOR, self.statement)
        if self.INVERT:
            result = not result
        return result


def matches_statement(selector, statement):
    """Selectors are a simple list with a possible wildcard * in between words."""
    selector = selector[:]

    tokens = parser.parse_statement(statement)
    if not tokens:
        return False

    tokens = list(tokens[0].flatten())
    while selector and tokens:
        if tokens[0].is_whitespace:
            tokens = tokens[1:]
        elif (
            selector[0] == "*"
            and tokens[0].value.strip().upper() != selector[1].strip().upper()
        ):
            tokens = tokens[1:]
        elif (
            selector[0] == "*"
            and tokens[0].value.strip().upper() == selector[1].strip().upper()
        ):
            selector = selector[1:]
        elif tokens[0].value.strip().upper() == selector[0].strip().upper():
            selector = selector[1:]
            tokens = tokens[1:]
        else:
            return False

    return not bool(selector)


class AddColumnSelector(BaseSelector):
    SELECTOR = ("ALTER", "TABLE", "*", "ADD", "COLUMN")


class NotNullSelector(BaseSelector):
    SELECTOR = ("*", "NOT NULL")


class NoDefaultValueSelector(BaseSelector):
    SELECTOR = ("*", "DEFAULT")
    INVERT = True


class CreateIndexSelector(BaseSelector):
    SELECTOR = ("CREATE", "INDEX")


class NotConcurrentlySelector(BaseSelector):
    SELECTOR = ("*", "CONCURRENTLY")
    INVERT = True


class NoStatementTimeoutSelector(BaseSelector):
    SELECTOR = ("SET", "LOCAL", "statement_timeout")
    INVERT = True
