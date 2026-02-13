require('dotenv').config();
const express = require('express');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const db = require('./database');
const { authMiddleware, roleMiddleware } = require('./middleware');

const app = express();
app.use(cors());
app.use(express.json());

// ============ AUTH ENDPOINTS ============

app.post('/api/auth/login', (req, res) => {
  const { role, identifier, password } = req.body;

  try {
    let user;
    if (role === 'student') {
      user = db.prepare('SELECT * FROM users WHERE role = ? AND roll_number = ?').get(role, identifier.toUpperCase());
    } else {
      user = db.prepare('SELECT * FROM users WHERE role = ? AND email = ?').get(role, identifier.toLowerCase());
    }

    if (!user || !bcrypt.compareSync(password, user.password_hash)) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    const token = jwt.sign(
      { id: user.id, role: user.role, name: user.name, class: user.class, department: user.department, roll_number: user.roll_number },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRES_IN }
    );

    res.json({ token, user: { id: user.id, name: user.name, role: user.role, class: user.class, department: user.department, roll_number: user.roll_number } });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ============ STUDENT ENDPOINTS ============

app.post('/api/student/request', authMiddleware, roleMiddleware('student'), (req, res) => {
  const { type, reason, date, time } = req.body;

  try {
    // Validation
    if (!reason || !date || !time) {
      return res.status(400).json({ error: 'All fields required' });
    }

    const today = new Date().toISOString().split('T')[0];
    if (date < today) {
      return res.status(400).json({ error: 'Cannot apply for past dates' });
    }

    // Check duplicate
    const existing = db.prepare(`
      SELECT * FROM requests 
      WHERE student_id = ? AND leave_date = ? AND status IN ('PENDING_PARENT', 'PENDING_TEACHER', 'PENDING_HOD')
    `).get(req.user.id, date);

    if (existing) {
      return res.status(400).json({ error: 'You already have a pending request for this date' });
    }

    // Get student details
    const student = db.prepare('SELECT * FROM users WHERE id = ?').get(req.user.id);

    // Generate token
    const token = 'TOKEN_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    const tokenExpiry = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString();
    const requestId = 'REQ_' + Date.now();

    const insert = db.prepare(`
      INSERT INTO requests (
        request_id, student_id, student_name, student_roll, student_class, student_department,
        parent_phone, request_type, reason, leave_date, leave_time, expires_at,
        status, parent_token, token_expiry
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    const result = insert.run(
      requestId, req.user.id, student.name, student.roll_number, student.class, student.department,
      student.parent_phone, type, reason, date, time, `${date} ${time}`,
      'PENDING_PARENT', token, tokenExpiry
    );

    res.json({ 
      message: 'Request submitted successfully',
      requestId: requestId,
      id: result.lastInsertRowid,
      parentToken: token
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/student/requests', authMiddleware, roleMiddleware('student'), (req, res) => {
  try {
    const requests = db.prepare('SELECT * FROM requests WHERE student_id = ? ORDER BY submitted_at DESC').all(req.user.id);
    res.json(requests);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/student/cancel/:id', authMiddleware, roleMiddleware('student'), (req, res) => {
  try {
    const request = db.prepare('SELECT * FROM requests WHERE id = ? AND student_id = ?').get(req.params.id, req.user.id);

    if (!request) {
      return res.status(404).json({ error: 'Request not found' });
    }

    if (!['PENDING_PARENT', 'PENDING_TEACHER', 'PENDING_HOD'].includes(request.status)) {
      return res.status(400).json({ error: 'Cannot cancel this request' });
    }

    db.prepare('UPDATE requests SET status = ?, cancelled_at = CURRENT_TIMESTAMP WHERE id = ?')
      .run('CANCELLED_BY_STUDENT', req.params.id);

    res.json({ message: 'Request cancelled successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ============ PARENT ENDPOINTS ============

app.get('/api/parent/request/:token', (req, res) => {
  try {
    const request = db.prepare('SELECT * FROM requests WHERE parent_token = ?').get(req.params.token);

    if (!request) {
      return res.status(404).json({ error: 'Invalid or expired token' });
    }

    if (new Date() > new Date(request.token_expiry)) {
      return res.status(400).json({ error: 'This approval link has expired (24-hour limit)' });
    }

    if (request.token_used) {
      return res.status(400).json({ error: 'This approval link has already been used' });
    }

    res.json(request);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/parent/approve/:token', (req, res) => {
  try {
    const request = db.prepare('SELECT * FROM requests WHERE parent_token = ?').get(req.params.token);

    if (!request) {
      return res.status(404).json({ error: 'Invalid token' });
    }

    if (new Date() > new Date(request.token_expiry)) {
      return res.status(400).json({ error: 'Token expired' });
    }

    if (request.token_used) {
      return res.status(400).json({ error: 'Token already used' });
    }

    db.prepare(`
      UPDATE requests 
      SET status = 'PENDING_TEACHER', parent_status = 'approved', token_used = 1, parent_approved_at = CURRENT_TIMESTAMP
      WHERE parent_token = ?
    `).run(req.params.token);

    res.json({ message: 'Request approved successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/parent/reject/:token', (req, res) => {
  const { reason } = req.body;

  try {
    const request = db.prepare('SELECT * FROM requests WHERE parent_token = ?').get(req.params.token);

    if (!request) {
      return res.status(404).json({ error: 'Invalid token' });
    }

    if (new Date() > new Date(request.token_expiry)) {
      return res.status(400).json({ error: 'Token expired' });
    }

    if (request.token_used) {
      return res.status(400).json({ error: 'Token already used' });
    }

    db.prepare(`
      UPDATE requests 
      SET status = 'REJECTED_BY_PARENT', parent_status = 'rejected', token_used = 1, 
          parent_approved_at = CURRENT_TIMESTAMP, parent_rejection_reason = ?
      WHERE parent_token = ?
    `).run(reason || null, req.params.token);

    res.json({ message: 'Request rejected successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ============ TEACHER ENDPOINTS ============

app.get('/api/teacher/requests/pending', authMiddleware, roleMiddleware('teacher'), (req, res) => {
  try {
    const requests = db.prepare(`
      SELECT * FROM requests 
      WHERE status = 'PENDING_TEACHER' AND student_class = ?
      ORDER BY submitted_at ASC
    `).all(req.user.class);

    res.json(requests);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/teacher/approve/:id', authMiddleware, roleMiddleware('teacher'), (req, res) => {
  try {
    const request = db.prepare('SELECT * FROM requests WHERE id = ?').get(req.params.id);

    if (!request || request.status !== 'PENDING_TEACHER') {
      return res.status(400).json({ error: 'Invalid request' });
    }

    db.prepare(`
      UPDATE requests 
      SET status = 'PENDING_HOD', teacher_status = 'approved', teacher_approved_at = CURRENT_TIMESTAMP
      WHERE id = ?
    `).run(req.params.id);

    res.json({ message: 'Request approved successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/teacher/reject/:id', authMiddleware, roleMiddleware('teacher'), (req, res) => {
  const { reason } = req.body;

  if (!reason) {
    return res.status(400).json({ error: 'Rejection reason required' });
  }

  try {
    const request = db.prepare('SELECT * FROM requests WHERE id = ?').get(req.params.id);

    if (!request || request.status !== 'PENDING_TEACHER') {
      return res.status(400).json({ error: 'Invalid request' });
    }

    db.prepare(`
      UPDATE requests 
      SET status = 'REJECTED_BY_TEACHER', teacher_status = 'rejected', 
          teacher_approved_at = CURRENT_TIMESTAMP, teacher_rejection_reason = ?
      WHERE id = ?
    `).run(reason, req.params.id);

    res.json({ message: 'Request rejected successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ============ HOD ENDPOINTS ============

app.get('/api/hod/requests/pending', authMiddleware, roleMiddleware('hod'), (req, res) => {
  try {
    const requests = db.prepare(`
      SELECT * FROM requests 
      WHERE status = 'PENDING_HOD' AND student_department = ?
      ORDER BY submitted_at ASC
    `).all(req.user.department);

    res.json(requests);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/hod/approve/:id', authMiddleware, roleMiddleware('hod'), (req, res) => {
  try {
    const request = db.prepare('SELECT * FROM requests WHERE id = ?').get(req.params.id);

    if (!request || request.status !== 'PENDING_HOD') {
      return res.status(400).json({ error: 'Invalid request' });
    }

    db.prepare(`
      UPDATE requests 
      SET status = 'APPROVED', hod_status = 'approved', hod_approved_at = CURRENT_TIMESTAMP
      WHERE id = ?
    `).run(req.params.id);

    res.json({ message: 'Request approved successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/hod/reject/:id', authMiddleware, roleMiddleware('hod'), (req, res) => {
  const { reason } = req.body;

  if (!reason) {
    return res.status(400).json({ error: 'Rejection reason required' });
  }

  try {
    const request = db.prepare('SELECT * FROM requests WHERE id = ?').get(req.params.id);

    if (!request || request.status !== 'PENDING_HOD') {
      return res.status(400).json({ error: 'Invalid request' });
    }

    db.prepare(`
      UPDATE requests 
      SET status = 'REJECTED_BY_HOD', hod_status = 'rejected', 
          hod_approved_at = CURRENT_TIMESTAMP, hod_rejection_reason = ?
      WHERE id = ?
    `).run(reason, req.params.id);

    res.json({ message: 'Request rejected successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ============ EXPIRY CHECK JOB ============

setInterval(() => {
  try {
    const now = new Date().toISOString();
    db.prepare(`
      UPDATE requests 
      SET status = 'EXPIRED' 
      WHERE status = 'APPROVED' AND datetime(expires_at) < datetime(?)
    `).run(now);
  } catch (error) {
    console.error('Expiry check error:', error);
  }
}, 60000); // Run every minute

// ============ START SERVER ============

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
});
