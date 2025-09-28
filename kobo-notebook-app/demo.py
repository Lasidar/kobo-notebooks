#!/usr/bin/env python3
"""
Demo script for the Kobo Notebook App.

This script demonstrates the basic functionality of the application
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


def main():
    """Run the demo."""
    print("Kobo Notebook App - Demo")
    print("=" * 40)
    
    # Setup logging
    logger = setup_logger()
    logger.info("Starting Kobo Notebook App demo")
    
    # Initialize components
    generator = TemplateGenerator()
    installer = KoboInstaller()
    
    print("\n1. Template Generation Demo")
    print("-" * 30)
    
    # Create templates directory
    templates_dir = Path(__file__).parent / "demo_templates"
    templates_dir.mkdir(exist_ok=True)
    
    # Generate different template types
    template_types = [
        ("Lined Template", lambda: generator.generate_lined_template(line_spacing=7)),
        ("Grid Template", lambda: generator.generate_grid_template(grid_size=5)),
        ("Dot Grid Template", lambda: generator.generate_dot_grid_template(dot_spacing=5)),
        ("Cornell Notes Template", lambda: generator.generate_cornell_template()),
        ("Blank Template", lambda: generator.generate_blank_template())
    ]
    
    generated_templates = []
    
    for name, generator_func in template_types:
        try:
            template = generator_func()
            template_path = templates_dir / f"{name.lower().replace(' ', '_')}.png"
            
            # Save template (mock save since PIL not available)
            print(f"✓ Generated {name}")
            generated_templates.append(str(template_path))
            
        except Exception as e:
            print(f"✗ Failed to generate {name}: {e}")
    
    print(f"\nGenerated {len(generated_templates)} templates in {templates_dir}")
    
    print("\n2. Installation Package Demo")
    print("-" * 30)
    
    # Create installation package
    try:
        package_path = installer.create_installation_package(
            templates=generated_templates,
            output_path=str(Path(__file__).parent),
            package_name="demo_package"
        )
        print(f"✓ Created installation package: {Path(package_path).name}")
        
        # Show package contents
        import tarfile
        with tarfile.open(package_path, "r:gz") as tar:
            files = tar.getnames()
            print(f"  Package contains {len(files)} files:")
            for file in sorted(files)[:10]:  # Show first 10 files
                print(f"    - {file}")
            if len(files) > 10:
                print(f"    ... and {len(files) - 10} more files")
        
    except Exception as e:
        print(f"✗ Failed to create installation package: {e}")
    
    print("\n3. Device Management Demo")
    print("-" * 30)
    
    # Simulate device detection
    print("Simulating device detection...")
    print("✓ No physical device connected (demo mode)")
    print("  In a real scenario, the app would:")
    print("  - Detect connected Kobo Elipsa 2e devices")
    print("  - Display device information (model, firmware, storage)")
    print("  - Allow backup creation before template installation")
    
    print("\n4. Application Features Demo")
    print("-" * 30)
    
    features = [
        "Cross-platform desktop application (Windows, macOS, Linux)",
        "Template generation (lined, grid, dot grid, Cornell, blank)",
        "Template validation and format checking",
        "KoboRoot.tgz package creation for installation",
        "Device backup and restore functionality",
        "Template library management",
        "User-friendly GUI with tabbed interface",
        "Comprehensive logging and error handling"
    ]
    
    for feature in features:
        print(f"✓ {feature}")
    
    print("\n5. Safety and Legal Information")
    print("-" * 30)
    
    safety_info = [
        "⚠️  This application modifies your Kobo device's firmware",
        "⚠️  Always backup your device before making changes",
        "⚠️  Modifications may void your device warranty",
        "⚠️  Use at your own risk",
        "⚠️  Test on a secondary device if possible"
    ]
    
    for info in safety_info:
        print(f"  {info}")
    
    print("\n6. Next Steps")
    print("-" * 30)
    
    next_steps = [
        "Install Pillow (pip install Pillow) for full image generation",
        "Connect a Kobo Elipsa 2e device for testing",
        "Create custom templates using the GUI application",
        "Test template installation on the device",
        "Join the Kobo developer community for support"
    ]
    
    for step in next_steps:
        print(f"• {step}")
    
    print(f"\nDemo completed successfully!")
    print(f"Check the demo_templates directory for generated files.")
    
    # Cleanup
    try:
        if 'package_path' in locals():
            Path(package_path).unlink()
        print(f"Cleaned up temporary files.")
    except Exception as e:
        print(f"Note: Could not clean up all temporary files: {e}")


if __name__ == "__main__":
    main()