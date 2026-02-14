import sqlite3
import bcrypt
from datetime import datetime

def init_db():
    conn = sqlite3.connect('gateway.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            email TEXT,
            password_hash TEXT,
            phone_number TEXT,
            name TEXT NOT NULL,
            department TEXT,
            class TEXT,
            roll_number TEXT UNIQUE,
            parent_phone TEXT,
            parent_email TEXT,
            parent_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create requests table
    c.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id TEXT UNIQUE NOT NULL,
            student_id INTEGER NOT NULL,
            student_name TEXT NOT NULL,
            student_roll TEXT NOT NULL,
            student_class TEXT NOT NULL,
            student_department TEXT NOT NULL,
            parent_phone TEXT NOT NULL,
            request_type TEXT NOT NULL,
            reason TEXT NOT NULL,
            leave_date TEXT NOT NULL,
            leave_time TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            status TEXT NOT NULL,
            parent_token TEXT UNIQUE,
            token_expiry TIMESTAMP,
            token_used INTEGER DEFAULT 0,
            parent_status TEXT,
            teacher_status TEXT,
            hod_status TEXT,
            parent_rejection_reason TEXT,
            teacher_rejection_reason TEXT,
            hod_rejection_reason TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            parent_approved_at TIMESTAMP,
            teacher_approved_at TIMESTAMP,
            hod_approved_at TIMESTAMP,
            cancelled_at TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES users(id)
        )
    ''')
    
    # Create indexes
    c.execute('CREATE INDEX IF NOT EXISTS idx_requests_status ON requests(status)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_requests_student ON requests(student_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_requests_token ON requests(parent_token)')
    
    # Seed users if empty
    c.execute('SELECT COUNT(*) FROM users')
    if c.fetchone()[0] == 0:
        users = [
            ('student', None, bcrypt.hashpw('8712209017'.encode(), bcrypt.gensalt()).decode(), 'Student L9', 'CSE', 'CS-A', 'L9', '7416016864'),
            ('student', None, bcrypt.hashpw('1234567890'.encode(), bcrypt.gensalt()).decode(), 'Rahul Kumar', 'CSE', 'CS-A', 'CS101', '9876543210'),
            ('teacher', 'jahnavi@gmail.com', bcrypt.hashpw('jahnavi123'.encode(), bcrypt.gensalt()).decode(), 'Jahnavi', 'CSE', 'CS-A', None, None),
            ('teacher', 'teacher@school.com', bcrypt.hashpw('teacher123'.encode(), bcrypt.gensalt()).decode(), 'Prof. Singh', 'CSE', 'CS-B', None, None),
            ('hod', 'kruthika@gmail.com', bcrypt.hashpw('kruthika123'.encode(), bcrypt.gensalt()).decode(), 'Kruthika', 'CSE', None, None, None),
            ('hod', 'hod@school.com', bcrypt.hashpw('hod123'.encode(), bcrypt.gensalt()).decode(), 'Dr. Verma', 'ECE', None, None, None),
        ]
        
        for user in users:
            c.execute('''
                INSERT INTO users (role, email, password_hash, name, department, class, roll_number, parent_phone)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', user)
        
        print('✅ Database seeded with initial users')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print('✅ Database initialized')
