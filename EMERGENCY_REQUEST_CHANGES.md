# Emergency Request Auto-Approval Changes

## What Changed

Emergency requests now **auto-approve** after parent approval, bypassing teacher and HOD approval requirements.

## New Workflow

### Emergency Requests:
1. Student submits emergency request
2. Parent receives email
3. **Parent approves → IMMEDIATELY APPROVED** ✅
4. Student and parent receive approval notification
5. Teachers and HODs can still **view** these requests (read-only)

### Casual Requests (unchanged):
1. Student submits casual request
2. Parent approves → goes to Teacher
3. Teacher approves → goes to HOD
4. HOD approves → final approval

## Technical Changes

### Backend (server.py)

#### 1. Parent Approval Endpoint (`/api/parent/approve/{token}`)
- Checks if `request_type == 'Emergency'`
- If emergency: Sets status to `APPROVED` and auto-fills teacher/HOD approvals
- If casual: Normal flow to `PENDING_TEACHER`
- Sends approval notification emails for emergency requests

#### 2. Teacher View (`/api/teacher/requests/pending`)
- Shows `PENDING_TEACHER` casual requests (actionable)
- Shows `APPROVED` emergency requests (view-only for tracking)
- Ordered by most recent first

#### 3. HOD View (`/api/hod/requests/pending`)
- Shows `PENDING_HOD` casual requests (actionable)
- Shows `APPROVED` emergency requests (view-only for tracking)
- Ordered by most recent first

### Frontend (front_gate.html)

#### 1. Teacher Dashboard (`loadTeacherRequests()`)
- Detects emergency + approved status
- Shows green border and "AUTO-APPROVED" badge
- Hides approve/reject buttons for emergency requests
- Displays "view only" message

#### 2. HOD Dashboard (`loadHODRequests()`)
- Same visual treatment as teacher dashboard
- Shows emergency requests for tracking purposes

#### 3. Student Dashboard
- Shows "✅ Auto" for teacher/HOD status on emergency requests
- Flow diagram reflects auto-approval

## Database Status Values

Emergency requests after parent approval:
```
status: 'APPROVED'
parent_status: 'approved'
teacher_status: 'auto_approved'
hod_status: 'auto_approved'
```

## Visual Indicators

Emergency auto-approved requests show:
- Green border (`border: 2px solid #27ae60`)
- Light green background (`background: #d4edda`)
- "AUTO-APPROVED" badge (green with white text)
- "view only" message
- No action buttons

## Benefits

- Emergency situations get immediate approval
- Parents have full control for emergencies
- Teachers/HODs maintain visibility for safety tracking
- Reduces approval delays for urgent situations
- Clear visual distinction between actionable and informational requests
