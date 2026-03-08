#!/bin/bash
# Render deployment script

echo "🚀 Starting Gateway Application..."

# Initialize database (works with both SQLite and PostgreSQL)
python3 init_db_postgres.py

# Start backend with uvicorn
uvicorn server:app --host 0.0.0.0 --port ${PORT:-8080}
