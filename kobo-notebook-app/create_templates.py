#!/usr/bin/env python3
"""
Simple template creation script for the Kobo Notebook App.

This script generates a basic set of templates for testing and demonstration.
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from template_tools.template_generator import TemplateGenerator
from template_tools.advanced_template_generator import AdvancedTemplateGenerator


def create_basic_templates():
    """Create basic template types."""
    print("Creating basic templates...")
    
    # Create templates directory
    templates_dir = Path(__file__).parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    # Initialize generators
    generator = TemplateGenerator()
    advanced_generator = AdvancedTemplateGenerator()
    
    templates_created = []
    
    # Basic templates
    basic_templates = [
        ("Lined 5mm", lambda: generator.generate_lined_template(line_spacing=7)),
        ("Lined 7mm", lambda: generator.generate_lined_template(line_spacing=10)),
        ("Lined 10mm", lambda: generator.generate_lined_template(line_spacing=14)),
        ("Grid 5mm", lambda: generator.generate_grid_template(grid_size=7)),
        ("Grid 10mm", lambda: generator.generate_grid_template(grid_size=14)),
        ("Dot Grid 5mm", lambda: generator.generate_dot_grid_template(dot_spacing=7)),
        ("Dot Grid 7mm", lambda: generator.generate_dot_grid_template(dot_spacing=10)),
        ("Cornell Notes", lambda: generator.generate_cornell_template()),
        ("Blank", lambda: generator.generate_blank_template()),
    ]
    
    for name, generator_func in basic_templates:
        try:
            template = generator_func()
            template_path = templates_dir / f"{name.lower().replace(' ', '_')}.png"
            generator.save_template(template, str(template_path))
            templates_created.append(template_path.name)
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
    
    # Advanced templates
    print("\nCreating advanced templates...")
    advanced_templates = [
        ("Bullet Journal", lambda: advanced_generator.generate_bullet_journal_template()),
        ("Academic Notes", lambda: advanced_generator.generate_academic_notes_template()),
        ("Technical Drawing", lambda: advanced_generator.generate_technical_drawing_template()),
        ("Creative Writing", lambda: advanced_generator.generate_creative_writing_template()),
        ("Meeting Notes", lambda: advanced_generator.generate_meeting_notes_template()),
        ("Mind Map", lambda: advanced_generator.generate_mind_map_template()),
    ]
    
    for name, generator_func in advanced_templates:
        try:
            template = generator_func()
            template_path = templates_dir / f"{name.lower().replace(' ', '_')}.png"
            advanced_generator.save_template(template, str(template_path))
            templates_created.append(template_path.name)
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
    
    print(f"\nTemplate Creation Complete!")
    print(f"Created {len(templates_created)} templates in {templates_dir}")
    
    # Create template manifest
    import json
    manifest = {
        "version": "1.0.0",
        "created": "2024-09-28",
        "total_templates": len(templates_created),
        "templates": {}
    }
    
    for template_file in templates_created:
        template_path = templates_dir / template_file
        if template_path.exists():
            manifest["templates"][template_file] = {
                "filename": template_file,
                "size": template_path.stat().st_size,
                "created": "2024-09-28",
                "category": "generated"
            }
    
    manifest_file = templates_dir / "template_manifest.json"
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"Created template manifest: {manifest_file}")
    
    return templates_created


if __name__ == "__main__":
    create_basic_templates()