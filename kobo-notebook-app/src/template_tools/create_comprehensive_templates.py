#!/usr/bin/env python3
"""
Comprehensive template library creation script.

This script generates a complete library of templates for various use cases
including academic notes, creative writing, technical drawing, and more.
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from .template_generator import TemplateGenerator
from .advanced_template_generator import AdvancedTemplateGenerator
from ..utils.logger import setup_logger


def create_basic_templates(generator, templates_dir):
    """Create basic template types."""
    print("Creating basic templates...")
    
    basic_templates = [
        # Lined templates with different spacing
        ("Lined 5mm", lambda: generator.generate_lined_template(line_spacing=7)),
        ("Lined 7mm", lambda: generator.generate_lined_template(line_spacing=10)),
        ("Lined 10mm", lambda: generator.generate_lined_template(line_spacing=14)),
        ("Lined 15mm", lambda: generator.generate_lined_template(line_spacing=21)),
        
        # Grid templates with different sizes
        ("Grid 5mm", lambda: generator.generate_grid_template(grid_size=7)),
        ("Grid 10mm", lambda: generator.generate_grid_template(grid_size=14)),
        ("Grid 15mm", lambda: generator.generate_grid_template(grid_size=21)),
        
        # Dot grid templates
        ("Dot Grid 5mm", lambda: generator.generate_dot_grid_template(dot_spacing=7)),
        ("Dot Grid 7mm", lambda: generator.generate_dot_grid_template(dot_spacing=10)),
        ("Dot Grid 10mm", lambda: generator.generate_dot_grid_template(dot_spacing=14)),
        
        # Cornell notes
        ("Cornell Notes", lambda: generator.generate_cornell_template()),
        
        # Blank template
        ("Blank", lambda: generator.generate_blank_template()),
    ]
    
    created_templates = []
    
    for name, generator_func in basic_templates:
        try:
            template = generator_func()
            template_path = templates_dir / f"{name.lower().replace(' ', '_')}.png"
            generator.save_template(template, str(template_path))
            created_templates.append(template_path.name)
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
    
    return created_templates


def create_advanced_templates(advanced_generator, templates_dir):
    """Create advanced/specialized templates."""
    print("\nCreating advanced templates...")
    
    advanced_templates = [
        # Bullet journal templates
        ("Bullet Journal Basic", lambda: advanced_generator.generate_bullet_journal_template()),
        ("Bullet Journal Compact", lambda: advanced_generator.generate_bullet_journal_template(
            dot_spacing=4, header_height=80, footer_height=60
        )),
        
        # Academic templates
        ("Academic Notes", lambda: advanced_generator.generate_academic_notes_template()),
        ("Academic Notes Wide", lambda: advanced_generator.generate_academic_notes_template(
            sidebar_width=150, line_spacing=10
        )),
        
        # Technical drawing templates
        ("Technical Drawing 5mm", lambda: advanced_generator.generate_technical_drawing_template(
            grid_size=7
        )),
        ("Technical Drawing 10mm", lambda: advanced_generator.generate_technical_drawing_template(
            grid_size=14
        )),
        ("Technical Drawing 20mm", lambda: advanced_generator.generate_technical_drawing_template(
            grid_size=28
        )),
        
        # Creative writing templates
        ("Creative Writing", lambda: advanced_generator.generate_creative_writing_template()),
        ("Creative Writing Wide", lambda: advanced_generator.generate_creative_writing_template(
            line_spacing=12, margin_left=60
        )),
        
        # Meeting notes templates
        ("Meeting Notes", lambda: advanced_generator.generate_meeting_notes_template()),
        ("Meeting Notes Compact", lambda: advanced_generator.generate_meeting_notes_template(
            line_spacing=6, header_height=100
        )),
        
        # Mind map templates
        ("Mind Map 6 Branches", lambda: advanced_generator.generate_mind_map_template(branches=6)),
        ("Mind Map 8 Branches", lambda: advanced_generator.generate_mind_map_template(branches=8)),
        ("Mind Map 12 Branches", lambda: advanced_generator.generate_mind_map_template(branches=12)),
    ]
    
    created_templates = []
    
    for name, generator_func in advanced_templates:
        try:
            template = generator_func()
            template_path = templates_dir / f"{name.lower().replace(' ', '_')}.png"
            advanced_generator.save_template(template, str(template_path))
            created_templates.append(template_path.name)
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
    
    return created_templates


def create_specialized_templates(generator, advanced_generator, templates_dir):
    """Create specialized templates for specific use cases."""
    print("\nCreating specialized templates...")
    
    specialized_templates = [
        # Language learning templates
        ("Language Learning", lambda: generator.generate_lined_template(
            line_spacing=8, margin_left=60, margin_right=60
        )),
        
        # Music notation templates
        ("Music Staff", lambda: generator.generate_lined_template(
            line_spacing=12, margin_top=100, margin_bottom=100
        )),
        
        # Recipe templates
        ("Recipe Card", lambda: generator.generate_lined_template(
            line_spacing=10, margin_top=80, margin_bottom=80
        )),
        
        # Journal templates
        ("Daily Journal", lambda: generator.generate_lined_template(
            line_spacing=9, margin_top=60, margin_bottom=60
        )),
        
        # Study templates
        ("Study Notes", lambda: advanced_generator.generate_academic_notes_template(
            line_spacing=7, sidebar_width=120
        )),
        
        # Project planning templates
        ("Project Planning", lambda: advanced_generator.generate_meeting_notes_template(
            line_spacing=8, header_height=140
        )),
    ]
    
    created_templates = []
    
    for name, generator_func in specialized_templates:
        try:
            template = generator_func()
            template_path = templates_dir / f"{name.lower().replace(' ', '_')}.png"
            generator.save_template(template, str(template_path))
            created_templates.append(template_path.name)
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
    
    return created_templates


def create_template_categories(templates_dir):
    """Create organized template categories."""
    print("\nOrganizing templates into categories...")
    
    categories = {
        "basic": [
            "lined_5mm.png", "lined_7mm.png", "lined_10mm.png", "lined_15mm.png",
            "grid_5mm.png", "grid_10mm.png", "grid_15mm.png",
            "dot_grid_5mm.png", "dot_grid_7mm.png", "dot_grid_10mm.png",
            "cornell_notes.png", "blank.png"
        ],
        "academic": [
            "academic_notes.png", "academic_notes_wide.png", "study_notes.png"
        ],
        "creative": [
            "creative_writing.png", "creative_writing_wide.png",
            "mind_map_6_branches.png", "mind_map_8_branches.png", "mind_map_12_branches.png"
        ],
        "professional": [
            "meeting_notes.png", "meeting_notes_compact.png",
            "project_planning.png"
        ],
        "technical": [
            "technical_drawing_5mm.png", "technical_drawing_10mm.png", "technical_drawing_20mm.png"
        ],
        "journaling": [
            "bullet_journal_basic.png", "bullet_journal_compact.png",
            "daily_journal.png"
        ],
        "specialized": [
            "language_learning.png", "music_staff.png", "recipe_card.png"
        ]
    }
    
    # Create category directories
    for category in categories.keys():
        category_dir = templates_dir / category
        category_dir.mkdir(exist_ok=True)
        print(f"  ✓ Created category: {category}")
    
    return categories


def create_template_manifest(templates_dir, all_templates):
    """Create a manifest file for all templates."""
    print("\nCreating template manifest...")
    
    manifest = {
        "version": "1.0.0",
        "created": "2024-09-28",
        "total_templates": len(all_templates),
        "categories": {
            "basic": "Standard lined, grid, and dot grid templates",
            "academic": "Templates optimized for academic note-taking",
            "creative": "Templates for creative writing and brainstorming",
            "professional": "Templates for business and professional use",
            "technical": "Templates for technical drawings and diagrams",
            "journaling": "Templates for personal journaling and planning",
            "specialized": "Templates for specific use cases"
        },
        "templates": {}
    }
    
    # Add template information
    for template_file in all_templates:
        template_path = templates_dir / template_file
        if template_path.exists():
            template_info = {
                "filename": template_file,
                "size": template_path.stat().st_size,
                "created": "2024-09-28",
                "category": "basic",  # Default category
                "description": f"Template: {template_file.replace('_', ' ').replace('.png', '')}"
            }
            
            # Determine category based on filename
            for category, files in {
                "academic": ["academic", "study"],
                "creative": ["creative", "mind_map"],
                "professional": ["meeting", "project"],
                "technical": ["technical"],
                "journaling": ["bullet", "journal"],
                "specialized": ["language", "music", "recipe"]
            }.items():
                if any(keyword in template_file.lower() for keyword in files):
                    template_info["category"] = category
                    break
            
            manifest["templates"][template_file] = template_info
    
    # Save manifest
    import json
    manifest_file = templates_dir / "template_manifest.json"
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"  ✓ Created manifest with {len(all_templates)} templates")
    return manifest


def main():
    """Create comprehensive template library."""
    print("Kobo Notebook App - Comprehensive Template Library Creator")
    print("=" * 60)
    
    # Setup logging
    logger = setup_logger()
    logger.info("Starting comprehensive template library creation")
    
    # Create templates directory
    templates_dir = Path(__file__).parent.parent.parent.parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    # Initialize generators
    generator = TemplateGenerator()
    advanced_generator = AdvancedTemplateGenerator()
    
    all_templates = []
    
    try:
        # Create basic templates
        basic_templates = create_basic_templates(generator, templates_dir)
        all_templates.extend(basic_templates)
        
        # Create advanced templates
        advanced_templates = create_advanced_templates(advanced_generator, templates_dir)
        all_templates.extend(advanced_templates)
        
        # Create specialized templates
        specialized_templates = create_specialized_templates(generator, advanced_generator, templates_dir)
        all_templates.extend(specialized_templates)
        
        # Organize into categories
        categories = create_template_categories(templates_dir)
        
        # Create manifest
        manifest = create_template_manifest(templates_dir, all_templates)
        
        # Summary
        print(f"\nTemplate Library Creation Complete!")
        print(f"=" * 40)
        print(f"Total templates created: {len(all_templates)}")
        print(f"Categories: {len(categories)}")
        print(f"Location: {templates_dir}")
        
        print(f"\nTemplate Categories:")
        for category, description in manifest["categories"].items():
            count = len([t for t in all_templates if any(keyword in t.lower() for keyword in 
                {"academic": ["academic", "study"], "creative": ["creative", "mind_map"],
                 "professional": ["meeting", "project"], "technical": ["technical"],
                 "journaling": ["bullet", "journal"], "specialized": ["language", "music", "recipe"]}.get(category, []))])
            print(f"  {category.capitalize()}: {count} templates - {description}")
        
        print(f"\nSample templates:")
        for template in sorted(all_templates)[:10]:
            print(f"  - {template}")
        if len(all_templates) > 10:
            print(f"  ... and {len(all_templates) - 10} more")
        
        logger.info(f"Template library creation completed successfully: {len(all_templates)} templates")
        
    except Exception as e:
        logger.error(f"Error creating template library: {e}")
        print(f"\nError: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())