#!/usr/bin/env python3
"""
Check email status for a specific task
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv('.env.local')

DATABASE_URL = (
    os.getenv('POSTGRES_URL_NON_POOLING') or
    os.getenv('POSTGRES_URL') or 
    os.getenv('DATABASE_URL')
)

if not DATABASE_URL:
    print("❌ No database URL found.")
    sys.exit(1)

def clean_database_url(url):
    if '?' in url:
        base_url, query_string = url.split('?', 1)
        import urllib.parse
        params = urllib.parse.parse_qs(query_string)
        supported_params = ['sslmode', 'connect_timeout', 'application_name']
        clean_params = {k: v for k, v in params.items() if k in supported_params}
        if clean_params:
            clean_query = urllib.parse.urlencode(clean_params, doseq=True)
            return f"{base_url}?{clean_query}"
        else:
            return base_url
    return url

DATABASE_URL = clean_database_url(DATABASE_URL)

task_id = sys.argv[1] if len(sys.argv) > 1 else "trun_73f9127b31ef452585e7850813e2f5ea"

try:
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT task_run_id, industry, geography, email, status, title, slug, completed_at
        FROM reports 
        WHERE task_run_id = %s
    ''', (task_id,))
    
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not result:
        print(f"❌ Task {task_id} not found")
        sys.exit(1)
    
    print(f"\n📧 Email Status for Task: {task_id}\n")
    print("-" * 80)
    print(f"Industry: {result['industry']}")
    print(f"Geography: {result['geography']}")
    print(f"Status: {result['status']}")
    print(f"Email: {result['email'] or '❌ NOT PROVIDED'}")
    print(f"Title: {result['title']}")
    print(f"Slug: {result['slug']}")
    print(f"Completed: {result['completed_at']}")
    print("-" * 80)
    
    # Check RESEND_API_KEY
    resend_key = os.getenv('RESEND_API_KEY')
    print(f"\n🔑 RESEND_API_KEY: {'✅ Configured' if resend_key else '❌ NOT CONFIGURED'}")
    
    if not result['email']:
        print("\n⚠️  No email was stored for this task. Email notifications require an email address.")
    elif not resend_key:
        print("\n⚠️  RESEND_API_KEY is not configured. Email sending is disabled.")
    else:
        print(f"\n✅ Email should have been sent to: {result['email']}")
        print("   Check your spam folder or check server logs for email sending errors.")
        
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)


