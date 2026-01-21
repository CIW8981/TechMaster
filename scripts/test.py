#!/usr/bin/env python3
"""
Comprehensive test script that runs all validation and build checks.
"""
import subprocess
import sys
import os

def run_command(description: str, command: list) -> bool:
    """Run a command and return success status."""
    print(f"\n{'=' * 60}")
    print(f"Running: {description}")
    print(f"{'=' * 60}")
    
    try:
        result = subprocess.run(command, check=True)
        print(f"✅ {description} - PASSED")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        return False

def main():
    """Run all tests."""
    # Change to project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    print("=" * 60)
    print("Running All Tests")
    print("=" * 60)
    
    results = []
    
    # Run content validation
    results.append(run_command(
        "Content Validation",
        ["python", "scripts/validate.py"]
    ))
    
    # Run build test
    results.append(run_command(
        "Build Test",
        ["python", "scripts/build.py"]
    ))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    
    if all(results):
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
