# Login Issue Fix Guide

## Problem
Google login fails with "Login failed" error.

## Root Causes Found

### 1. Missing GOOGLE_CLIENT_ID
- `.env` file didn't exist
- `GOOGLE_CLIENT_ID` not configured
- Google OAuth verification fails without it

### 2. Users Have No Email in Database
Some users in database have empty email fields:
```
email: "" (empty)
name: "Student L9"
role: student
```

## Solutions Applied

### ✅ Fix #1: Created .env File
Created `/Users/kruthikab/gateway/.env` with basic configuration

### ✅ Fix #2: Added Development Mode
Modified `server.py` to handle missing GOOGLE_CLIENT_ID:
- If `GOOGLE_CLIENT_ID` not set → Development mode (skips Google verification)
- If `GOOGLE_CLIENT_ID` set → Production mode (full Google OAuth)

**⚠️ Development mode is INSECURE - only for local testing**

### ✅ Fix #3: Alternative Login Methods

**Option A: Use Email Login (Simple Mode)**
1. Enter email address (e.g., `jahnavi@gmail.com`)
2. Click "Login"
3. No password required (development mode)

**Option B: Use Roll Number (Students)**
1. Enter roll number (e.g., `L9`, `CS101`)
2. Click "Login"

**Option C: Configure Google OAuth (Recommended for Production)**
1. Get Google Client ID from Google Cloud Console
2. Add to `.env`: `GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com`
3. Restart server
4. Use Google Sign-In button

## Test Users Available

### Students:
- Roll: `L9` (no email)
- Roll: `CS101`, Email: (empty), Name: Rahul Kumar

### Teachers:
- Email: `jahnavi@gmail.com`, Name: Jahnavi
- Email: `teacher@school.com`, Name: Prof. Singh

### HODs:
- Email: `kruthika@gmail.com`, Name: Kruthika
- Email: `hod@school.com`, Name: Dr. Verma

## How to Login Now

### Method 1: Email Login (Easiest)
```
1. Enter: jahnavi@gmail.com
2. Click "Login"
3. ✅ Logged in as Teacher
```

### Method 2: Roll Number (Students)
```
1. Enter: CS101
2. Click "Login"
3. ✅ Logged in as Student
```

## Next Steps

1. ✅ Server restarted with fixes
2. 🔄 Try logging in with email or roll number
3. ⏭️ If needed: Configure proper Google OAuth for production

## For Production Deployment

1. Get Google OAuth Client ID
2. Update `.env` with real credentials
3. Set `ENFORCE_DOMAIN_RESTRICTION=true` if needed
4. Configure SMTP for email notifications
