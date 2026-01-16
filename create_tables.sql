-- SQL Script to Create Tables for Umatter Backend
-- Run this in your Render PostgreSQL SQL Editor

-- Drop existing tables if they exist (optional - comment out if you want to keep data)
-- DROP TABLE IF EXISTS wellness_metrics CASCADE;
-- DROP TABLE IF EXISTS user_table CASCADE;

-- Create user_table
CREATE TABLE IF NOT EXISTS user_table (
    userid SERIAL PRIMARY KEY
);

-- Create wellness_metrics table
CREATE TABLE IF NOT EXISTS wellness_metrics (
    id SERIAL PRIMARY KEY,
    userid INTEGER NOT NULL,
    time TIMESTAMP NOT NULL DEFAULT NOW(),
    wellness_score FLOAT NOT NULL,

    -- Foreign key constraint
    CONSTRAINT fk_user
        FOREIGN KEY (userid)
        REFERENCES user_table(userid)
        ON DELETE CASCADE,

    -- Check constraint for wellness score (0-10)
    CONSTRAINT check_wellness_score
        CHECK (wellness_score >= 0 AND wellness_score <= 10)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_wellness_metrics_userid ON wellness_metrics(userid);
CREATE INDEX IF NOT EXISTS idx_wellness_metrics_time ON wellness_metrics(time);

-- Verify tables were created
SELECT
    table_name,
    column_name,
    data_type
FROM
    information_schema.columns
WHERE
    table_name IN ('user_table', 'wellness_metrics')
ORDER BY
    table_name, ordinal_position;

-- Show table structure
\d user_table
\d wellness_metrics
