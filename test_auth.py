#!/usr/bin/env python3
"""
Test Script for Social Authentication
Verifies that all authentication features are working correctly
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"  # Change to production URL for prod testing
HEADERS = {"Content-Type": "application/json"}

def print_test(test_name, passed):
    """Print test result"""
    status = "✅ PASSED" if passed else "❌ FAILED"
    print(f"{status}: {test_name}")

def test_homepage():
    """Test if homepage loads"""
    try:
        response = requests.get(f"{BASE_URL}/")
        passed = response.status_code == 200
        print_test("Homepage loads", passed)
        return passed
    except Exception as e:
        print_test(f"Homepage loads - Error: {e}", False)
        return False

def test_static_files():
    """Test if static files are accessible"""
    files_to_test = [
        "/static/css/style.css",
        "/static/js/app.js",
        "/static/js/social_auth.js"
    ]
    
    all_passed = True
    for file_path in files_to_test:
        try:
            response = requests.get(f"{BASE_URL}{file_path}")
            passed = response.status_code == 200
            print_test(f"Static file: {file_path}", passed)
            all_passed = all_passed and passed
        except Exception as e:
            print_test(f"Static file: {file_path} - Error: {e}", False)
            all_passed = False
    
    return all_passed

def test_auth_check():
    """Test authentication check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/auth/check")
        passed = response.status_code == 200
        data = response.json()
        print_test("Auth check endpoint", passed)
        print(f"  └─ Authenticated: {data.get('authenticated', False)}")
        return passed
    except Exception as e:
        print_test(f"Auth check endpoint - Error: {e}", False)
        return False

def test_demo_google_auth():
    """Test demo Google authentication"""
    try:
        payload = {
            "token": "demo-google-token-for-testing"
        }
        response = requests.post(
            f"{BASE_URL}/auth/google",
            headers=HEADERS,
            json=payload
        )
        
        passed = response.status_code == 200
        if passed:
            data = response.json()
            passed = data.get("success", False) and data.get("demo_mode", False)
            print_test("Demo Google authentication", passed)
            if passed:
                print(f"  └─ User: {data.get('user', {}).get('name', 'Unknown')}")
                print(f"  └─ Email: {data.get('user', {}).get('email', 'Unknown')}")
        else:
            print_test("Demo Google authentication", False)
        
        return passed
    except Exception as e:
        print_test(f"Demo Google authentication - Error: {e}", False)
        return False

def test_demo_linkedin_auth():
    """Test demo LinkedIn authentication"""
    try:
        payload = {
            "email": "test@example.com",
            "name": "Test User",
            "linkedin_id": "test123",
            "picture": ""
        }
        response = requests.post(
            f"{BASE_URL}/auth/linkedin",
            headers=HEADERS,
            json=payload
        )
        
        passed = response.status_code == 200
        if passed:
            data = response.json()
            passed = data.get("success", False) and data.get("demo_mode", False)
            print_test("Demo LinkedIn authentication", passed)
            if passed:
                print(f"  └─ User: {data.get('user', {}).get('name', 'Unknown')}")
                print(f"  └─ Email: {data.get('user', {}).get('email', 'Unknown')}")
        else:
            print_test("Demo LinkedIn authentication", False)
        
        return passed
    except Exception as e:
        print_test(f"Demo LinkedIn authentication - Error: {e}", False)
        return False

def test_api_endpoints():
    """Test other API endpoints"""
    endpoints = [
        ("/api/careers", "GET"),
        ("/api/skills", "GET")
    ]
    
    all_passed = True
    for endpoint, method in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}")
            else:
                response = requests.post(f"{BASE_URL}{endpoint}", headers=HEADERS)
            
            passed = response.status_code in [200, 201]
            print_test(f"API endpoint: {method} {endpoint}", passed)
            all_passed = all_passed and passed
        except Exception as e:
            print_test(f"API endpoint: {method} {endpoint} - Error: {e}", False)
            all_passed = False
    
    return all_passed

def main():
    """Run all tests"""
    print("="*60)
    print("🧪 CAREER ADVISOR MVP - AUTHENTICATION TEST SUITE")
    print("="*60)
    print(f"Testing URL: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*60)
    
    tests = [
        ("Homepage", test_homepage),
        ("Static Files", test_static_files),
        ("Auth Check", test_auth_check),
        ("Demo Google Auth", test_demo_google_auth),
        ("Demo LinkedIn Auth", test_demo_linkedin_auth),
        ("API Endpoints", test_api_endpoints)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Testing: {test_name}")
        print("-"*40)
        result = test_func()
        results.append((test_name, result))
        time.sleep(0.5)  # Small delay between tests
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✅" if passed else "❌"
        print(f"{status} {test_name}")
    
    print("-"*60)
    print(f"Results: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("🎉 ALL TESTS PASSED! The application is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed_count == total_count

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
