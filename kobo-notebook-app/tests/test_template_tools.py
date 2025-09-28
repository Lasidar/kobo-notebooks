#!/usr/bin/env python3
"""
Unit tests for template tools modules.

This module contains comprehensive unit tests for template generation,
management, and advanced template features.
"""

import unittest
import tempfile
import os
import shutil
from pathlib import Path
import sys
import json

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from template_tools.template_generator import TemplateGenerator
from template_tools.advanced_template_generator import AdvancedTemplateGenerator
from template_tools.template_manager import TemplateManager


class TestTemplateGenerator(unittest.TestCase):
    """Test the basic template generator."""
    
    def setUp(self):
        """Set up test environment."""
        self.generator = TemplateGenerator()
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_generator_creation(self):
        """Test template generator creation."""
        self.assertIsNotNone(self.generator)
        self.assertEqual(self.generator.DEVICE_WIDTH, 1404)
        self.assertEqual(self.generator.DEVICE_HEIGHT, 1872)
        self.assertEqual(self.generator.DPI, 300)
    
    def test_generate_lined_template(self):
        """Test lined template generation."""
        template = self.generator.generate_lined_template()
        self.assertIsNotNone(template)
        
        # Test with custom parameters
        template2 = self.generator.generate_lined_template(
            line_spacing=10,
            margin_top=60,
            margin_bottom=60,
            margin_left=50,
            margin_right=50,
            line_color="#FF0000"
        )
        self.assertIsNotNone(template2)
    
    def test_generate_grid_template(self):
        """Test grid template generation."""
        template = self.generator.generate_grid_template()
        self.assertIsNotNone(template)
        
        # Test with custom parameters
        template2 = self.generator.generate_grid_template(
            grid_size=10,
            margin_top=60,
            margin_bottom=60,
            margin_left=50,
            margin_right=50,
            grid_color="#0000FF"
        )
        self.assertIsNotNone(template2)
    
    def test_generate_dot_grid_template(self):
        """Test dot grid template generation."""
        template = self.generator.generate_dot_grid_template()
        self.assertIsNotNone(template)
        
        # Test with custom parameters
        template2 = self.generator.generate_dot_grid_template(
            dot_spacing=10,
            margin_top=60,
            margin_bottom=60,
            margin_left=50,
            margin_right=50,
            dot_color="#00FF00",
            dot_size=2
        )
        self.assertIsNotNone(template2)
    
    def test_generate_cornell_template(self):
        """Test Cornell template generation."""
        template = self.generator.generate_cornell_template()
        self.assertIsNotNone(template)
        
        # Test with custom parameters
        template2 = self.generator.generate_cornell_template(
            line_spacing=10,
            margin_top=60,
            margin_bottom=60,
            margin_left=50,
            margin_right=50,
            note_width_ratio=0.8,
            cue_width_ratio=0.15,
            summary_height_ratio=0.2,
            line_color="#800080"
        )
        self.assertIsNotNone(template2)
    
    def test_generate_blank_template(self):
        """Test blank template generation."""
        template = self.generator.generate_blank_template()
        self.assertIsNotNone(template)
    
    def test_save_template(self):
        """Test template saving."""
        template = self.generator.generate_blank_template()
        template_path = os.path.join(self.test_dir, "test_template.png")
        
        self.generator.save_template(template, template_path)
        self.assertTrue(os.path.exists(template_path))
    
    def test_create_template_from_image_nonexistent(self):
        """Test template creation from non-existent image."""
        with self.assertRaises(Exception):
            self.generator.create_template_from_image("/nonexistent/image.png")
    
    def test_validate_template(self):
        """Test template validation."""
        template = self.generator.generate_blank_template()
        validation = self.generator.validate_template(template)
        
        self.assertIsInstance(validation, dict)
        self.assertIn('valid', validation)
        self.assertIn('warnings', validation)
        self.assertIn('errors', validation)
        self.assertIsInstance(validation['warnings'], list)
        self.assertIsInstance(validation['errors'], list)


class TestAdvancedTemplateGenerator(unittest.TestCase):
    """Test the advanced template generator."""
    
    def setUp(self):
        """Set up test environment."""
        self.generator = AdvancedTemplateGenerator()
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_generator_creation(self):
        """Test advanced template generator creation."""
        self.assertIsNotNone(self.generator)
        # Should inherit from TemplateGenerator
        self.assertEqual(self.generator.DEVICE_WIDTH, 1404)
        self.assertEqual(self.generator.DEVICE_HEIGHT, 1872)
    
    def test_generate_bullet_journal_template(self):
        """Test bullet journal template generation."""
        template = self.generator.generate_bullet_journal_template()
        self.assertIsNotNone(template)
        
        # Test with custom parameters
        template2 = self.generator.generate_bullet_journal_template(
            dot_spacing=7,
            margin_top=60,
            margin_bottom=60,
            margin_left=50,
            margin_right=50,
            header_height=120,
            footer_height=100
        )
        self.assertIsNotNone(template2)
    
    def test_generate_academic_notes_template(self):
        """Test academic notes template generation."""
        template = self.generator.generate_academic_notes_template()
        self.assertIsNotNone(template)
        
        # Test with custom parameters
        template2 = self.generator.generate_academic_notes_template(
            line_spacing=10,
            margin_top=60,
            margin_bottom=60,
            margin_left=50,
            margin_right=50,
            sidebar_width=120
        )
        self.assertIsNotNone(template2)
    
    def test_generate_technical_drawing_template(self):
        """Test technical drawing template generation."""
        template = self.generator.generate_technical_drawing_template()
        self.assertIsNotNone(template)
        
        # Test with custom parameters
        template2 = self.generator.generate_technical_drawing_template(
            grid_size=10,
            margin_top=60,
            margin_bottom=60,
            margin_left=50,
            margin_right=50,
            title_height=80
        )
        self.assertIsNotNone(template2)
    
    def test_generate_creative_writing_template(self):
        """Test creative writing template generation."""
        template = self.generator.generate_creative_writing_template()
        self.assertIsNotNone(template)
        
        # Test with custom parameters
        template2 = self.generator.generate_creative_writing_template(
            line_spacing=12,
            margin_top=60,
            margin_bottom=60,
            margin_left=50,
            margin_right=50,
            header_height=100
        )
        self.assertIsNotNone(template2)
    
    def test_generate_meeting_notes_template(self):
        """Test meeting notes template generation."""
        template = self.generator.generate_meeting_notes_template()
        self.assertIsNotNone(template)
        
        # Test with custom parameters
        template2 = self.generator.generate_meeting_notes_template(
            line_spacing=10,
            margin_top=60,
            margin_bottom=60,
            margin_left=50,
            margin_right=50,
            header_height=140
        )
        self.assertIsNotNone(template2)
    
    def test_generate_mind_map_template(self):
        """Test mind map template generation."""
        template = self.generator.generate_mind_map_template()
        self.assertIsNotNone(template)
        
        # Test with custom parameters
        template2 = self.generator.generate_mind_map_template(
            center_x=700,
            center_y=936,
            radius=250,
            branches=10
        )
        self.assertIsNotNone(template2)


class TestTemplateManager(unittest.TestCase):
    """Test the template manager."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.manager = TemplateManager(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_manager_creation(self):
        """Test template manager creation."""
        self.assertIsNotNone(self.manager)
        self.assertEqual(str(self.manager.templates_dir), self.test_dir)
    
    def test_get_template_info_nonexistent(self):
        """Test getting template info for non-existent file."""
        result = self.manager.get_template_info(Path("/nonexistent/file.png"))
        self.assertEqual(result, {})
    
    def test_get_template_info_existing(self):
        """Test getting template info for existing file."""
        # Create a test file
        test_file = os.path.join(self.test_dir, "test_template.png")
        with open(test_file, 'w') as f:
            f.write("test content")
        
        info = self.manager.get_template_info(Path(test_file))
        
        self.assertIn('filename', info)
        self.assertIn('path', info)
        self.assertIn('size', info)
        self.assertIn('created', info)
        self.assertIn('modified', info)
        self.assertIn('hash', info)
        self.assertIn('extension', info)
        self.assertIn('category', info)
        
        self.assertEqual(info['filename'], 'test_template.png')
        self.assertEqual(info['extension'], '.png')
    
    def test_determine_category(self):
        """Test category determination."""
        self.assertEqual(self.manager._determine_category("lined_5mm.png"), "lined")
        self.assertEqual(self.manager._determine_category("grid_template.png"), "grid")
        self.assertEqual(self.manager._determine_category("dot_grid.png"), "dot_grid")
        self.assertEqual(self.manager._determine_category("cornell_notes.png"), "cornell")
        self.assertEqual(self.manager._determine_category("blank.png"), "blank")
        self.assertEqual(self.manager._determine_category("academic_notes.png"), "academic")
        self.assertEqual(self.manager._determine_category("creative_writing.png"), "creative")
        self.assertEqual(self.manager._determine_category("meeting_notes.png"), "professional")
        self.assertEqual(self.manager._determine_category("technical_drawing.png"), "technical")
        self.assertEqual(self.manager._determine_category("bullet_journal.png"), "journaling")
        self.assertEqual(self.manager._determine_category("unknown.png"), "other")
    
    def test_list_templates_empty(self):
        """Test listing templates in empty directory."""
        templates = self.manager.list_templates()
        self.assertIsInstance(templates, list)
        self.assertEqual(len(templates), 0)
    
    def test_list_templates_with_files(self):
        """Test listing templates with files."""
        # Create test template files
        test_files = [
            "lined_5mm.png",
            "grid_10mm.jpg",
            "dot_grid_7mm.jpeg"
        ]
        
        for filename in test_files:
            filepath = os.path.join(self.test_dir, filename)
            with open(filepath, 'w') as f:
                f.write("test content")
        
        templates = self.manager.list_templates()
        self.assertIsInstance(templates, list)
        self.assertEqual(len(templates), 3)
        
        # Check that all files are included
        template_names = [t['filename'] for t in templates]
        for filename in test_files:
            self.assertIn(filename, template_names)
    
    def test_list_templates_with_category_filter(self):
        """Test listing templates with category filter."""
        # Create test template files
        test_files = [
            "lined_5mm.png",
            "grid_10mm.png",
            "dot_grid_7mm.png"
        ]
        
        for filename in test_files:
            filepath = os.path.join(self.test_dir, filename)
            with open(filepath, 'w') as f:
                f.write("test content")
        
        # Filter by lined category
        lined_templates = self.manager.list_templates("lined")
        self.assertEqual(len(lined_templates), 1)
        self.assertEqual(lined_templates[0]['filename'], "lined_5mm.png")
        
        # Filter by grid category
        grid_templates = self.manager.list_templates("grid")
        self.assertEqual(len(grid_templates), 1)
        self.assertEqual(grid_templates[0]['filename'], "grid_10mm.png")
    
    def test_export_template_nonexistent(self):
        """Test exporting non-existent template."""
        with self.assertRaises(FileNotFoundError):
            self.manager.export_template("/nonexistent/template.png")
    
    def test_export_template_existing(self):
        """Test exporting existing template."""
        # Create a test template file
        test_file = os.path.join(self.test_dir, "test_template.png")
        with open(test_file, 'w') as f:
            f.write("test content")
        
        export_path = self.manager.export_template(test_file)
        self.assertTrue(os.path.exists(export_path))
        
        # Check that metadata file was created
        metadata_path = export_path.replace('.png', '.json')
        self.assertTrue(os.path.exists(metadata_path))
        
        # Check metadata content
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        self.assertIn('filename', metadata)
        self.assertIn('size', metadata)
        self.assertIn('created', metadata)
    
    def test_import_template(self):
        """Test importing template."""
        # Create a test template file
        source_file = os.path.join(self.test_dir, "source_template.png")
        with open(source_file, 'w') as f:
            f.write("test content")
        
        imported_path = self.manager.import_template(source_file)
        self.assertTrue(os.path.exists(imported_path))
        
        # Check content
        with open(imported_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, "test content")
    
    def test_import_template_with_target_name(self):
        """Test importing template with target name."""
        # Create a test template file
        source_file = os.path.join(self.test_dir, "source_template.png")
        with open(source_file, 'w') as f:
            f.write("test content")
        
        imported_path = self.manager.import_template(source_file, "target_template.png")
        self.assertTrue(os.path.exists(imported_path))
        self.assertEqual(os.path.basename(imported_path), "target_template.png")
    
    def test_validate_template_nonexistent(self):
        """Test validating non-existent template."""
        result = self.manager.validate_template("/nonexistent/template.png")
        
        self.assertFalse(result['valid'])
        self.assertIn('File does not exist', result['errors'])
    
    def test_validate_template_existing(self):
        """Test validating existing template."""
        # Create a test template file
        test_file = os.path.join(self.test_dir, "test_template.png")
        with open(test_file, 'w') as f:
            f.write("test content")
        
        result = self.manager.validate_template(test_file)
        
        self.assertIsInstance(result, dict)
        self.assertIn('valid', result)
        self.assertIn('warnings', result)
        self.assertIn('errors', result)
        self.assertIsInstance(result['warnings'], list)
        self.assertIsInstance(result['errors'], list)
    
    def test_delete_template_nonexistent(self):
        """Test deleting non-existent template."""
        result = self.manager.delete_template("/nonexistent/template.png")
        self.assertFalse(result)
    
    def test_delete_template_existing(self):
        """Test deleting existing template."""
        # Create a test template file
        test_file = os.path.join(self.test_dir, "test_template.png")
        with open(test_file, 'w') as f:
            f.write("test content")
        
        result = self.manager.delete_template(test_file)
        self.assertTrue(result)
        
        # Check that file was moved to trash
        trash_dir = self.manager.templates_dir / "trash"
        self.assertTrue(trash_dir.exists())
        
        # Check that there's a file in trash
        trash_files = list(trash_dir.glob("*"))
        self.assertGreater(len(trash_files), 0)


if __name__ == '__main__':
    unittest.main()