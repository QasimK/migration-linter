import sqlparse


def parse_statement(statement):
    return sqlparse.parse(statement)


def parse_statements(sql):
    for statement in split_sql(sql):
        yield parse_statement(statement)


def split_sql(sql):
    return sqlparse.split(sql)
