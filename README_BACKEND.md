# Student Gateway Permission System - Backend

## Setup Instructions

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment
Edit `.env` file and set your JWT secret:
```
JWT_SECRET=your-secure-secret-key
```

### 3. Start Server
```bash
npm start
```

For development with auto-reload:
```bash
npm run dev
```

Server will run on `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login for all roles

### Student
- `POST /api/student/request` - Submit permission request
- `GET /api/student/requests` - Get all student requests
- `POST /api/student/cancel/:id` - Cancel pending request

### Parent
- `GET /api/parent/request/:token` - View request via token
- `POST /api/parent/approve/:token` - Approve request
- `POST /api/parent/reject/:token` - Reject request

### Teacher
- `GET /api/teacher/requests/pending` - Get pending requests for class
- `POST /api/teacher/approve/:id` - Approve request
- `POST /api/teacher/reject/:id` - Reject request (requires reason)

### HOD
- `GET /api/hod/requests/pending` - Get pending requests for department
- `POST /api/hod/approve/:id` - Approve request
- `POST /api/hod/reject/:id` - Reject request (requires reason)

## Default Users

### Students
- Roll: `L9`, Password: `8712209017`
- Roll: `CS101`, Password: `1234567890`

### Teachers
- Email: `jahnavi@gmail.com`, Password: `jahnavi123`
- Email: `teacher@school.com`, Password: `teacher123`

### HODs
- Email: `kruthika@gmail.com`, Password: `kruthika123`
- Email: `hod@school.com`, Password: `hod123`

## Database

Uses SQLite (`gateway.db`) for simplicity. Database is auto-created on first run.

## Features Implemented

✅ JWT Authentication
✅ Role-based access control
✅ Password hashing (bcrypt)
✅ Token-based parent approval (24-hour expiry, one-time use)
✅ Class/Department filtering
✅ Rejection reason capture
✅ Complete audit trail with timestamps
✅ Auto-expiry job (runs every minute)
✅ Duplicate request prevention

## Next Steps

To connect frontend:
1. Update `front_gate.html` to call these API endpoints
2. Store JWT token in localStorage
3. Send token in Authorization header: `Bearer <token>`
