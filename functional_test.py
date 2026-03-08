#!/usr/bin/env python3
"""Functional workflow tests - simulate real user scenarios"""

import sqlite3
import sys

print("=" * 70)
print("FUNCTIONAL WORKFLOW TESTS")
print("=" * 70)

bugs = []

# Test 1: Check request flow states
print("\n📋 REQUEST WORKFLOW TESTS")
try:
    conn = sqlite3.connect('gateway.db')
    c = conn.cursor()
    
    # Check if requests table exists and has correct columns
    c.execute("PRAGMA table_info(requests)")
    columns = [col[1] for col in c.fetchall()]
    
    required_columns = ['id', 'student_id', 'request_type', 'reason', 'leave_date', 
                       'leave_time', 'status', 'parent_status', 'teacher_status', 'hod_status']
    
    for col in required_columns:
        if col in columns:
            print(f"✅ Column '{col}' exists")
        else:
            print(f"❌ Column '{col}' missing")
            bugs.append(f"Missing column: {col}")
    
    conn.close()
except Exception as e:
    print(f"❌ Database schema check failed: {e}")
    bugs.append(f"Database schema: {e}")

# Test 2: Check user data integrity
print("\n👤 USER DATA INTEGRITY TESTS")
try:
    conn = sqlite3.connect('gateway.db')
    c = conn.cursor()
    
    # Check students have required fields
    c.execute("SELECT email, name, class, parent_email FROM users WHERE role='student'")
    students = c.fetchall()
    
    for student in students:
        email, name, cls, parent_email = student
        if not email or '@' not in email:
            print(f"❌ Student missing valid email: {name}")
            bugs.append(f"Student {name} has invalid email")
        else:
            print(f"✅ Student {name} has valid email")
        
        if not parent_email or '@' not in parent_email:
            print(f"❌ Student {name} missing parent email")
            bugs.append(f"Student {name} missing parent email")
        else:
            print(f"✅ Student {name} has parent email")
        
        if not cls:
            print(f"❌ Student {name} missing class")
            bugs.append(f"Student {name} missing class")
        else:
            print(f"✅ Student {name} has class: {cls}")
    
    # Check teachers have class assignments
    c.execute("SELECT email, name, class FROM users WHERE role='teacher'")
    teachers = c.fetchall()
    
    for teacher in teachers:
        email, name, cls = teacher
        if not cls:
            print(f"⚠️  Teacher {name} has no class assignment")
        else:
            print(f"✅ Teacher {name} assigned to class: {cls}")
    
    conn.close()
except Exception as e:
    print(f"❌ User data check failed: {e}")
    bugs.append(f"User data: {e}")

# Test 3: Check frontend-backend consistency
print("\n🔄 FRONTEND-BACKEND CONSISTENCY TESTS")
try:
    with open('front_gate.html', 'r') as f:
        html = f.read()
    
    with open('server.py', 'r') as f:
        server = f.read()
    
    # Check API endpoints match
    frontend_endpoints = [
        '/auth/google',
        '/student/requests',
        '/student/request',
        '/student/cancel/',
        '/teacher/requests/pending',
        '/teacher/approve/',
        '/teacher/reject/',
        '/hod/requests/pending',
        '/hod/approve/',
        '/hod/reject/',
        '/parent/request/',
        '/parent/approve/',
        '/parent/reject/'
    ]
    
    for endpoint in frontend_endpoints:
        if endpoint in html and endpoint in server:
            print(f"✅ Endpoint {endpoint} exists in both")
        elif endpoint in html and endpoint not in server:
            print(f"❌ Endpoint {endpoint} in frontend but not backend")
            bugs.append(f"Missing backend endpoint: {endpoint}")
        elif endpoint not in html and endpoint in server:
            print(f"⚠️  Endpoint {endpoint} in backend but not used in frontend")
    
except Exception as e:
    print(f"❌ Consistency check failed: {e}")
    bugs.append(f"Consistency: {e}")

# Test 4: Check email templates
print("\n📧 EMAIL TEMPLATE TESTS")
try:
    with open('email_service.py', 'r') as f:
        email_code = f.read()
    
    required_functions = [
        'send_parent_approval_email',
        'send_approval_notification_email',
        'send_rejection_notification_email'
    ]
    
    for func in required_functions:
        if f"def {func}" in email_code:
            print(f"✅ Email function {func} exists")
        else:
            print(f"❌ Email function {func} missing")
            bugs.append(f"Missing email function: {func}")
    
    # Check if email templates have required info
    if 'Leave Date' in email_code and 'Leave Time' in email_code:
        print("✅ Email templates have leave date/time")
    else:
        print("❌ Email templates missing leave date/time")
        bugs.append("Email templates incomplete")
    
except Exception as e:
    print(f"❌ Email template check failed: {e}")
    bugs.append(f"Email templates: {e}")

# Test 5: Check logout functionality
print("\n🚪 LOGOUT FUNCTIONALITY TESTS")
try:
    with open('front_gate.html', 'r') as f:
        html = f.read()
    
    if 'clearSession' in html and 'localStorage.removeItem' in html:
        print("✅ Logout clears session storage")
    else:
        print("❌ Logout doesn't clear session properly")
        bugs.append("Logout doesn't clear localStorage")
    
    if 'stopAutoRefresh' in html:
        print("✅ Logout stops auto-refresh")
    else:
        print("⚠️  Logout might not stop auto-refresh")
    
except Exception as e:
    print(f"❌ Logout check failed: {e}")

# Summary
print("\n" + "=" * 70)
print("FUNCTIONAL TEST SUMMARY")
print("=" * 70)

if bugs:
    print(f"🐛 Found {len(bugs)} potential issues:")
    for i, bug in enumerate(bugs, 1):
        print(f"  {i}. {bug}")
    sys.exit(1)
else:
    print("🎉 All functional tests passed! No bugs found.")
    sys.exit(0)
