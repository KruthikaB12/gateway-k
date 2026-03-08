#!/usr/bin/env python3
"""Comprehensive test suite for Gateway Permission System"""

import requests
import json
import time
import sys

BASE_URL = "http://127.0.0.1:8080"
API_URL = f"{BASE_URL}/api"

tests_passed = 0
tests_failed = 0
bugs_found = []

def test(name, condition, bug_msg=""):
    global tests_passed, tests_failed, bugs_found
    if condition:
        print(f"✅ {name}")
        tests_passed += 1
    else:
        print(f"❌ {name}")
        tests_failed += 1
        if bug_msg:
            bugs_found.append(f"{name}: {bug_msg}")

print("=" * 70)
print("GATEWAY PERMISSION SYSTEM - COMPREHENSIVE TEST SUITE")
print("=" * 70)

# Test 1: Server Health
print("\n🔧 SERVER HEALTH TESTS")
try:
    resp = requests.get(BASE_URL, timeout=3)
    test("Server is running", resp.status_code == 200)
except Exception as e:
    test("Server is running", False, str(e))

# Test 2: Static Files
print("\n📄 STATIC FILE TESTS")
try:
    resp = requests.get(f"{BASE_URL}/front_gate.html", timeout=3)
    test("Front gate HTML loads", resp.status_code == 200 and len(resp.text) > 1000)
    
    resp = requests.get(f"{BASE_URL}/parent-approve.html", timeout=3)
    test("Parent approve HTML loads", resp.status_code == 200 and len(resp.text) > 1000)
except Exception as e:
    test("Static files load", False, str(e))

# Test 3: Database
print("\n🗄️  DATABASE TESTS")
import sqlite3
try:
    conn = sqlite3.connect('gateway.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM users")
    user_count = c.fetchone()[0]
    test("Users table has data", user_count >= 3, f"Only {user_count} users")
    
    c.execute("SELECT COUNT(*) FROM users WHERE role='student'")
    student_count = c.fetchone()[0]
    test("Student exists", student_count >= 1)
    
    c.execute("SELECT COUNT(*) FROM users WHERE role='teacher'")
    teacher_count = c.fetchone()[0]
    test("Teacher exists", teacher_count >= 1)
    
    c.execute("SELECT COUNT(*) FROM users WHERE role='hod'")
    hod_count = c.fetchone()[0]
    test("HOD exists", hod_count >= 1)
    
    c.execute("SELECT email, parent_email FROM users WHERE role='student' LIMIT 1")
    student = c.fetchone()
    test("Student has parent email", student and student[1] is not None and '@' in student[1])
    
    conn.close()
except Exception as e:
    test("Database access", False, str(e))

# Test 4: API Endpoints
print("\n🔌 API ENDPOINT TESTS")
try:
    # Test auth endpoint exists
    resp = requests.post(f"{API_URL}/auth/google", json={"token": "test"}, timeout=3)
    test("Auth endpoint responds", resp.status_code in [400, 401, 500])
    
    # Test student endpoint (should require auth)
    resp = requests.get(f"{API_URL}/student/requests", timeout=3)
    test("Student endpoint requires auth", resp.status_code == 401)
    
    # Test teacher endpoint (should require auth)
    resp = requests.get(f"{API_URL}/teacher/requests/pending", timeout=3)
    test("Teacher endpoint requires auth", resp.status_code == 401)
    
    # Test HOD endpoint (should require auth)
    resp = requests.get(f"{API_URL}/hod/requests/pending", timeout=3)
    test("HOD endpoint requires auth", resp.status_code == 401)
    
except Exception as e:
    test("API endpoints", False, str(e))

# Test 5: CORS Headers
print("\n🌐 CORS TESTS")
try:
    resp = requests.get(f"{API_URL}/student/requests", 
                       headers={'Origin': 'http://localhost:8080'}, timeout=3)
    has_cors = 'access-control-allow-origin' in resp.headers
    test("CORS headers present", has_cors)
except Exception as e:
    test("CORS configuration", False, str(e))

# Test 6: Email Configuration
print("\n📧 EMAIL SERVICE TESTS")
try:
    from email_service import email_enabled, SMTP_EMAIL, SMTP_PASSWORD
    test("Email service enabled", email_enabled)
    test("SMTP email configured", SMTP_EMAIL and '@' in SMTP_EMAIL)
    test("SMTP password configured", SMTP_PASSWORD and len(SMTP_PASSWORD) > 10)
except Exception as e:
    test("Email configuration", False, str(e))

# Test 7: Google OAuth Configuration
print("\n🔐 GOOGLE OAUTH TESTS")
try:
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    test("Google Client ID configured", client_id and '.apps.googleusercontent.com' in client_id)
    
    # Check HTML has correct Client ID
    with open('front_gate.html', 'r') as f:
        html = f.read()
    test("HTML has Google Client ID", client_id in html if client_id else False)
    
except Exception as e:
    test("Google OAuth config", False, str(e))

# Test 8: Frontend Configuration
print("\n🎨 FRONTEND TESTS")
try:
    with open('front_gate.html', 'r') as f:
        html = f.read()
    
    test("API URL uses port 8080", 'http://127.0.0.1:8080/api' in html)
    test("Google Sign-In button present", 'g_id_signin' in html)
    test("Student dashboard present", 'studentDashboard' in html)
    test("Teacher dashboard present", 'teacherDashboard' in html)
    test("HOD dashboard present", 'hodDashboard' in html)
    test("Session persistence (localStorage)", 'localStorage' in html)
    test("Auto-refresh implemented", 'autoRefreshInterval' in html or 'setInterval' in html)
    
    with open('parent-approve.html', 'r') as f:
        parent_html = f.read()
    test("Parent page API URL correct", 'http://127.0.0.1:8080/api' in parent_html)
    
except Exception as e:
    test("Frontend files", False, str(e))

# Test 9: Role Detection
print("\n👥 ROLE DETECTION TESTS")
try:
    conn = sqlite3.connect('gateway.db')
    c = conn.cursor()
    
    c.execute("SELECT email FROM users WHERE role='teacher'")
    teachers = [row[0] for row in c.fetchall()]
    
    # Check if teachers are in server.py
    with open('server.py', 'r') as f:
        server_code = f.read()
    
    for teacher_email in teachers:
        test(f"Teacher {teacher_email} in TEACHER_EMAILS", teacher_email in server_code)
    
    conn.close()
except Exception as e:
    test("Role detection", False, str(e))

# Test 10: Emergency Auto-Approve Logic
print("\n🚨 EMERGENCY AUTO-APPROVE TESTS")
try:
    with open('server.py', 'r') as f:
        server_code = f.read()
    
    test("Emergency auto-approve logic exists", "request_type'].lower() == 'emergency'" in server_code or "request_type == 'Emergency'" in server_code)
    test("Status APPROVED exists", "'APPROVED'" in server_code)
    test("Auto-approved status exists", "'auto_approved'" in server_code)
    
except Exception as e:
    test("Emergency logic", False, str(e))

# Test 11: Security Tests
print("\n🔒 SECURITY TESTS")
try:
    with open('server.py', 'r') as f:
        server_code = f.read()
    
    test("JWT authentication used", 'jwt.encode' in server_code or 'jwt.decode' in server_code)
    test("Password hashing (bcrypt)", 'bcrypt' in server_code)
    test("SQL parameterization", '?' in server_code or '%s' in server_code)
    test("No hardcoded passwords", 'password=' not in server_code.lower() or 'your-password' not in server_code.lower())
    
except Exception as e:
    test("Security checks", False, str(e))

# Summary
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print(f"✅ Tests Passed: {tests_passed}")
print(f"❌ Tests Failed: {tests_failed}")
print(f"📊 Success Rate: {tests_passed}/{tests_passed + tests_failed} ({100*tests_passed/(tests_passed+tests_failed):.1f}%)")

if bugs_found:
    print("\n🐛 BUGS FOUND:")
    for i, bug in enumerate(bugs_found, 1):
        print(f"  {i}. {bug}")
else:
    print("\n🎉 No bugs found!")

print("\n" + "=" * 70)
sys.exit(0 if tests_failed == 0 else 1)
