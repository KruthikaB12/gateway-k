# Railway Deployment Guide (Free $5 Credit)

## Quick Deployment to Railway.app

---

## Step 1: Sign Up for Railway

1. Go to: https://railway.app
2. Click **"Start a New Project"**
3. Sign up with **GitHub** (recommended)

You get **$5 free credit** (enough for ~500 hours)

---

## Step 2: Push Code to GitHub

```bash
cd gateway

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Deploy to Railway"

# Create GitHub repo and push
# (Or use existing repo)
```

---

## Step 3: Deploy to Railway

### Option A: Deploy from GitHub (Recommended)

1. Go to Railway dashboard
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `gateway` repository
5. Railway will auto-detect Python and deploy

### Option B: Deploy with Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
cd gateway
railway init

# Deploy
railway up
```

---

## Step 4: Configure Environment Variables

In Railway dashboard:

1. Click your project
2. Go to **"Variables"** tab
3. Add these variables:

```
GOOGLE_CLIENT_ID=745219283704-bsdrvaldieopi6bj3h5d4r2n51d42l0q.apps.googleusercontent.com
JWT_SECRET=production-secret-key-change-this-random
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=kruthikaburagadda@gmail.com
SMTP_PASSWORD=wozyastfdqqymhol
COLLEGE_NAME=BVRIT Hyderabad
COLLEGE_EMAIL=kruthikaburagadda@gmail.com
ENFORCE_DOMAIN_RESTRICTION=false
PORT=8080
```

4. Click **"Add"** for each variable

---

## Step 5: Configure Start Command

1. In Railway dashboard, go to **"Settings"**
2. Find **"Start Command"**
3. Set to:
   ```
   python3 -m uvicorn server:app --host 0.0.0.0 --port $PORT
   ```
4. Save

---

## Step 6: Get Your Deployment URL

1. In Railway dashboard, go to **"Settings"**
2. Click **"Generate Domain"**
3. You'll get a URL like: `https://gateway-production.up.railway.app`

---

## Step 7: Update BASE_URL

1. Go back to **"Variables"** tab
2. Add/Update:
   ```
   BASE_URL=https://gateway-production.up.railway.app
   ```
3. Railway will auto-redeploy

---

## Step 8: Update Google OAuth

1. Go to: https://console.cloud.google.com/apis/credentials
2. Click your OAuth Client ID
3. Add **Authorized JavaScript origins:**
   ```
   https://gateway-production.up.railway.app
   ```
4. Add **Authorized redirect URIs:**
   ```
   https://gateway-production.up.railway.app
   ```
5. Click **Save**

---

## Step 9: Initialize Database

### Option A: Using Railway CLI
```bash
railway run python3 init_db.py
```

### Option B: Using Railway Dashboard
1. Go to your project
2. Click **"Deployments"**
3. Click latest deployment
4. Click **"View Logs"**
5. Database should auto-initialize on first run

---

## Step 10: Test Your Deployment

1. Open: `https://your-app.up.railway.app/front_gate.html`
2. Login with Google
3. Test submitting a request
4. Check parent email

---

## Railway Features

✅ **Automatic HTTPS**
✅ **Auto-deploy on git push**
✅ **Built-in monitoring**
✅ **Easy database management**
✅ **$5 free credit monthly**

---

## Cost Estimate

- **Free tier:** $5 credit/month
- **Usage:** ~$0.01/hour
- **Estimate:** ~500 hours free (plenty for testing)

---

## Add PostgreSQL (Optional but Recommended)

1. In Railway dashboard, click **"New"**
2. Select **"Database"** → **"PostgreSQL"**
3. Railway will create and link database
4. Add to your variables:
   ```
   DATABASE_URL=<automatically set by Railway>
   ```

---

## Troubleshooting

### Issue: Build fails
- Check `requirements.txt` is present
- Check Python version in logs
- Verify all dependencies are listed

### Issue: App crashes
- Check logs in Railway dashboard
- Verify environment variables are set
- Check start command is correct

### Issue: Can't access app
- Verify domain is generated
- Check deployment status is "Active"
- Wait 1-2 minutes after deployment

---

## Quick Commands (Railway CLI)

```bash
# Deploy
railway up

# View logs
railway logs

# Open app in browser
railway open

# Run command
railway run python3 init_db.py

# Link to project
railway link
```

---

## Your Deployment Checklist

- [ ] Railway account created
- [ ] Code pushed to GitHub
- [ ] Project created in Railway
- [ ] Environment variables added
- [ ] Start command configured
- [ ] Domain generated
- [ ] BASE_URL updated
- [ ] Google OAuth URLs updated
- [ ] Database initialized
- [ ] App tested

---

## Final URLs

After deployment:
- **App:** `https://your-app.up.railway.app/front_gate.html`
- **API:** `https://your-app.up.railway.app/api`

---

**Estimated Time:** 10-15 minutes

**Cost:** FREE ($5 credit)

**Advantages over Vercel:**
- ✅ Better Python support
- ✅ Persistent database
- ✅ No serverless timeouts
- ✅ Auto-deploy on push
- ✅ Built-in PostgreSQL

Ready to deploy? Just follow the steps above!
