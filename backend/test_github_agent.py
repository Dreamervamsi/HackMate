"""
Test file for GitHub Agent functionality
Tests the GitHub branch creation and code push operations
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents import create_github_branch, commit_and_push_to_github, parse_github_repo_url

def test_parse_github_repo_url():
    """Test parsing of various GitHub URL formats"""
    print("Testing GitHub URL parsing...")
    
    test_cases = [
        ("https://github.com/owner/repo", ("owner", "repo")),
        ("https://github.com/owner/repo.git", ("owner", "repo")),
        ("github.com/owner/repo", ("owner", "repo")),
        ("https://github.com/myusername/myproject", ("myusername", "myproject")),
    ]
    
    for url, expected in test_cases:
        try:
            result = parse_github_repo_url(url)
            if result == expected:
                print(f"✓ PASS: {url} -> {result}")
            else:
                print(f"✗ FAIL: {url} -> {result} (expected {expected})")
        except Exception as e:
            print(f"✗ ERROR: {url} -> {str(e)}")
    
    # Test invalid URL
    try:
        parse_github_repo_url("invalid-url")
        print("✗ FAIL: Invalid URL should raise error")
    except ValueError:
        print("✓ PASS: Invalid URL correctly raises ValueError")
    except Exception as e:
        print(f"✗ ERROR: Invalid URL raised unexpected error: {str(e)}")

def test_github_branch_creation():
    """Test GitHub branch creation (requires valid credentials)"""
    print("\nTesting GitHub branch creation...")
    
    load_dotenv()
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        print("⚠ SKIP: GITHUB_TOKEN not set in environment variables")
        print("  Set GITHUB_TOKEN in .env file to test GitHub operations")
        return
    
    # Test with a sample repository (replace with your test repo)
    test_repo = "https://github.com/your-username/your-repo"  # Replace with actual test repo
    test_branch = "test-branch-automation"
    
    print(f"Attempting to create branch '{test_branch}' in {test_repo}")
    
    result = create_github_branch(
        repo_url=test_repo,
        branch_name=test_branch,
        base_branch="main",
        github_token=github_token
    )
    
    if result.get("success"):
        print(f"✓ PASS: Branch created successfully")
        print(f"  Branch URL: {result.get('branch_url')}")
    else:
        print(f"✗ FAIL: Branch creation failed")
        print(f"  Error: {result.get('error')}")
        print(f"  Note: This might be expected if the repository doesn't exist or token is invalid")

def test_github_commit_and_push():
    """Test GitHub commit and push operations (requires valid credentials)"""
    print("\nTesting GitHub commit and push...")
    
    load_dotenv()
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        print("⚠ SKIP: GITHUB_TOKEN not set in environment variables")
        print("  Set GITHUB_TOKEN in .env file to test GitHub operations")
        return
    
    # Test with a sample repository (replace with your test repo)
    test_repo = "https://github.com/your-username/your-repo"  # Replace with actual test repo
    test_branch = "test-branch-automation"
    
    # Sample files to commit
    test_files = {
        "test_file.txt": "This is a test file created by GitHub agent",
        "test_folder/test.py": "print('Hello from GitHub agent!')"
    }
    
    print(f"Attempting to commit {len(test_files)} files to {test_branch} in {test_repo}")
    
    result = commit_and_push_to_github(
        repo_url=test_repo,
        branch_name=test_branch,
        files=test_files,
        commit_message="Test commit from GitHub agent",
        github_token=github_token
    )
    
    if result.get("success"):
        print(f"✓ PASS: Files committed successfully")
        print(f"  Commit SHA: {result.get('commit_sha')}")
        print(f"  Files committed: {result.get('files_committed')}")
        print(f"  Branch URL: {result.get('branch_url')}")
    else:
        print(f"✗ FAIL: Commit operation failed")
        print(f"  Error: {result.get('error')}")
        print(f"  Note: This might be expected if the branch doesn't exist or token is invalid")

def test_error_handling():
    """Test error handling for invalid inputs"""
    print("\nTesting error handling...")
    
    # Test branch creation without token
    result = create_github_branch(
        repo_url="https://github.com/owner/repo",
        branch_name="test-branch"
    )
    
    if not result.get("success") and "token" in result.get("error", "").lower():
        print("✓ PASS: Correctly handles missing token")
    else:
        print("✗ FAIL: Should fail gracefully without token")
    
    # Test commit with invalid repo URL
    result = commit_and_push_to_github(
        repo_url="invalid-repo-url",
        branch_name="test-branch",
        files={"test.txt": "content"},
        commit_message="test"
    )
    
    if not result.get("success"):
        print("✓ PASS: Correctly handles invalid repository URL")
    else:
        print("✗ FAIL: Should fail with invalid repository URL")

def main():
    """Run all tests"""
    print("="*60)
    print("GitHub Agent Functionality Tests")
    print("="*60)
    
    # Run tests that don't require credentials
    test_parse_github_repo_url()
    test_error_handling()
    
    # Run tests that require credentials (will skip if not available)
    print("\n" + "="*60)
    print("Tests requiring GitHub credentials")
    print("="*60)
    test_github_branch_creation()
    test_github_commit_and_push()
    
    print("\n" + "="*60)
    print("Test suite completed")
    print("="*60)

if __name__ == "__main__":
    main()