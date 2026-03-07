import os
import sqlite3
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def get_db():
    """Get database connection - supports both SQLite and PostgreSQL"""
    if DATABASE_URL and DATABASE_URL.startswith('postgres'):
        # PostgreSQL connection
        import psycopg2
        from psycopg2.extras import RealDictCursor
        
        # Render uses postgres:// but psycopg2 needs postgresql://
        db_url = DATABASE_URL.replace('postgres://', 'postgresql://')
        conn = psycopg2.connect(db_url, cursor_factory=RealDictCursor)
        conn.row_factory = dict_factory_postgres
        return conn
    else:
        # SQLite connection (fallback for local development)
        conn = sqlite3.connect('gateway.db', check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

def dict_factory_postgres(cursor, row):
    """Convert PostgreSQL row to dict"""
    return dict(row)

def execute_query(query, params=None, fetch=False):
    """Execute query with automatic connection handling"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall() if fetch == 'all' else cursor.fetchone()
            conn.close()
            return result
        else:
            conn.commit()
            last_id = cursor.lastrowid if hasattr(cursor, 'lastrowid') else None
            conn.close()
            return last_id
    except Exception as e:
        conn.rollback()
        conn.close()
        raise e
