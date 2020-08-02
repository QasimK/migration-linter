BEGIN;

-- Add boolean column (unsafe)
ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL;

COMMIT;
