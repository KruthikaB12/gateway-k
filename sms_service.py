import os
from twilio.rest import Client

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
COLLEGE_NAME = os.getenv('COLLEGE_NAME', 'College')

# Initialize Twilio client
twilio_client = None
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    try:
        twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        print('✅ Twilio SMS service initialized')
    except Exception as e:
        print(f'⚠️  Twilio initialization failed: {e}')
else:
    print('⚠️  Twilio credentials not configured - SMS disabled')

def send_sms(to_phone, message):
    """Send SMS via Twilio"""
    if not twilio_client:
        print(f'📱 SMS (disabled): To {to_phone}: {message[:50]}...')
        return False
    
    try:
        # Format phone number (add +91 for India if not present)
        if not to_phone.startswith('+'):
            to_phone = '+91' + to_phone
        
        message_obj = twilio_client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone
        )
        print(f'✅ SMS sent to {to_phone}: {message_obj.sid}')
        return True
    except Exception as e:
        print(f'❌ SMS failed to {to_phone}: {e}')
        return False

def send_parent_approval_sms(parent_phone, student_name, request_type, leave_date, leave_time, reason, token):
    """Send approval request SMS to parent"""
    approval_url = f"http://localhost:3000/parent-approve.html?token={token}"
    
    message = f"""{COLLEGE_NAME} Permission Request from {student_name}
Type: {request_type.upper()}
Leave: {leave_date} at {leave_time}
Reason: {reason[:50]}{'...' if len(reason) > 50 else ''}
Approve: {approval_url}"""
    
    return send_sms(parent_phone, message)

def send_approval_notification(phone, student_name, leave_date, leave_time):
    """Send approval confirmation SMS"""
    message = f"""Permission APPROVED for {student_name}
Leave Date: {leave_date}
Leave Time: {leave_time}
Keep this message for gate pass."""
    
    return send_sms(phone, message)

def send_rejection_notification(phone, student_name, rejected_by, reason=None):
    """Send rejection notification SMS"""
    message = f"""Permission REJECTED for {student_name}
Rejected by: {rejected_by}"""
    
    if reason:
        message += f"\nReason: {reason[:100]}"
    
    return send_sms(phone, message)

def send_cancellation_notification(phone, student_name):
    """Send cancellation notification SMS"""
    message = f"""Permission request CANCELLED by {student_name}"""
    return send_sms(phone, message)
