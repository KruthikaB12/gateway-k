#!/usr/bin/env python3
"""Quick integration test for running server"""

import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8080"

print("=" * 60)
print("INTEGRATION TEST - Running Server")
print("=" * 60)

tests_passed = 0
tests_failed = 0

def test(name, condition):
    global tests_passed, tests_failed
    if condition:
        print(f"✅ {name}")
        tests_passed += 1
    else:
        print(f"❌ {name}")
        tests_failed += 1

# Test 1: Server is running
try:
    resp = requests.get(BASE_URL, timeout=2)
    test("Server is running", resp.status_code == 200)
except Exception as e:
    test("Server is running", False)
    print(f"   Error: {e}")

# Test 2: HTML page loads
try:
    resp = requests.get(f"{BASE_URL}/front_gate.html", timeout=2)
    test("Front gate HTML loads", resp.status_code == 200 and "<!DOCTYPE html>" in resp.text)
except Exception as e:
    test("Front gate HTML loads", False)

# Test 3: Parent approve page exists
try:
    resp = requests.get(f"{BASE_URL}/parent-approve.html", timeout=2)
    test("Parent approve page exists", resp.status_code == 200)
except Exception as e:
    test("Parent approve page exists", False)

# Test 4: API responds (even with auth error)
try:
    resp = requests.get(f"{BASE_URL}/api/student/requests", timeout=2)
    test("API endpoint responds", resp.status_code in [401, 403])
except Exception as e:
    test("API endpoint responds", False)

# Test 5: CORS headers present
try:
    resp = requests.get(f"{BASE_URL}/api/student/requests", 
                       headers={'Origin': 'http://localhost:8080'}, timeout=2)
    has_cors = 'access-control-allow-origin' in resp.headers
    test("CORS headers configured", has_cors)
except Exception as e:
    test("CORS headers configured", False)

print("\n" + "=" * 60)
print(f"✅ Passed: {tests_passed}/{tests_passed + tests_failed}")
print(f"❌ Failed: {tests_failed}/{tests_passed + tests_failed}")
print("=" * 60)

if tests_failed == 0:
    print("\n🎉 All tests passed! Server is working correctly.")
    sys.exit(0)
else:
    print(f"\n⚠️  {tests_failed} test(s) failed.")
    sys.exit(1)
