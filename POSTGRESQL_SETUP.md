# PostgreSQL Setup Guide for Render

## What Changed

Your app now supports **PostgreSQL** for persistent data storage! Data will survive redeployments.

## Benefits

✅ **Data persists** across deployments  
✅ **No need to re-import** students after code updates  
✅ **Production-ready** database  
✅ **Free tier available** on Render  
✅ **Automatic backups**  

## Deployment Options

### Option 1: With PostgreSQL (Recommended)

1. **Deploy using render.yaml:**
   - Render will automatically create a PostgreSQL database
   - Database connection is auto-configured
   - Data persists forever

2. **Manual setup:**
   - Create PostgreSQL database in Render dashboard
   - Copy the "Internal Database URL"
   - Add as `DATABASE_URL` environment variable

### Option 2: Without PostgreSQL (SQLite fallback)

- If no `DATABASE_URL` is set, app uses SQLite
- Data resets on each deployment
- Good for testing only

## Files Added

- `db_connection.py` - Smart connection handler (auto-detects SQLite vs PostgreSQL)
- `init_db_postgres.py` - Database initialization for both databases
- Updated `requirements.txt` - Added `psycopg2-binary`
- Updated `render.yaml` - Includes PostgreSQL database config

## How It Works

The app automatically detects which database to use:

```python
if DATABASE_URL exists and starts with 'postgres':
    → Use PostgreSQL
else:
    → Use SQLite (local development)
```

## Deployment Steps

### Using render.yaml (Easiest):

1. Go to Render Dashboard
2. **New → Blueprint**
3. Connect your Git repository
4. Select `render.yaml`
5. Click **Apply**
6. Render creates:
   - Web service (your app)
   - PostgreSQL database
   - Connects them automatically

### Manual Setup:

1. **Create PostgreSQL Database:**
   - Dashboard → New → PostgreSQL
   - Name: `gateway-db`
   - Plan: Free
   - Create

2. **Create Web Service:**
   - Dashboard → New → Web Service
   - Connect repository
   - Add environment variables
   - **Add DATABASE_URL:**
     - Copy "Internal Database URL" from your PostgreSQL database
     - Add as environment variable: `DATABASE_URL=<paste URL>`

3. **Deploy**

## After Deployment

### First Time Setup:

The database initializes automatically with sample users:
- 4 students
- 1 teacher (Sundari M - CS-B)
- 1 HOD (CSE department)

### Adding More Users:

**Via CSV Import:**
```bash
# In Render Shell
python3 import_students.py students.csv
```

**Via Direct SQL:**
```bash
# In Render Shell
python3 -c "
from db_connection import get_db
conn = get_db()
c = conn.cursor()
c.execute('''INSERT INTO users (role, name, email, class, department, parent_email) 
             VALUES (%s, %s, %s, %s, %s, %s)''', 
          ('student', 'Name', 'email@bvrit.edu.in', 'CS-A', 'CSE', 'parent@gmail.com'))
conn.commit()
"
```

## Local Development

Still works with SQLite:
```bash
# No DATABASE_URL set → uses SQLite
python3 server.py
```

## Database Comparison

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| Data persistence | ❌ Resets on deploy | ✅ Persists forever |
| Concurrent users | ⚠️ Limited | ✅ Unlimited |
| Production ready | ❌ No | ✅ Yes |
| Render cost | Free | Free tier available |
| Setup complexity | Easy | Easy (with render.yaml) |

## Troubleshooting

**Error: "relation does not exist"**
- Database tables not created
- Run: `python3 init_db_postgres.py`

**Error: "could not connect to server"**
- DATABASE_URL incorrect
- Check environment variable in Render dashboard

**Data still resetting:**
- Verify DATABASE_URL is set
- Check it starts with `postgres://` or `postgresql://`

## Migration from SQLite

If you already deployed with SQLite:

1. Create PostgreSQL database in Render
2. Add DATABASE_URL environment variable
3. Redeploy
4. Import your student data

Old SQLite data is not automatically migrated.

---

**Ready to deploy with PostgreSQL!** 🚀
