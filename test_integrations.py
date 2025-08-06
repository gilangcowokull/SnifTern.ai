#!/usr/bin/env python3
"""
Test script for SnifTern.ai integrations
Tests LinkedIn, Indeed, and Glassdoor integrations
"""

import requests
import json
import time

# Test configuration
BASE_URL = "http://localhost:5000"

def test_linkedin_integration():
    """Test LinkedIn integration"""
    print("🔗 Testing LinkedIn Integration...")
    
    # Sample LinkedIn job URL (you can replace with a real one)
    test_url = "https://www.linkedin.com/jobs/view/software-engineer-intern-at-google-1234567890"
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze_linkedin",
            headers={'Content-Type': 'application/json'},
            json={'linkedin_url': test_url},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ LinkedIn Integration: SUCCESS")
            print(f"   Result: {data.get('result', 'N/A')}")
            print(f"   Confidence: {data.get('confidence_score', 'N/A')}%")
            print(f"   Words: {data.get('word_count', 'N/A')}")
            return True
        else:
            data = response.json()
            print(f"❌ LinkedIn Integration: FAILED")
            print(f"   Error: {data.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ LinkedIn Integration: ERROR - {str(e)}")
        return False

def test_indeed_integration():
    """Test Indeed integration"""
    print("\n🔍 Testing Indeed Integration...")
    
    # Sample Indeed job URL (you can replace with a real one)
    test_url = "https://www.indeed.com/viewjob?jk=1234567890abcdef"
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze_indeed",
            headers={'Content-Type': 'application/json'},
            json={'indeed_url': test_url},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Indeed Integration: SUCCESS")
            print(f"   Result: {data.get('result', 'N/A')}")
            print(f"   Confidence: {data.get('confidence_score', 'N/A')}%")
            print(f"   Words: {data.get('word_count', 'N/A')}")
            return True
        else:
            data = response.json()
            print(f"❌ Indeed Integration: FAILED")
            print(f"   Error: {data.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Indeed Integration: ERROR - {str(e)}")
        return False

def test_glassdoor_integration():
    """Test Glassdoor integration"""
    print("\n🏢 Testing Glassdoor Integration...")
    
    # Sample Glassdoor job URL (you can replace with a real one)
    test_url = "https://www.glassdoor.com/Job/software-engineer-intern-jobs-SRCH_IL.0,23_KO24,50.htm"
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze_glassdoor",
            headers={'Content-Type': 'application/json'},
            json={'glassdoor_url': test_url},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Glassdoor Integration: SUCCESS")
            print(f"   Result: {data.get('result', 'N/A')}")
            print(f"   Confidence: {data.get('confidence_score', 'N/A')}%")
            print(f"   Words: {data.get('word_count', 'N/A')}")
            return True
        else:
            data = response.json()
            print(f"❌ Glassdoor Integration: FAILED")
            print(f"   Error: {data.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Glassdoor Integration: ERROR - {str(e)}")
        return False

def test_basic_detection():
    """Test basic job detection functionality"""
    print("\n🧪 Testing Basic Job Detection...")
    
    # Sample fake job posting
    fake_job_text = """
    We are looking for a remote data entry specialist. No experience required. 
    You can work from home and earn $50-100 per hour. Immediate start available. 
    Please send your personal information including bank details and credit card information. 
    This is an urgent opportunity with limited time. Certificate will be provided for a small fee.
    """
    
    try:
        response = requests.post(
            f"{BASE_URL}/detect",
            headers={'Content-Type': 'application/json'},
            json={'text': fake_job_text},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Basic Detection: SUCCESS")
            print(f"   Result: {data.get('result', 'N/A')}")
            print(f"   Confidence: {data.get('confidence_score', 'N/A')}%")
            print(f"   Words: {data.get('word_count', 'N/A')}")
            return True
        else:
            data = response.json()
            print(f"❌ Basic Detection: FAILED")
            print(f"   Error: {data.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Basic Detection: ERROR - {str(e)}")
        return False

def test_company_search():
    """Test company search functionality"""
    print("\n🏢 Testing Company Search...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/search_company",
            headers={'Content-Type': 'application/json'},
            json={'company_name': 'fakecorp'},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Company Search: SUCCESS")
            print(f"   Found: {data.get('found', 'N/A')}")
            if data.get('found'):
                print(f"   Company: {data.get('company_data', {}).get('name', 'N/A')}")
                print(f"   Fraud Score: {data.get('company_data', {}).get('fraud_score', 'N/A')}/100")
            return True
        else:
            data = response.json()
            print(f"❌ Company Search: FAILED")
            print(f"   Error: {data.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Company Search: ERROR - {str(e)}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 SnifTern.ai Integration Tests")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not responding properly")
            return
    except:
        print("❌ Server is not running. Please start the Flask app first:")
        print("   python app.py")
        return
    
    print("✅ Server is running")
    
    # Run tests
    results = []
    
    results.append(test_basic_detection())
    results.append(test_company_search())
    results.append(test_linkedin_integration())
    results.append(test_indeed_integration())
    results.append(test_glassdoor_integration())
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Integrations are working correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        print("\n💡 Troubleshooting Tips:")
        print("   1. Make sure the Flask app is running")
        print("   2. Check if all dependencies are installed")
        print("   3. Verify that the model files exist in the model/ directory")
        print("   4. Some job platforms may block automated access")
        print("   5. Try with different job URLs")

if __name__ == "__main__":
    main() 