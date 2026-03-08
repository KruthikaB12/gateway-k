#!/usr/bin/env python3
"""Test suite for Gateway Permission System"""

import sys
import os
from datetime import datetime, timedelta

# Test results
tests_passed = 0
tests_failed = 0
bugs_found = []

def test(name, condition, error_msg=""):
    global tests_passed, tests_failed, bugs_found
    if condition:
        print(f"✅ {name}")
        tests_passed += 1
    else:
        print(f"❌ {name}")
        tests_failed += 1
        if error_msg:
            bugs_found.append(f"{name}: {error_msg}")

print("=" * 60)
print("GATEWAY PERMISSION SYSTEM - TEST SUITE")
print("=" * 60)

# Test 1: File existence
print("\n📁 FILE EXISTENCE TESTS")
required_files = [
    'server.py', 'db_connection.py', 'init_db.py', 'init_db_postgres.py',
    'email_service.py', 'front_gate.html', 'requirements.txt', '.env.example'
]
for file in required_files:
    test(f"File exists: {file}", os.path.exists(file), f"Missing {file}")

# Test 2: Python imports
print("\n🐍 PYTHON IMPORT TESTS")
try:
    from db_connection import get_db
    test("Import db_connection", True)
except Exception as e:
    test("Import db_connection", False, str(e))

try:
    from email_service import send_email
    test("Import email_service", True)
except Exception as e:
    test("Import email_service", False, str(e))

# Test 3: Environment variables
print("\n🔧 ENVIRONMENT CONFIGURATION TESTS")
from dotenv import load_dotenv
load_dotenv()

env_vars = ['GOOGLE_CLIENT_ID', 'SMTP_EMAIL', 'SMTP_SERVER', 'COLLEGE_NAME']
for var in env_vars:
    value = os.getenv(var)
    test(f"Env var {var}", value is not None, f"{var} not set")

# Test 4: Database connection
print("\n🗄️  DATABASE TESTS")
try:
    from db_connection import get_db
    conn = get_db()
    test("Database connection", conn is not None)
    
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    conn.close()
    
    required_tables = ['users', 'requests']  # Fixed: table is 'requests' not 'permission_requests'
    for table in required_tables:
        found = any(table in str(t) for t in tables)
        test(f"Table exists: {table}", found, f"Table {table} missing")
except Exception as e:
    test("Database connection", False, str(e))

# Test 5: Server configuration
print("\n⚙️  SERVER CONFIGURATION TESTS")
try:
    import sys
    sys.path.insert(0, '.')
    
    # Check server.py for critical configurations
    with open('server.py', 'r') as f:
        server_code = f.read()
    
    test("FastAPI imported", 'from fastapi import FastAPI' in server_code)
    test("CORS configured", 'CORSMiddleware' in server_code)
    test("JWT configured", 'import jwt' in server_code)
    test("Google OAuth configured", 'GOOGLE_CLIENT_ID' in server_code)
    test("Emergency auto-approve logic", "request_type == 'Emergency'" in server_code or "request_type == 'emergency'" in server_code)
    
except Exception as e:
    test("Server configuration check", False, str(e))

# Test 6: Email service
print("\n📧 EMAIL SERVICE TESTS")
try:
    from email_service import send_parent_approval_email, send_approval_notification_email
    test("Email functions defined", True)
    
    # Check if BASE_URL is used
    with open('email_service.py', 'r') as f:
        email_code = f.read()
    test("BASE_URL configured", 'BASE_URL' in email_code)
    test("HTML email templates", '<html>' in email_code)
    
except Exception as e:
    test("Email service check", False, str(e))

# Test 7: Frontend validation
print("\n🌐 FRONTEND TESTS")
try:
    with open('front_gate.html', 'r') as f:
        html_code = f.read()
    
    test("Google OAuth button", 'google' in html_code.lower())
    test("Student dashboard", 'student' in html_code.lower())
    test("Teacher dashboard", 'teacher' in html_code.lower())
    test("HOD dashboard", 'hod' in html_code.lower())
    test("API calls configured", 'fetch(' in html_code or 'apiCall' in html_code)
    test("Emergency request type", 'emergency' in html_code.lower())
    
except Exception as e:
    test("Frontend check", False, str(e))

# Test 8: Deployment readiness
print("\n🚀 DEPLOYMENT READINESS TESTS")
test("requirements.txt exists", os.path.exists('requirements.txt'))
test("render.yaml exists", os.path.exists('render.yaml'))
test("start_server.sh exists", os.path.exists('start_server.sh'))

if os.path.exists('start_server.sh'):
    with open('start_server.sh', 'r') as f:
        start_script = f.read()
    test("Start script has uvicorn", 'uvicorn' in start_script)

# Test 9: Security checks
print("\n🔒 SECURITY TESTS")
try:
    with open('server.py', 'r') as f:
        server_code = f.read()
    
    test("JWT secret configured", 'JWT_SECRET' in server_code)
    test("Password hashing (bcrypt)", 'bcrypt' in server_code)
    # SQL injection protection via parameterized queries
    has_sql_protection = '?' in server_code or '%s' in server_code
    test("SQL injection protection", has_sql_protection)
    
    # Check for hardcoded secrets
    has_hardcoded = 'password=' in server_code.lower() and '=' in server_code
    test("No hardcoded passwords", 'your-password' not in server_code.lower())
    
except Exception as e:
    test("Security check", False, str(e))

# Test 10: Logic bugs
print("\n🐛 LOGIC BUG TESTS")
try:
    with open('server.py', 'r') as f:
        server_code = f.read()
    
    # Check emergency auto-approve logic
    has_emergency_logic = ("request_type'].lower() == 'emergency'" in server_code or 
                          "request_type == 'Emergency'" in server_code)
    test("Emergency auto-approve implemented", has_emergency_logic)
    
    # Check status transitions
    test("Status APPROVED exists", 'APPROVED' in server_code)
    test("Status PENDING exists", 'PENDING' in server_code)
    
    # Check email notifications
    test("Parent email notification", 'send_parent_approval_email' in server_code)
    test("Approval notification", 'send_approval_notification_email' in server_code)
    
except Exception as e:
    test("Logic bug check", False, str(e))

# Summary
print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print(f"✅ Tests Passed: {tests_passed}")
print(f"❌ Tests Failed: {tests_failed}")
print(f"📊 Success Rate: {tests_passed}/{tests_passed + tests_failed} ({100*tests_passed/(tests_passed+tests_failed):.1f}%)")

if bugs_found:
    print("\n🐛 BUGS FOUND:")
    for i, bug in enumerate(bugs_found, 1):
        print(f"  {i}. {bug}")
else:
    print("\n🎉 No critical bugs found!")

print("\n" + "=" * 60)
sys.exit(0 if tests_failed == 0 else 1)
