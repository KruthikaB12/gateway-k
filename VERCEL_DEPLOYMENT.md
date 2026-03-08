# Deployment Guide - Vercel (Free)

## Quick Deployment to Vercel

---

## Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

Or use without installing:
```bash
npx vercel
```

---

## Step 2: Prepare for Vercel

### Create vercel.json

```bash
cd gateway
```

Create `vercel.json` file:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "server.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "server.py"
    }
  ],
  "env": {
    "GOOGLE_CLIENT_ID": "745219283704-bsdrvaldieopi6bj3h5d4r2n51d42l0q.apps.googleusercontent.com",
    "JWT_SECRET": "production-secret-key-change-this",
    "SMTP_SERVER": "smtp.gmail.com",
    "SMTP_PORT": "587",
    "SMTP_EMAIL": "kruthikaburagadda@gmail.com",
    "SMTP_PASSWORD": "wozyastfdqqymhol",
    "COLLEGE_NAME": "BVRIT Hyderabad",
    "COLLEGE_EMAIL": "kruthikaburagadda@gmail.com",
    "ENFORCE_DOMAIN_RESTRICTION": "false"
  }
}
```

---

## Step 3: Deploy

```bash
cd gateway
vercel
```

Follow the prompts:
1. **Set up and deploy?** → Yes
2. **Which scope?** → Your account
3. **Link to existing project?** → No
4. **Project name?** → gateway-permission (or any name)
5. **Directory?** → ./ (current directory)
6. **Override settings?** → No

Wait 1-2 minutes for deployment.

You'll get a URL like: `https://gateway-permission.vercel.app`

---

## Step 4: Update Google OAuth

1. Go to: https://console.cloud.google.com/apis/credentials
2. Click your OAuth Client ID
3. Add **Authorized JavaScript origins:**
   ```
   https://gateway-permission.vercel.app
   ```
4. Add **Authorized redirect URIs:**
   ```
   https://gateway-permission.vercel.app
   ```
5. Click **Save**

---

## Step 5: Update Environment Variables

```bash
vercel env add BASE_URL
```
Enter: `https://gateway-permission.vercel.app`

Then redeploy:
```bash
vercel --prod
```

---

## Step 6: Test

Open: `https://gateway-permission.vercel.app/front_gate.html`

---

## Important: Vercel Limitations

⚠️ **Vercel has issues with FastAPI/Python backends:**
- Serverless functions have 10-second timeout
- SQLite doesn't work well (serverless environment)
- Database resets on each request

### Better Alternative: Use Vercel for Frontend + Render for Backend

---

## Recommended: Hybrid Deployment

### Option 1: Vercel Frontend + Render Backend

**Frontend (Vercel):**
- Deploy only HTML files
- Fast, free, always-on

**Backend (Render):**
- Deploy Python API
- Database persistence
- Better for long-running processes

### Option 2: Deploy Everything to Render

Render is better suited for Python FastAPI applications.

---

## Quick Commands

```bash
# Deploy to Vercel
vercel

# Deploy to production
vercel --prod

# Check logs
vercel logs

# Remove deployment
vercel remove gateway-permission
```

---

**Recommendation:** Use Render.com instead of Vercel for this Python FastAPI application. Vercel is optimized for Next.js/Node.js, not Python backends.

Would you like me to create the Render deployment guide instead?
