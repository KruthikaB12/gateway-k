#!/bin/bash
# Render deployment script

echo "🚀 Starting Gateway Application..."

# Initialize database (works with both SQLite and PostgreSQL)
python3 init_db_postgres.py

# Start backend and proxy server
python3 server.py &
python3 proxy_server.py
