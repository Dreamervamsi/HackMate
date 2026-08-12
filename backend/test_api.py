import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
    print(f"{'='*60}\n")

def test_root_endpoint():
    """Test the root endpoint"""
    print("Testing Root Endpoint...")
    response = requests.get(f"{API_BASE_URL}/")
    print_response("Root Endpoint Response", response)
    return response.status_code == 200

def test_health_check():
    """Test the health check endpoint"""
    print("Testing Health Check...")
    response = requests.get(f"{API_BASE_URL}/health")
    print_response("Health Check Response", response)
    return response.status_code == 200

def test_get_agents():
    """Test the get agents endpoint"""
    print("Testing Get Agents...")
    response = requests.get(f"{API_BASE_URL}/agents")
    print_response("Active Agents Response", response)
    return response.status_code == 200

def test_orchestrate():
    """Test the orchestration endpoint"""
    print("Testing Orchestration Endpoint...")
    
    test_prompt = "Create a simple function that adds two numbers in Python"
    
    payload = {
        "user_prompt": test_prompt,
        "context": {
            "test": True,
            "language": "python"
        },
        "priority": "normal"
    }
    
    print(f"Sending orchestration request: {test_prompt}")
    start_time = time.time()
    
    response = requests.post(
        f"{API_BASE_URL}/orchestrate",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    execution_time = time.time() - start_time
    print(f"Request completed in {execution_time:.2f} seconds")
    
    print_response("Orchestration Response", response)
    return response.status_code == 200

def test_invalid_request():
    """Test with invalid request to test error handling"""
    print("Testing Invalid Request (Error Handling)...")
    
    # Missing user_prompt
    payload = {
        "context": {"test": True}
    }
    
    response = requests.post(
        f"{API_BASE_URL}/orchestrate",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print_response("Invalid Request Response", response)
    return response.status_code == 400

def main():
    """Run all tests"""
    print(f"Starting API Tests against {API_BASE_URL}")
    print(f"{'='*60}\n")
    
    tests = [
        ("Root Endpoint", test_root_endpoint),
        ("Health Check", test_health_check),
        ("Get Agents", test_get_agents),
        ("Orchestration", test_orchestrate),
        ("Error Handling", test_invalid_request)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"Error running {test_name}: {e}")
            results.append((test_name, False))
        time.sleep(1)  # Small delay between tests
    
    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()