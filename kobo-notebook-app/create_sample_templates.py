#!/usr/bin/env python3
"""
Create sample template files for demonstration.

This script creates placeholder template files to demonstrate the
template library structure without requiring PIL.
"""

import os
import json
from pathlib import Path
from datetime import datetime


def create_sample_templates():
    """Create sample template files."""
    print("Creating sample template files...")
    
    # Create templates directory
    templates_dir = Path(__file__).parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    # Create subdirectories
    categories = ["basic", "academic", "creative", "professional", "technical", "journaling", "specialized"]
    for category in categories:
        (templates_dir / category).mkdir(exist_ok=True)
    
    # Sample templates
    templates = [
        # Basic templates
        ("basic", "lined_5mm.png", "Lined 5mm", "Standard lined paper with 5mm spacing"),
        ("basic", "lined_7mm.png", "Lined 7mm", "Standard lined paper with 7mm spacing"),
        ("basic", "lined_10mm.png", "Lined 10mm", "Standard lined paper with 10mm spacing"),
        ("basic", "grid_5mm.png", "Grid 5mm", "5mm grid paper for technical drawings"),
        ("basic", "grid_10mm.png", "Grid 10mm", "10mm grid paper for general use"),
        ("basic", "dot_grid_5mm.png", "Dot Grid 5mm", "5mm dot grid for flexible layouts"),
        ("basic", "dot_grid_7mm.png", "Dot Grid 7mm", "7mm dot grid for bullet journaling"),
        ("basic", "cornell_notes.png", "Cornell Notes", "Cornell note-taking system"),
        ("basic", "blank.png", "Blank", "Clean blank page"),
        
        # Academic templates
        ("academic", "academic_notes.png", "Academic Notes", "Structured notes with keyword sidebar"),
        ("academic", "study_notes.png", "Study Notes", "Optimized for study sessions"),
        ("academic", "lecture_notes.png", "Lecture Notes", "Template for lecture note-taking"),
        
        # Creative templates
        ("creative", "creative_writing.png", "Creative Writing", "Template for creative writing"),
        ("creative", "mind_map_6.png", "Mind Map 6", "Mind map with 6 branches"),
        ("creative", "mind_map_8.png", "Mind Map 8", "Mind map with 8 branches"),
        ("creative", "story_planning.png", "Story Planning", "Template for story development"),
        
        # Professional templates
        ("professional", "meeting_notes.png", "Meeting Notes", "Structured meeting notes"),
        ("professional", "project_planning.png", "Project Planning", "Project management template"),
        ("professional", "business_notes.png", "Business Notes", "Professional note-taking"),
        
        # Technical templates
        ("technical", "technical_drawing_5mm.png", "Technical Drawing 5mm", "5mm grid for technical drawings"),
        ("technical", "technical_drawing_10mm.png", "Technical Drawing 10mm", "10mm grid for technical drawings"),
        ("technical", "circuit_diagram.png", "Circuit Diagram", "Template for circuit diagrams"),
        
        # Journaling templates
        ("journaling", "bullet_journal.png", "Bullet Journal", "Complete bullet journal layout"),
        ("journaling", "daily_journal.png", "Daily Journal", "Daily journaling template"),
        ("journaling", "weekly_planner.png", "Weekly Planner", "Weekly planning template"),
        
        # Specialized templates
        ("specialized", "language_learning.png", "Language Learning", "Template for language study"),
        ("specialized", "music_staff.png", "Music Staff", "Musical notation template"),
        ("specialized", "recipe_card.png", "Recipe Card", "Recipe writing template"),
    ]
    
    created_templates = []
    
    for category, filename, name, description in templates:
        try:
            # Create placeholder file
            template_path = templates_dir / category / filename
            with open(template_path, 'w') as f:
                f.write(f"# {name}\n")
                f.write(f"# {description}\n")
                f.write(f"# Created: {datetime.now().isoformat()}\n")
                f.write(f"# Size: 1404 x 1872 pixels\n")
                f.write(f"# Format: PNG\n")
                f.write(f"# This is a placeholder file for demonstration.\n")
                f.write(f"# In a real implementation, this would be a PNG image.\n")
            
            created_templates.append({
                "filename": filename,
                "category": category,
                "name": name,
                "description": description,
                "path": str(template_path),
                "size": template_path.stat().st_size,
                "created": datetime.now().isoformat()
            })
            
            print(f"  ✓ {category}/{filename}")
            
        except Exception as e:
            print(f"  ✗ {category}/{filename}: {e}")
    
    # Create template manifest
    manifest = {
        "version": "1.0.0",
        "created": datetime.now().isoformat(),
        "total_templates": len(created_templates),
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
    
    for template in created_templates:
        manifest["templates"][template["filename"]] = {
            "filename": template["filename"],
            "category": template["category"],
            "name": template["name"],
            "description": template["description"],
            "size": template["size"],
            "created": template["created"]
        }
    
    # Save manifest
    manifest_file = templates_dir / "template_manifest.json"
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\nTemplate Library Creation Complete!")
    print(f"=" * 40)
    print(f"Total templates created: {len(created_templates)}")
    print(f"Categories: {len(categories)}")
    print(f"Location: {templates_dir}")
    
    print(f"\nTemplate Categories:")
    for category, description in manifest["categories"].items():
        count = len([t for t in created_templates if t["category"] == category])
        print(f"  {category.capitalize()}: {count} templates - {description}")
    
    print(f"\nSample templates:")
    for template in created_templates[:10]:
        print(f"  - {template['category']}/{template['filename']}: {template['name']}")
    if len(created_templates) > 10:
        print(f"  ... and {len(created_templates) - 10} more")
    
    print(f"\nCreated template manifest: {manifest_file}")
    
    return created_templates


if __name__ == "__main__":
    create_sample_templates()