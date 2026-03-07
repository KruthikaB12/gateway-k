# Deployment Guide - Render.com

## Quick Deploy (5 minutes)

### Step 1: Sign Up
1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories

### Step 2: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your repository: `wingsai/gateway`
3. Configure:
   - **Name:** gateway-permission-system
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `bash start_server.sh`
   - **Plan:** Free

### Step 3: Add Environment Variables
Click "Environment" and add:
```
GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET=YOUR_GOOGLE_CLIENT_SECRET
JWT_SECRET=your-secret-key-change-in-production
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=watermelon37453@gmail.com
SMTP_PASSWORD=fhfbvpbcawkgocid
COLLEGE_NAME=BVRIT Hyderabad
COLLEGE_EMAIL=watermelon37453@gmail.com
```

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait 3-5 minutes for deployment
3. You'll get a URL like: `https://gateway-permission-system.onrender.com`

### Step 5: Update Google OAuth
1. Go to Google Cloud Console → Credentials
2. Add to Authorized JavaScript origins:
   - `https://gateway-permission-system.onrender.com`
3. Save

### Step 6: Test
Open your Render URL and login!

## Database Updates After Deployment

### Option 1: SSH Access
```bash
# Connect to your Render service
render ssh gateway-permission-system

# Update database
python3 import_students.py students.csv
```

### Option 2: Redeploy
1. Update database locally
2. Commit and push
3. Render auto-deploys

## Your Deployed URL
After deployment, share this URL with everyone:
`https://gateway-permission-system.onrender.com`

No ngrok, no localhost issues, works everywhere! 🎉
