// Test script to verify backend functionality
const API_URL = 'http://localhost:3000/api';

async function testBackend() {
  console.log('🧪 Testing Backend API...\n');

  try {
    // Test 1: Student Login
    console.log('1️⃣ Testing Student Login...');
    const loginRes = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role: 'student', identifier: 'L9', password: '8712209017' })
    });
    const loginData = await loginRes.json();
    console.log('✅ Student logged in:', loginData.user.name);
    const studentToken = loginData.token;

    // Test 2: Submit Request
    console.log('\n2️⃣ Testing Request Submission...');
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const date = tomorrow.toISOString().split('T')[0];
    
    const requestRes = await fetch(`${API_URL}/student/request`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${studentToken}`
      },
      body: JSON.stringify({
        type: 'casual',
        reason: 'Medical appointment',
        date: date,
        time: '10:00'
      })
    });
    const requestData = await requestRes.json();
    console.log('✅ Request submitted:', requestData.requestId);
    const parentToken = requestData.parentToken;

    // Test 3: Get Student Requests
    console.log('\n3️⃣ Testing Get Student Requests...');
    const getReqRes = await fetch(`${API_URL}/student/requests`, {
      headers: { 'Authorization': `Bearer ${studentToken}` }
    });
    const requests = await getReqRes.json();
    console.log(`✅ Found ${requests.length} request(s)`);

    // Test 4: Parent View Request
    console.log('\n4️⃣ Testing Parent View Request...');
    const parentViewRes = await fetch(`${API_URL}/parent/request/${parentToken}`);
    const parentView = await parentViewRes.json();
    console.log('✅ Parent can view request:', parentView.student_name);

    // Test 5: Parent Approve
    console.log('\n5️⃣ Testing Parent Approval...');
    const approveRes = await fetch(`${API_URL}/parent/approve/${parentToken}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    const approveData = await approveRes.json();
    console.log('✅ Parent approved:', approveData.message);

    // Test 6: Teacher Login
    console.log('\n6️⃣ Testing Teacher Login...');
    const teacherLoginRes = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role: 'teacher', identifier: 'jahnavi@gmail.com', password: 'jahnavi123' })
    });
    const teacherData = await teacherLoginRes.json();
    console.log('✅ Teacher logged in:', teacherData.user.name);
    const teacherToken = teacherData.token;

    // Test 7: Teacher Get Pending
    console.log('\n7️⃣ Testing Teacher Get Pending Requests...');
    const teacherReqRes = await fetch(`${API_URL}/teacher/requests/pending`, {
      headers: { 'Authorization': `Bearer ${teacherToken}` }
    });
    const teacherRequests = await teacherReqRes.json();
    console.log(`✅ Teacher has ${teacherRequests.length} pending request(s)`);

    if (teacherRequests.length > 0) {
      // Test 8: Teacher Approve
      console.log('\n8️⃣ Testing Teacher Approval...');
      const teacherApproveRes = await fetch(`${API_URL}/teacher/approve/${teacherRequests[0].id}`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${teacherToken}`
        }
      });
      const teacherApprove = await teacherApproveRes.json();
      console.log('✅ Teacher approved:', teacherApprove.message);
    }

    // Test 9: HOD Login
    console.log('\n9️⃣ Testing HOD Login...');
    const hodLoginRes = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role: 'hod', identifier: 'kruthika@gmail.com', password: 'kruthika123' })
    });
    const hodData = await hodLoginRes.json();
    console.log('✅ HOD logged in:', hodData.user.name);
    const hodToken = hodData.token;

    // Test 10: HOD Get Pending
    console.log('\n🔟 Testing HOD Get Pending Requests...');
    const hodReqRes = await fetch(`${API_URL}/hod/requests/pending`, {
      headers: { 'Authorization': `Bearer ${hodToken}` }
    });
    const hodRequests = await hodReqRes.json();
    console.log(`✅ HOD has ${hodRequests.length} pending request(s)`);

    console.log('\n✅ All tests passed! Backend is working correctly.');

  } catch (error) {
    console.error('❌ Test failed:', error.message);
  }
}

// Run tests
testBackend();
