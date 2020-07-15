from migration_linter.checks import (
    m102_statement_timeout,
    m201_add_column_not_null_no_default,
    m202_add_index_not_concurrently,
)

DEFAULT_CHECKS = [
    # m101_lock_timeout.
    m102_statement_timeout.StatementTimeoutMissingCheck,
    m201_add_column_not_null_no_default.AddColumnNotNullNoDefaultCheck,
    m202_add_index_not_concurrently.CreateIndexNotConcurrentlyCheck,
]
