-- Database setup SQL for Market Analysis Demo
-- Run this in Supabase SQL Editor

-- Reports table (stores both running tasks and completed reports)
CREATE TABLE IF NOT EXISTS reports (
    id VARCHAR PRIMARY KEY,
    task_run_id VARCHAR UNIQUE NOT NULL,
    title VARCHAR,
    slug VARCHAR UNIQUE,
    industry VARCHAR NOT NULL,
    geography VARCHAR,
    details TEXT,
    content TEXT,
    basis JSONB,
    status VARCHAR DEFAULT 'running',
    session_id VARCHAR,
    email VARCHAR,
    is_public BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Rate limit table (for global rate limiting)
CREATE TABLE IF NOT EXISTS rate_limit (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_reports_status ON reports(status);
CREATE INDEX IF NOT EXISTS idx_reports_slug ON reports(slug);
CREATE INDEX IF NOT EXISTS idx_reports_task_run_id ON reports(task_run_id);
CREATE INDEX IF NOT EXISTS idx_rate_limit_created_at ON rate_limit(created_at);

