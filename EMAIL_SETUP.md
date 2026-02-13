# Email Notification Setup Guide

## ✅ Email Integration Complete!

The system now sends email notifications instead of SMS.

---

## 🚀 Quick Setup with Gmail (5 minutes)

### Step 1: Enable 2-Factor Authentication

1. Go to your Google Account: https://myaccount.google.com
2. Click **Security** (left sidebar)
3. Under "Signing in to Google", click **2-Step Verification**
4. Follow steps to enable it

### Step 2: Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Select app: **Mail**
3. Select device: **Other (Custom name)**
4. Enter name: **Gateway System**
5. Click **Generate**
6. **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

### Step 3: Update .env File

Edit `/Users/jahnavibandarupalli/gateway/.env`:

```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-actual-email@gmail.com
SMTP_PASSWORD=abcdefghijklmnop
COLLEGE_NAME=Your College Name
COLLEGE_EMAIL=your-actual-email@gmail.com
```

**Important:** Remove spaces from app password!

### Step 4: Update Parent Emails in Database

```bash
cd /Users/jahnavibandarupalli/gateway

# Update parent emails
sqlite3 gateway.db "UPDATE users SET parent_email = 'actual-parent@gmail.com' WHERE roll_number = 'L9';"
sqlite3 gateway.db "UPDATE users SET parent_email = 'another-parent@gmail.com' WHERE roll_number = 'CS101';"
```

### Step 5: Restart Server

```bash
lsof -ti:3000 | xargs kill -9
cd /Users/jahnavibandarupalli/gateway
python3 server.py
```

---

## 📧 Email Notifications Implemented

### 1. **Parent Approval Request** (When student submits)
- Professional HTML email
- Clickable approval link
- All request details
- 24-hour expiry notice

### 2. **Approval Confirmation** (When HOD approves)
- Sent to student AND parent
- Leave details
- Gate pass reminder

### 3. **Rejection Notification** (When rejected)
- Sent to student
- Shows who rejected
- Includes rejection reason

### 4. **Cancellation Notification** (When student cancels)
- Sent to parent
- Confirms cancellation

---

## 🧪 Testing Without Gmail (Current Mode)

**Current Status:** Email is disabled (no credentials configured)

When email is disabled:
- ✅ System works normally
- ✅ All workflows function
- ⚠️ Emails are logged to console instead of sent
- ⚠️ Parent token still shown in browser alert

**Console Output:**
```
📧 Email (disabled): To parent.l9@example.com: Permission Request from Student L9
```

---

## 🎨 Email Features

✅ **Professional HTML Design**
- College branding
- Color-coded request types
- Responsive layout
- Mobile-friendly

✅ **Security**
- One-time use links
- 24-hour expiry
- Token-based authentication

✅ **User Experience**
- One-click approval
- Clear information
- No login required for parents

---

## 🔧 Alternative Email Providers

### Using Outlook/Hotmail
```bash
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_EMAIL=your-email@outlook.com
SMTP_PASSWORD=your-password
```

### Using Yahoo
```bash
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_EMAIL=your-email@yahoo.com
SMTP_PASSWORD=your-app-password
```

### Using Custom Domain (e.g., college email)
```bash
SMTP_SERVER=smtp.yourcollege.edu
SMTP_PORT=587
SMTP_EMAIL=gateway@yourcollege.edu
SMTP_PASSWORD=your-password
```

---

## 💰 Cost Comparison

### Email (FREE)
- ✅ **Gmail:** 500 emails/day FREE
- ✅ **Outlook:** 300 emails/day FREE
- ✅ **No ongoing costs**
- ✅ No credit card needed

### SMS (Paid)
- ❌ Twilio: $0.01 per SMS
- ❌ MSG91: ₹0.25 per SMS
- ❌ Monthly costs: ₹500-1000

**Winner:** Email is FREE and works great!

---

## ✅ Current Database Setup

**Students with emails:**
- L9: `student.l9@example.com` (Parent: `parent.l9@example.com`)
- CS101: `student.cs101@example.com` (Parent: `parent.cs101@example.com`)

**To add real emails:**
```bash
sqlite3 gateway.db "UPDATE users SET email = 'real-student@gmail.com', parent_email = 'real-parent@gmail.com' WHERE roll_number = 'L9';"
```

---

## 🎯 What's Working Now

**Without Gmail credentials:**
- ✅ All workflows work
- ✅ Emails logged to console
- ✅ Token shown in browser alert
- ✅ System fully functional

**With Gmail credentials:**
- ✅ Real emails sent to parents
- ✅ Real emails sent to students
- ✅ Professional HTML emails
- ✅ Production-ready

---

## 🚀 Quick Start for Testing

1. **Use your personal Gmail**
2. **Generate app password** (5 minutes)
3. **Update .env file**
4. **Restart server**
5. **Test with your own email**

---

## 📞 Troubleshooting

**"Authentication failed"**
- Make sure 2FA is enabled
- Use app password, not regular password
- Remove spaces from app password

**"Connection refused"**
- Check SMTP server and port
- Verify firewall settings

**"Emails not received"**
- Check spam folder
- Verify email address is correct
- Check server logs for errors

---

## 🔒 Security Notes

- Never commit `.env` file to git (already in .gitignore)
- Use app passwords, not regular passwords
- Rotate credentials periodically
- Use environment variables in production
