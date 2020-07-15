"""
Bad:

CREATE UNIQUE INDEX token_uniq_idx ON large_table (token);

Good:

CREATE UNIQUE INDEX CONCURRENTLY token_uniq_idx ON large_table (token);
ALTER TABLE large_table ADD CONSTRAINT token UNIQUE USING INDEX token_uniq_idx;
"""
