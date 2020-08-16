from hypothesis import strategies as st

from migration_linter import types

GOOD_REQUIRED_STATEMENTS = [
    "SET LOCAL statement_timeout = 5000;",
    "SET LOCAL lock_timeout = 3000;",
]

GOOD_STATEMENTS = [
    "ALTER TABLE my_table ADD COLUMN my_column BOOLEAN;",
    "CREATE INDEX CONCURRENTLY my_column_idx ON my_table (my_column);",
]

BAD_STATEMENTS = ["ALTER TABLE my_table ADD COLUMN my_column NOT NULL;"]


def _add_required_statements(optional_statements):
    return GOOD_REQUIRED_STATEMENTS + optional_statements


def _sql_list_to_string(statements_list):
    return "\n".join(statements_list)


good_sql = (
    st.lists(st.sampled_from(GOOD_STATEMENTS))
    .map(_add_required_statements)
    .map(_sql_list_to_string)
)

bad_sql = st.lists(st.sampled_from(BAD_STATEMENTS)).map(_sql_list_to_string)

good_source = st.builds(types.Source, sql=good_sql)
bad_source = st.builds(types.Source, sql=bad_sql)
