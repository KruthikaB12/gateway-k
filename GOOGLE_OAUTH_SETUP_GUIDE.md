# Google OAuth Setup Guide

## Step 1: Create Google Cloud Project

1. Go to **Google Cloud Console**: https://console.cloud.google.com
2. Click **Select a project** → **New Project**
3. Project name: `Gateway Permission System`
4. Click **Create**

## Step 2: Enable Google+ API

1. In the left menu, go to **APIs & Services** → **Library**
2. Search for "Google+ API"
3. Click **Enable**

## Step 3: Create OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **External** (for testing with any Google account)
3. Click **Create**

**Fill in:**
- App name: `Gateway Permission System`
- User support email: Your email
- Developer contact: Your email
- Click **Save and Continue**

**Scopes:** Click **Save and Continue** (default scopes are fine)

**Test users:** 
- Add: `25wh1a05g5@bvrithyderabad.edu.in`
- Add: `25wh1a05d1@bvrithyderabad.edu.in`
- Add: `25wh1a05l9@bvrithyderabad.edu.in`
- Click **Save and Continue**

## Step 4: Create OAuth Client ID

1. Go to **APIs & Services** → **Credentials**
2. Click **+ Create Credentials** → **OAuth client ID**
3. Application type: **Web application**
4. Name: `Gateway Web Client`

**Authorized JavaScript origins:**
```
http://localhost:8080
http://127.0.0.1:8080
```

**Authorized redirect URIs:**
```
http://localhost:8080
http://127.0.0.1:8080
```

5. Click **Create**
6. **Copy the Client ID** (looks like: `xxxxx.apps.googleusercontent.com`)

## Step 5: Configure Application

1. Open `.env` file in gateway folder
2. Update:
```
GOOGLE_CLIENT_ID=YOUR_CLIENT_ID_HERE.apps.googleusercontent.com
```

3. Open `front_gate.html`
4. Find line with `data-client_id=`
5. Replace with your Client ID:
```html
data-client_id="YOUR_CLIENT_ID_HERE.apps.googleusercontent.com"
```

## Step 6: Restart Server

```bash
cd gateway
kill $(cat server.pid)
python3 -m uvicorn server:app --host 127.0.0.1 --port 8080 > server.log 2>&1 &
echo $! > server.pid
```

## Step 7: Test Login

1. Open http://127.0.0.1:8080/front_gate.html
2. Click **Sign in with Google**
3. Select your @bvrithyderabad.edu.in account
4. Grant permissions
5. ✅ You should be logged in!

---

## Quick Setup (If you already have Client ID)

Just provide your Google Client ID and I'll configure everything automatically.

**Your Client ID format:** `123456789-abc123.apps.googleusercontent.com`
