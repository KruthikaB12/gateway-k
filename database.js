const Database = require('better-sqlite3');
const bcrypt = require('bcryptjs');

const db = new Database('gateway.db');

// Create tables
db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    email TEXT,
    password_hash TEXT NOT NULL,
    phone_number TEXT,
    name TEXT NOT NULL,
    department TEXT,
    class TEXT,
    roll_number TEXT UNIQUE,
    parent_phone TEXT,
    parent_name TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

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
    token_expiry DATETIME,
    token_used INTEGER DEFAULT 0,
    parent_status TEXT,
    teacher_status TEXT,
    hod_status TEXT,
    parent_rejection_reason TEXT,
    teacher_rejection_reason TEXT,
    hod_rejection_reason TEXT,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    parent_approved_at DATETIME,
    teacher_approved_at DATETIME,
    hod_approved_at DATETIME,
    cancelled_at DATETIME,
    FOREIGN KEY (student_id) REFERENCES users(id)
  );

  CREATE INDEX IF NOT EXISTS idx_requests_status ON requests(status);
  CREATE INDEX IF NOT EXISTS idx_requests_student ON requests(student_id);
  CREATE INDEX IF NOT EXISTS idx_requests_token ON requests(parent_token);
`);

// Seed initial users
const seedUsers = () => {
  const hashedPassword1 = bcrypt.hashSync('8712209017', 10);
  const hashedPassword2 = bcrypt.hashSync('1234567890', 10);
  const hashedPassword3 = bcrypt.hashSync('jahnavi123', 10);
  const hashedPassword4 = bcrypt.hashSync('teacher123', 10);
  const hashedPassword5 = bcrypt.hashSync('kruthika123', 10);
  const hashedPassword6 = bcrypt.hashSync('hod123', 10);

  const checkUser = db.prepare('SELECT COUNT(*) as count FROM users').get();
  
  if (checkUser.count === 0) {
    const insert = db.prepare(`
      INSERT INTO users (role, email, password_hash, name, department, class, roll_number, parent_phone)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `);

    insert.run('student', null, hashedPassword1, 'Student L9', 'CSE', 'CS-A', 'L9', '7416016864');
    insert.run('student', null, hashedPassword2, 'Rahul Kumar', 'CSE', 'CS-A', 'CS101', '9876543210');
    insert.run('teacher', 'jahnavi@gmail.com', hashedPassword3, 'Jahnavi', 'CSE', 'CS-A', null, null);
    insert.run('teacher', 'teacher@school.com', hashedPassword4, 'Prof. Singh', 'CSE', 'CS-B', null, null);
    insert.run('hod', 'kruthika@gmail.com', hashedPassword5, 'Kruthika', 'CSE', null, null, null);
    insert.run('hod', 'hod@school.com', hashedPassword6, 'Dr. Verma', 'ECE', null, null, null);

    console.log('✅ Database seeded with initial users');
  }
};

seedUsers();

module.exports = db;
