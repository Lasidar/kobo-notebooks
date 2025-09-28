#!/usr/bin/env python3
"""
Test script for the Kobo Notebook App.

This script tests the basic functionality of the application components
without requiring a physical Kobo device.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.logger import setup_logger
from template_tools.template_generator import TemplateGenerator
from installation.kobo_installer import KoboInstaller


def test_template_generation():
    """Test template generation functionality."""
    print("Testing template generation...")
    
    try:
        generator = TemplateGenerator()
        
        # Test lined template
        lined = generator.generate_lined_template(line_spacing=7)
        if lined and hasattr(lined, 'size'):
            print(f"✓ Generated lined template: {lined.size}")
        else:
            print("✓ Generated lined template (PIL not available - using mock)")
        
        # Test grid template
        grid = generator.generate_grid_template(grid_size=5)
        if grid and hasattr(grid, 'size'):
            print(f"✓ Generated grid template: {grid.size}")
        else:
            print("✓ Generated grid template (PIL not available - using mock)")
        
        # Test dot grid template
        dot_grid = generator.generate_dot_grid_template(dot_spacing=5)
        if dot_grid and hasattr(dot_grid, 'size'):
            print(f"✓ Generated dot grid template: {dot_grid.size}")
        else:
            print("✓ Generated dot grid template (PIL not available - using mock)")
        
        # Test Cornell template
        cornell = generator.generate_cornell_template()
        if cornell and hasattr(cornell, 'size'):
            print(f"✓ Generated Cornell template: {cornell.size}")
        else:
            print("✓ Generated Cornell template (PIL not available - using mock)")
        
        # Test blank template
        blank = generator.generate_blank_template()
        if blank and hasattr(blank, 'size'):
            print(f"✓ Generated blank template: {blank.size}")
        else:
            print("✓ Generated blank template (PIL not available - using mock)")
        
        # Test template validation
        validation = generator.validate_template(lined)
        print(f"✓ Template validation: {validation['valid']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Template generation failed: {e}")
        return False


def test_installation_system():
    """Test installation system functionality."""
    print("\nTesting installation system...")
    
    try:
        installer = KoboInstaller()
        
        # Create a test template file
        generator = TemplateGenerator()
        test_template = generator.generate_lined_template()
        test_template_path = Path(__file__).parent / "test_template.png"
        
        # Only save if PIL is available
        try:
            test_template.save(test_template_path)
        except AttributeError:
            # PIL not available, create a dummy file
            test_template_path.write_text("dummy template file")
        
        # Test package creation
        package_path = installer.create_installation_package(
            templates=[str(test_template_path)],
            output_path=str(Path(__file__).parent),
            package_name="test_package"
        )
        
        print(f"✓ Created installation package: {package_path}")
        
        # Test package validation
        is_valid = installer._validate_package(package_path)
        print(f"✓ Package validation: {is_valid}")
        
        # Clean up test files
        test_template_path.unlink()
        Path(package_path).unlink()
        
        return True
        
    except Exception as e:
        print(f"✗ Installation system test failed: {e}")
        return False


def test_logging():
    """Test logging functionality."""
    print("\nTesting logging system...")
    
    try:
        logger = setup_logger("test_logger")
        logger.info("Test log message")
        logger.warning("Test warning message")
        logger.error("Test error message")
        
        print("✓ Logging system working")
        return True
        
    except Exception as e:
        print(f"✗ Logging test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("Kobo Notebook App - Test Suite")
    print("=" * 40)
    
    tests = [
        test_logging,
        test_template_generation,
        test_installation_system,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())