#!/usr/bin/env python3
import requests
import json

# Test login
login_url = 'http://localhost:5000/api/teacher/login'
login_data = {
    'username': 't..bhaskar',
    'password': 'NkEZ48De'
}

print("Testing login...")
response = requests.post(login_url, json=login_data)
print(f"Login Status: {response.status_code}")
print(f"Login Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 200:
    token = response.json()['access_token']
    print(f"\nToken received: {token[:50]}...")

    # Test protected endpoint
    profile_url = 'http://localhost:5000/api/teacher/profile'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    print("\nTesting profile endpoint...")
    profile_response = requests.get(profile_url, headers=headers)
    print(f"Profile Status: {profile_response.status_code}")
    print(f"Profile Response: {json.dumps(profile_response.json(), indent=2)}")

    # Test timetable endpoint
    timetable_url = 'http://localhost:5000/api/teacher/timetable'
    print("\nTesting timetable endpoint...")
    timetable_response = requests.get(timetable_url, headers=headers)
    print(f"Timetable Status: {timetable_response.status_code}")
    print(f"Timetable Response: {json.dumps(timetable_response.json(), indent=2)}")
