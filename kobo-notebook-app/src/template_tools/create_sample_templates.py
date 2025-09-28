#!/usr/bin/env python3
"""
Script to create sample templates for testing and demonstration.

This script generates various types of notebook templates and saves them
to the templates directory for use with the Kobo Notebook App.
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from template_tools.template_generator import TemplateGenerator
from utils.logger import setup_logger


def create_sample_templates():
    """Create a set of sample templates for testing."""
    logger = setup_logger()
    
    try:
        # Create templates directory
        templates_dir = Path(__file__).parent.parent.parent.parent / "templates"
        templates_dir.mkdir(exist_ok=True)
        
        # Initialize template generator
        generator = TemplateGenerator()
        
        # Create lined templates with different spacing
        logger.info("Creating lined templates...")
        lined_5mm = generator.generate_lined_template(line_spacing=7)
        generator.save_template(lined_5mm, templates_dir / "lined_5mm.png")
        
        lined_7mm = generator.generate_lined_template(line_spacing=10)
        generator.save_template(lined_7mm, templates_dir / "lined_7mm.png")
        
        lined_10mm = generator.generate_lined_template(line_spacing=14)
        generator.save_template(lined_10mm, templates_dir / "lined_10mm.png")
        
        # Create grid templates with different sizes
        logger.info("Creating grid templates...")
        grid_5mm = generator.generate_grid_template(grid_size=7)
        generator.save_template(grid_5mm, templates_dir / "grid_5mm.png")
        
        grid_10mm = generator.generate_grid_template(grid_size=14)
        generator.save_template(grid_10mm, templates_dir / "grid_10mm.png")
        
        # Create dot grid templates
        logger.info("Creating dot grid templates...")
        dot_grid_5mm = generator.generate_dot_grid_template(dot_spacing=7)
        generator.save_template(dot_grid_5mm, templates_dir / "dot_grid_5mm.png")
        
        dot_grid_7mm = generator.generate_dot_grid_template(dot_spacing=10)
        generator.save_template(dot_grid_7mm, templates_dir / "dot_grid_7mm.png")
        
        # Create Cornell note template
        logger.info("Creating Cornell note template...")
        cornell = generator.generate_cornell_template()
        generator.save_template(cornell, templates_dir / "cornell_notes.png")
        
        # Create blank template
        logger.info("Creating blank template...")
        blank = generator.generate_blank_template()
        generator.save_template(blank, templates_dir / "blank.png")
        
        # Create custom lined template with margins
        logger.info("Creating custom lined template...")
        custom_lined = generator.generate_lined_template(
            line_spacing=8,
            margin_top=60,
            margin_bottom=60,
            margin_left=50,
            margin_right=30
        )
        generator.save_template(custom_lined, templates_dir / "custom_lined.png")
        
        logger.info(f"Created {len(list(templates_dir.glob('*.png')))} sample templates in {templates_dir}")
        
        # Print template information
        print("\nSample templates created:")
        for template_file in sorted(templates_dir.glob("*.png")):
            size = template_file.stat().st_size
            print(f"  - {template_file.name} ({size:,} bytes)")
        
    except Exception as e:
        logger.error(f"Error creating sample templates: {e}")
        raise


if __name__ == "__main__":
    create_sample_templates()