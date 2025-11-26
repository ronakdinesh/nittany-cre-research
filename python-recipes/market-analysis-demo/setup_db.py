#!/usr/bin/env python3
"""
Script to set up database tables for Market Analysis Demo
"""
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

DATABASE_URL = os.getenv('POSTGRES_URL_NON_POOLING')

if not DATABASE_URL:
    raise ValueError("POSTGRES_URL_NON_POOLING not found in environment variables")

# SQL to create tables
SQL = """
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
"""

def setup_database():
    """Create database tables"""
    try:
        print("Connecting to database...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("Creating tables and indexes...")
        cursor.execute(SQL)
        
        conn.commit()
        print("✅ Database tables created successfully!")
        
        # Verify tables were created
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('reports', 'rate_limit')
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print("\n✅ Verified tables exist:")
        for table in tables:
            print(f"   - {table[0]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        raise

if __name__ == '__main__':
    setup_database()


