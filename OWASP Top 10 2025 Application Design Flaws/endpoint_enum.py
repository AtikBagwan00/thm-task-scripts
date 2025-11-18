#!/usr/bin/env python3
"""
Enumerate SecureChat endpoints and test for insecure design
"""

import requests
import json

BASE_URL = "http://10.201.116.248:5005"

# Different user agents
user_agents = {
    "Desktop": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "iPhone": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
    "Android": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36",
}

# Common endpoints to test
endpoints = [
    "/",
    "/api",
    "/api/",
    "/api/messages",
    "/api/chat",
    "/api/user",
    "/api/users",
    "/api/admin",
    "/api/login",
    "/api/auth",
    "/api/register",
    "/api/config",
    "/api/settings",
    "/api/profile",
    "/admin",
    "/admin/",
    "/admin/login",
    "/dashboard",
    "/messages",
    "/chat",
    "/users",
    "/config",
    "/settings",
    "/debug",
    "/test",
    "/mobile",
    "/app",
    "/desktop",
    "/web",
    "/.env",
    "/config.json",
    "/api/v1",
    "/api/v2",
    "/swagger",
    "/docs",
    "/api-docs",
]

# HTTP methods to test
methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"]

print("=" * 80)
print("SecureChat Endpoint Enumeration")
print("=" * 80)

found_endpoints = []

# Test 1: Endpoint enumeration with different user agents
print("\n[*] Phase 1: Testing endpoints with different User-Agents...")
print("-" * 80)

for ua_name, ua_string in user_agents.items():
    print(f"\n[*] Testing with {ua_name} User-Agent...")
    
    for endpoint in endpoints:
        url = BASE_URL + endpoint
        headers = {"User-Agent": ua_string}
        
        try:
            response = requests.get(url, headers=headers, timeout=3)
            
            if response.status_code != 404:
                result = {
                    "endpoint": endpoint,
                    "user_agent": ua_name,
                    "status": response.status_code,
                    "length": len(response.text),
                    "preview": response.text[:200]
                }
                found_endpoints.append(result)
                
                print(f"  [+] {endpoint}")
                print(f"      Status: {response.status_code}")
                print(f"      Length: {len(response.text)} bytes")
                
                if response.status_code == 200:
                    print(f"      Preview: {response.text[:150]}")
                
        except requests.exceptions.RequestException:
            pass

# Test 2: Test different HTTP methods
print("\n" + "=" * 80)
print("[*] Phase 2: Testing different HTTP methods on found endpoints...")
print("-" * 80)

test_endpoints = ["/", "/api", "/admin", "/messages"]
headers = {"User-Agent": user_agents["iPhone"]}

for endpoint in test_endpoints:
    url = BASE_URL + endpoint
    print(f"\n[*] Testing {endpoint}:")
    
    for method in methods:
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=3)
            elif method == "POST":
                response = requests.post(url, headers=headers, json={}, timeout=3)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json={}, timeout=3)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=3)
            elif method == "OPTIONS":
                response = requests.options(url, headers=headers, timeout=3)
            elif method == "HEAD":
                response = requests.head(url, headers=headers, timeout=3)
            elif method == "PATCH":
                response = requests.patch(url, headers=headers, json={}, timeout=3)
            
            if response.status_code not in [404, 405]:
                print(f"  [{method}] Status: {response.status_code}")
                if response.text:
                    print(f"         Response: {response.text[:100]}")
                
                # Check headers for interesting info
                if 'Allow' in response.headers:
                    print(f"         Allowed: {response.headers['Allow']}")
                    
        except requests.exceptions.RequestException:
            pass

# Test 3: Test with different headers
print("\n" + "=" * 80)
print("[*] Phase 3: Testing with special headers...")
print("-" * 80)

special_headers = [
    {"X-Forwarded-For": "127.0.0.1"},
    {"X-Original-URL": "/admin"},
    {"X-Rewrite-URL": "/admin"},
    {"X-Custom-IP-Authorization": "127.0.0.1"},
    {"X-Originating-IP": "127.0.0.1"},
    {"X-Remote-IP": "127.0.0.1"},
    {"X-Client-IP": "127.0.0.1"},
    {"Referer": "http://10.201.116.248:5005/mobile-app"},
    {"X-App-Version": "1.0.0"},
    {"X-Device-Type": "mobile"},
]

base_headers = {"User-Agent": user_agents["iPhone"]}

for test_header in special_headers:
    headers = {**base_headers, **test_header}
    
    try:
        response = requests.get(BASE_URL, headers=headers, timeout=3)
        
        if len(response.text) != 3057:  # Different from default response
            print(f"\n[!] Different response with header: {test_header}")
            print(f"    Status: {response.status_code}")
            print(f"    Length: {len(response.text)} bytes")
            print(f"    Preview: {response.text[:200]}")
    except:
        pass

# Test 4: Check robots.txt and common files
print("\n" + "=" * 80)
print("[*] Phase 4: Checking common files...")
print("-" * 80)

common_files = [
    "/robots.txt",
    "/.git/config",
    "/.env",
    "/backup.zip",
    "/config.json",
    "/settings.json",
    "/package.json",
    "/composer.json",
    "/.DS_Store",
    "/web.config",
]

for file_path in common_files:
    url = BASE_URL + file_path
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            print(f"  [+] Found: {file_path}")
            print(f"      Content: {response.text[:200]}")
    except:
        pass

# Summary
print("\n" + "=" * 80)
print("SUMMARY OF FOUND ENDPOINTS:")
print("=" * 80)

if found_endpoints:
    for result in found_endpoints:
        print(f"\n[+] {result['endpoint']}")
        print(f"    User-Agent: {result['user_agent']}")
        print(f"    Status: {result['status']}")
        print(f"    Length: {result['length']} bytes")
else:
    print("\n[!] No additional endpoints found beyond main page")
    print("[!] The vulnerability might be in client-side logic or")
    print("    accessible through different request methods/headers")

print("\n" + "=" * 80)
print("[*] Enumeration Complete!")
print("=" * 80)