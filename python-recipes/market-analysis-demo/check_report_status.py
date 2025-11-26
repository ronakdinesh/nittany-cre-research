#!/usr/bin/env python3
"""
Quick script to check if a report has been completed
Usage: python check_report_status.py [industry] [geography]
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta

# Load environment variables
load_dotenv('.env.local')

DATABASE_URL = (
    os.getenv('POSTGRES_URL_NON_POOLING') or
    os.getenv('POSTGRES_URL') or 
    os.getenv('DATABASE_URL')
)

if not DATABASE_URL:
    print("❌ No database URL found. Make sure .env.local is configured.")
    sys.exit(1)

def clean_database_url(url):
    """Remove query parameters that psycopg2 doesn't support"""
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

def check_reports(industry=None, geography=None):
    """Check for completed reports matching criteria"""
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        
        # Build query based on provided criteria
        if industry and geography:
            query = '''
                SELECT task_run_id, industry, geography, status, title, slug, 
                       created_at, completed_at, 
                       CASE WHEN content IS NOT NULL THEN 'Yes' ELSE 'No' END as has_content
                FROM reports 
                WHERE industry ILIKE %s AND geography ILIKE %s
                ORDER BY created_at DESC
                LIMIT 10
            '''
            cursor.execute(query, (f'%{industry}%', f'%{geography}%'))
        elif industry:
            query = '''
                SELECT task_run_id, industry, geography, status, title, slug,
                       created_at, completed_at,
                       CASE WHEN content IS NOT NULL THEN 'Yes' ELSE 'No' END as has_content
                FROM reports 
                WHERE industry ILIKE %s
                ORDER BY created_at DESC
                LIMIT 10
            '''
            cursor.execute(query, (f'%{industry}%',))
        else:
            # Get all recent reports
            query = '''
                SELECT task_run_id, industry, geography, status, title, slug,
                       created_at, completed_at,
                       CASE WHEN content IS NOT NULL THEN 'Yes' ELSE 'No' END as has_content
                FROM reports 
                ORDER BY created_at DESC
                LIMIT 10
            '''
            cursor.execute(query)
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not results:
            print("📭 No reports found matching your criteria.")
            return
        
        print(f"\n📊 Found {len(results)} report(s):\n")
        print("-" * 100)
        
        for i, report in enumerate(results, 1):
            status_icon = "✅" if report['status'] == 'completed' else "⏳" if report['status'] == 'running' else "❌"
            print(f"{i}. {status_icon} Status: {report['status'].upper()}")
            print(f"   Industry: {report['industry']}")
            print(f"   Geography: {report['geography'] or 'Not specified'}")
            print(f"   Has Content: {report['has_content']}")
            if report['title']:
                print(f"   Title: {report['title']}")
            if report['slug']:
                print(f"   URL: /report/{report['slug']}")
            print(f"   Created: {report['created_at']}")
            if report['completed_at']:
                print(f"   Completed: {report['completed_at']}")
            print(f"   Task ID: {report['task_run_id']}")
            print("-" * 100)
        
        # Check for specifically AI + KSA reports
        ai_ksa_reports = [r for r in results if 'ai' in r['industry'].lower() and r['geography'] and 'ksa' in r['geography'].upper()]
        if ai_ksa_reports:
            print(f"\n🎯 AI + KSA Reports: {len(ai_ksa_reports)}")
            for report in ai_ksa_reports:
                if report['status'] == 'completed' and report['has_content'] == 'Yes':
                    print(f"   ✅ COMPLETED: {report['title']} - /report/{report['slug']}")
                elif report['status'] == 'running':
                    print(f"   ⏳ STILL RUNNING: {report['task_run_id']}")
        
    except Exception as e:
        print(f"❌ Error checking reports: {e}")
        sys.exit(1)

if __name__ == "__main__":
    industry = sys.argv[1] if len(sys.argv) > 1 else None
    geography = sys.argv[2] if len(sys.argv) > 2 else None
    
    if industry:
        print(f"🔍 Checking reports for Industry: '{industry}'" + (f", Geography: '{geography}'" if geography else ""))
    else:
        print("🔍 Checking all recent reports...")
    
    check_reports(industry, geography)


