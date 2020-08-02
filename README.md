# Migration Linter

Check whether migrations will cause an outage.

## Usage

* M1xx = Global errors
    * M101 - Missing lock timeout
    * M102 - Missing statement timeout
* M2xx = Statement errors
    * M201 - Add NOT-NULL column with default (Earlier than Postgres 11 only)
        * Causes full-table rewrite to retrospectively apply default to all rows
    * M202 - Set column value on all rows
    * M203 - Add NOT-NULL column with no default value
    * M204 - Add index not concurrently
    * M205 - Add unique index constraint not concurrently
    * M206 - Dropping NOT-NULL column
    * M207 - Alter column type
        * Known safe exceptions:
            * varchar less -> more
            * (var)char -> TEXT
            * numeric(less, same) -> numeric(more, same)
    * M221 - Alter Table Rename to, Set tablespace
* M3xx = Warnings
    * M301 - No index on ForeignKey
    * M302 - Drop column does not reclaim space until "VACUUM FULL" is run


## Development

1. `poetry install` to set up the virtualenv (one-off)
2. `make fix`, `make check`, and `make test` while coding
3. `make all` before committing (uses tox to test for Python 3.7+)

### Contributing

Pull requests are welcome :)

### Publishing

This project is not published yet.

## Changelog

This project is experimental.
