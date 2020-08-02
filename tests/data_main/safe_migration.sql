BEGIN;

SET LOCAL lock_timeout = '2s';
SET LOCAL statement_timeout = '3s';

-- Add boolean column
ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT FALSE;

COMMIT;
