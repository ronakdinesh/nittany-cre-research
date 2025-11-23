#!/usr/bin/env python3
"""
Send a test email to verify email delivery
Usage: python send_test_email.py [email_address]
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv('.env.local')

RESEND_API_KEY = os.getenv('RESEND_API_KEY')
BASE_URL = os.getenv('BASE_URL', 'https://aimarketresearch.app')

# Get email from command line or use default
email = sys.argv[1] if len(sys.argv) > 1 else 'ronakhq@gmail.com'

if not RESEND_API_KEY:
    print("❌ RESEND_API_KEY not configured")
    sys.exit(1)

print(f"📧 Sending test email to: {email}")
print("-" * 80)

# Use Resend's test domain
from_domain = "onboarding@resend.dev"

email_data = {
    "from": f"Nittany AI <{from_domain}>",
    "to": [email],
    "subject": "🧪 Test Email - Nittany AI Email System",
    "html": f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px 10px 0 0; color: white;">
            <h1 style="margin: 0;">🧪 Email Test</h1>
        </div>
        <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
            <h2>Email System Test</h2>
            <p>This is a test email to verify that the Nittany AI email system is working correctly.</p>
            <p><strong>If you received this email, the email sending functionality is working! ✅</strong></p>
            <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
            <p style="color: #666; font-size: 12px;">
                <strong>Sent to:</strong> {email}<br>
                <strong>From:</strong> {from_domain}<br>
                <strong>Base URL:</strong> {BASE_URL}
            </p>
        </div>
    </body>
    </html>
    """,
    "reply_to": from_domain
}

try:
    headers = {
        'Authorization': f'Bearer {RESEND_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        'https://api.resend.com/emails',
        headers=headers,
        json=email_data,
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Email sent successfully!")
        print(f"   Email ID: {result.get('id', 'N/A')}")
        print(f"   To: {email}")
        print(f"\n📬 Check your inbox (and spam folder) for the test email.")
        print(f"\n💡 To check delivery status, visit:")
        print(f"   https://resend.com/emails/{result.get('id', '')}")
    else:
        print(f"❌ Email sending failed!")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")

