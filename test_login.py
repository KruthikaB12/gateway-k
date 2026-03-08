import requests
import json

# Test Google OAuth endpoint
url = "http://127.0.0.1:8080/api/auth/google"

# Create a mock token with email
mock_token = json.dumps({"email": "25wh1a05g5@bvrithyderabad.edu.in", "name": "Test Student"})
import base64
encoded = base64.b64encode(mock_token.encode()).decode()

payload = {"token": f"header.{encoded}.signature"}

try:
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
