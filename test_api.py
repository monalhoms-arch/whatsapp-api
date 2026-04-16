import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"
HEADERS = {
    "X-API-KEY": "my_super_secret_key_123", 
    "Content-Type": "application/json"
}

def run_tests():
    print("========================================")
    print("Testing API Endpoints...")
    print("========================================\n")
    
    # 1. Test Creating Account
    print("1. Account Creation:")
    payload_account = {
        "phone_number": "966500000000",
        "account_type": "customer",
        "is_business_whatsapp": False,
        "name": "Test User"
    }
    try:
        res = requests.post(f"{BASE_URL}/accounts/", json=payload_account, headers=HEADERS)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.json()}\n")
    except Exception as e:
        print(f"Connection Failed: {e}\n")

    # 2. Test Sending Background Notification
    print("2. Notification Engine:")
    payload_notif = {
        "phone_number": "966500000000",
        "message": "Test Message",
        "account_type": "customer"
    }
    res = requests.post(f"{BASE_URL}/notifications/send", json=payload_notif, headers=HEADERS)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.json()}\n")

    # 3. Test Generating OTP
    print("3. OTP Engine:")
    payload_otp = {
        "phone_number": "966500000000",
        "account_type": "customer"
    }
    res = requests.post(f"{BASE_URL}/otp/send", json=payload_otp, headers=HEADERS)
    print(f"Status: {res.status_code}")
    if res.status_code == 200:
        print(f"Response: {res.json()}\n")
    else:
        print(f"Response: {res.text}\n")

    # 4. Test Verifying Wrong OTP to trigger rate limits
    print("4. Security/Rate Limiting (Wrong OTP):")
    payload_verify = {
        "phone_number": "966500000000",
        "code": "000000"
    }
    res = requests.post(f"{BASE_URL}/otp/verify", json=payload_verify, headers=HEADERS)
    print(f"Status: {res.status_code}")
    if res.status_code != 500:
        print(f"Response: {res.json()}\n")
    else:
        print(f"Response: {res.text}\n")

if __name__ == "__main__":
    run_tests()
