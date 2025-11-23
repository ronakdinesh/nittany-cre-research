#!/usr/bin/env python3
"""
Test email sending functionality
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv('.env.local')

RESEND_API_KEY = os.getenv('RESEND_API_KEY')
BASE_URL = os.getenv('BASE_URL', 'https://aimarketresearch.app')
TEST_EMAIL = os.getenv('TEST_EMAIL', 'ronakhq@gmail.com')

def test_email_sending():
    """Test if email can be sent via Resend API"""
    
    print("🧪 Testing Email Sending Functionality\n")
    print("-" * 80)
    
    # Check if RESEND_API_KEY is configured
    if not RESEND_API_KEY:
        print("❌ RESEND_API_KEY is not configured in .env.local")
        print("   Add: RESEND_API_KEY=your_resend_api_key")
        return False
    
    print(f"✅ RESEND_API_KEY: Configured")
    print(f"📧 Test Email: {TEST_EMAIL}")
    print(f"🌐 Base URL: {BASE_URL}")
    print("-" * 80)
    
    # Prepare test email
    # Use Resend's test domain for development (works without verification)
    from_domain = "onboarding@resend.dev"
    
    email_data = {
        "from": f"Nittany AI <{from_domain}>",
        "to": [TEST_EMAIL],
        "subject": "🧪 Test Email - Nittany AI Email System",
        "html": f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Email System Test</h2>
            <p>This is a test email to verify that the Nittany AI email system is working correctly.</p>
            <p>If you received this email, the email sending functionality is working! ✅</p>
            <hr>
            <p><small>Test sent from: {BASE_URL}</small></p>
        </body>
        </html>
        """,
        "reply_to": from_domain
    }
    
    # Send test email
    try:
        print("\n📤 Sending test email...")
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
            print(f"   To: {TEST_EMAIL}")
            print(f"\n📬 Check your inbox (and spam folder) for the test email.")
            return True
        else:
            print(f"❌ Email sending failed!")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text}")
            
            # Check for common errors
            if response.status_code == 401:
                print("\n⚠️  Authentication failed. Check if RESEND_API_KEY is correct.")
            elif response.status_code == 403:
                print("\n⚠️  Forbidden. Check if your Resend account has permission to send emails.")
            elif response.status_code == 422:
                print("\n⚠️  Validation error. Check email format and sender domain.")
            
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Check your internet connection.")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_email_template():
    """Check if email template exists"""
    template_path = 'templates/email_report_ready.html'
    if os.path.exists(template_path):
        print(f"✅ Email template found: {template_path}")
        return True
    else:
        print(f"⚠️  Email template not found: {template_path}")
        print("   The app will still work but may use default email format.")
        return False

if __name__ == "__main__":
    print("=" * 80)
    print("Nittany AI - Email System Test")
    print("=" * 80)
    
    # Check template
    print("\n1. Checking email template...")
    check_email_template()
    
    # Test sending
    print("\n2. Testing email sending...")
    success = test_email_sending()
    
    print("\n" + "=" * 80)
    if success:
        print("✅ Email system test completed successfully!")
        print("   If you didn't receive the email, check:")
        print("   - Spam/junk folder")
        print("   - Resend dashboard for delivery status")
        print("   - Email address is correct")
    else:
        print("❌ Email system test failed!")
        print("   Check the error messages above and verify your configuration.")
    print("=" * 80)

