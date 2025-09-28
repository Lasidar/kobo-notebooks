#!/usr/bin/env python3
"""
Comprehensive test runner for the Kobo Notebook App.

This script runs all unit tests and provides detailed reporting.
"""

import unittest
import sys
import os
from pathlib import Path
import time

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def run_test_suite():
    """Run the complete test suite."""
    print("Kobo Notebook App - Comprehensive Test Suite")
    print("=" * 50)
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        descriptions=True,
        failfast=False
    )
    
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Print summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    
    if result.failures:
        print(f"\nFailures ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0] if 'AssertionError: ' in traceback else 'Unknown failure'}")
    
    if result.errors:
        print(f"\nErrors ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\\n')[-2] if '\\n' in traceback else 'Unknown error'}")
    
    # Calculate success rate
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
        print(f"\nSuccess Rate: {success_rate:.1f}%")
        
        if success_rate >= 95:
            print("✓ Excellent test coverage!")
        elif success_rate >= 90:
            print("✓ Good test coverage")
        elif success_rate >= 80:
            print("⚠ Test coverage needs improvement")
        else:
            print("✗ Test coverage is insufficient")
    
    return result.wasSuccessful()


def run_specific_test(test_module):
    """Run a specific test module."""
    print(f"Running {test_module} tests...")
    print("-" * 30)
    
    # Import and run specific test module
    try:
        module = __import__(test_module)
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(module)
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return result.wasSuccessful()
        
    except ImportError as e:
        print(f"Error importing {test_module}: {e}")
        return False


def main():
    """Main test runner function."""
    if len(sys.argv) > 1:
        # Run specific test module
        test_module = sys.argv[1]
        success = run_specific_test(test_module)
    else:
        # Run all tests
        success = run_test_suite()
    
    if success:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed!")
        return 1


if __name__ == '__main__':
    sys.exit(main())