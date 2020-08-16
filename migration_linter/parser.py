import sqlparse

from migration_linter import types


def parse_statement(statement):
    return sqlparse.parse(statement)


def parse_statements(sql):
    for statement in split_sql(sql):
        yield parse_statement(statement)


def split_sql(source: types.Source):
    return sqlparse.split(source.sql)
