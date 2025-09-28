#!/usr/bin/env python3
"""
API tests for the Kobo Notebook App.

This module contains integration tests that verify the API contracts
and interfaces between different components of the application.
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
from installation.kobo_installer import KoboInstaller
from installation.advanced_installer import AdvancedInstaller
from utils.device_manager import DeviceManager
from utils.device_diagnostics import DeviceDiagnostics
from utils.logger import setup_logger


class TestTemplateGenerationAPI(unittest.TestCase):
    """Test the template generation API contracts."""
    
    def setUp(self):
        """Set up test environment."""
        self.generator = TemplateGenerator()
        self.advanced_generator = AdvancedTemplateGenerator()
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_template_generator_api(self):
        """Test basic template generator API."""
        # Test that all required methods exist
        self.assertTrue(hasattr(self.generator, 'generate_lined_template'))
        self.assertTrue(hasattr(self.generator, 'generate_grid_template'))
        self.assertTrue(hasattr(self.generator, 'generate_dot_grid_template'))
        self.assertTrue(hasattr(self.generator, 'generate_cornell_template'))
        self.assertTrue(hasattr(self.generator, 'generate_blank_template'))
        self.assertTrue(hasattr(self.generator, 'save_template'))
        self.assertTrue(hasattr(self.generator, 'validate_template'))
        
        # Test that methods are callable
        self.assertTrue(callable(self.generator.generate_lined_template))
        self.assertTrue(callable(self.generator.generate_grid_template))
        self.assertTrue(callable(self.generator.generate_dot_grid_template))
        self.assertTrue(callable(self.generator.generate_cornell_template))
        self.assertTrue(callable(self.generator.generate_blank_template))
        self.assertTrue(callable(self.generator.save_template))
        self.assertTrue(callable(self.generator.validate_template))
    
    def test_advanced_template_generator_api(self):
        """Test advanced template generator API."""
        # Test that all required methods exist
        self.assertTrue(hasattr(self.advanced_generator, 'generate_bullet_journal_template'))
        self.assertTrue(hasattr(self.advanced_generator, 'generate_academic_notes_template'))
        self.assertTrue(hasattr(self.advanced_generator, 'generate_technical_drawing_template'))
        self.assertTrue(hasattr(self.advanced_generator, 'generate_creative_writing_template'))
        self.assertTrue(hasattr(self.advanced_generator, 'generate_meeting_notes_template'))
        self.assertTrue(hasattr(self.advanced_generator, 'generate_mind_map_template'))
        
        # Test that methods are callable
        self.assertTrue(callable(self.advanced_generator.generate_bullet_journal_template))
        self.assertTrue(callable(self.advanced_generator.generate_academic_notes_template))
        self.assertTrue(callable(self.advanced_generator.generate_technical_drawing_template))
        self.assertTrue(callable(self.advanced_generator.generate_creative_writing_template))
        self.assertTrue(callable(self.advanced_generator.generate_meeting_notes_template))
        self.assertTrue(callable(self.advanced_generator.generate_mind_map_template))
    
    def test_template_parameter_validation(self):
        """Test template parameter validation."""
        # Test with valid parameters
        template = self.generator.generate_lined_template(line_spacing=10)
        self.assertIsNotNone(template)
        
        # Test with edge case parameters
        template = self.generator.generate_lined_template(line_spacing=1)
        self.assertIsNotNone(template)
        
        template = self.generator.generate_lined_template(line_spacing=100)
        self.assertIsNotNone(template)
    
    def test_template_save_api(self):
        """Test template save API."""
        template = self.generator.generate_blank_template()
        template_path = os.path.join(self.test_dir, "test_template.png")
        
        # Test save with default parameters
        self.generator.save_template(template, template_path)
        self.assertTrue(os.path.exists(template_path))
        
        # Test save with custom format
        template_path2 = os.path.join(self.test_dir, "test_template.jpg")
        self.generator.save_template(template, template_path2, format="JPEG")
        self.assertTrue(os.path.exists(template_path2))
    
    def test_template_validation_api(self):
        """Test template validation API."""
        template = self.generator.generate_blank_template()
        
        # Test validation
        validation_result = self.generator.validate_template(template)
        
        # Check API contract
        self.assertIsInstance(validation_result, dict)
        self.assertIn('valid', validation_result)
        self.assertIn('warnings', validation_result)
        self.assertIn('errors', validation_result)
        self.assertIsInstance(validation_result['warnings'], list)
        self.assertIsInstance(validation_result['errors'], list)


class TestTemplateManagerAPI(unittest.TestCase):
    """Test the template manager API contracts."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.manager = TemplateManager(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_template_manager_api(self):
        """Test template manager API."""
        # Test that all required methods exist
        self.assertTrue(hasattr(self.manager, 'get_template_info'))
        self.assertTrue(hasattr(self.manager, 'list_templates'))
        self.assertTrue(hasattr(self.manager, 'export_template'))
        self.assertTrue(hasattr(self.manager, 'import_template'))
        self.assertTrue(hasattr(self.manager, 'validate_template'))
        self.assertTrue(hasattr(self.manager, 'delete_template'))
        
        # Test that methods are callable
        self.assertTrue(callable(self.manager.get_template_info))
        self.assertTrue(callable(self.manager.list_templates))
        self.assertTrue(callable(self.manager.export_template))
        self.assertTrue(callable(self.manager.import_template))
        self.assertTrue(callable(self.manager.validate_template))
        self.assertTrue(callable(self.manager.delete_template))
    
    def test_template_info_api(self):
        """Test template info API."""
        # Create a test file
        test_file = os.path.join(self.test_dir, "test.png")
        with open(test_file, 'w') as f:
            f.write("test content")
        
        info = self.manager.get_template_info(Path(test_file))
        
        # Check API contract
        self.assertIsInstance(info, dict)
        self.assertIn('filename', info)
        self.assertIn('path', info)
        self.assertIn('size', info)
        self.assertIn('created', info)
        self.assertIn('modified', info)
        self.assertIn('hash', info)
        self.assertIn('extension', info)
        self.assertIn('category', info)
    
    def test_list_templates_api(self):
        """Test list templates API."""
        # Test with empty directory
        templates = self.manager.list_templates()
        self.assertIsInstance(templates, list)
        
        # Test with category filter
        templates = self.manager.list_templates("basic")
        self.assertIsInstance(templates, list)
        
        # Create test files
        test_files = ["lined_5mm.png", "grid_10mm.png", "dot_grid_7mm.png"]
        for filename in test_files:
            filepath = os.path.join(self.test_dir, filename)
            with open(filepath, 'w') as f:
                f.write("test content")
        
        templates = self.manager.list_templates()
        self.assertIsInstance(templates, list)
        self.assertEqual(len(templates), 3)
        
        # Test category filtering
        lined_templates = self.manager.list_templates("lined")
        self.assertEqual(len(lined_templates), 1)


class TestInstallationAPI(unittest.TestCase):
    """Test the installation API contracts."""
    
    def setUp(self):
        """Set up test environment."""
        self.installer = KoboInstaller()
        self.advanced_installer = AdvancedInstaller()
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        self.advanced_installer.stop_worker_thread()
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_kobo_installer_api(self):
        """Test Kobo installer API."""
        # Test that all required methods exist
        self.assertTrue(hasattr(self.installer, 'create_installation_package'))
        self.assertTrue(hasattr(self.installer, '_validate_package'))
        self.assertTrue(hasattr(self.installer, 'install_package'))
        self.assertTrue(hasattr(self.installer, 'list_installed_templates'))
        self.assertTrue(hasattr(self.installer, 'uninstall_templates'))
        
        # Test that methods are callable
        self.assertTrue(callable(self.installer.create_installation_package))
        self.assertTrue(callable(self.installer._validate_package))
        self.assertTrue(callable(self.installer.install_package))
        self.assertTrue(callable(self.installer.list_installed_templates))
        self.assertTrue(callable(self.installer.uninstall_templates))
    
    def test_advanced_installer_api(self):
        """Test advanced installer API."""
        # Test that all required methods exist
        self.assertTrue(hasattr(self.advanced_installer, 'create_installation_job'))
        self.assertTrue(hasattr(self.advanced_installer, 'get_job_status'))
        self.assertTrue(hasattr(self.advanced_installer, 'list_jobs'))
        self.assertTrue(hasattr(self.advanced_installer, 'cancel_job'))
        self.assertTrue(hasattr(self.advanced_installer, 'delete_job'))
        self.assertTrue(hasattr(self.advanced_installer, 'install_batch'))
        self.assertTrue(hasattr(self.advanced_installer, 'get_installation_statistics'))
        
        # Test that methods are callable
        self.assertTrue(callable(self.advanced_installer.create_installation_job))
        self.assertTrue(callable(self.advanced_installer.get_job_status))
        self.assertTrue(callable(self.advanced_installer.list_jobs))
        self.assertTrue(callable(self.advanced_installer.cancel_job))
        self.assertTrue(callable(self.advanced_installer.delete_job))
        self.assertTrue(callable(self.advanced_installer.install_batch))
        self.assertTrue(callable(self.advanced_installer.get_installation_statistics))
    
    def test_installation_package_api(self):
        """Test installation package creation API."""
        # Create test template files
        template_files = []
        for i in range(3):
            template_file = os.path.join(self.test_dir, f"template_{i}.png")
            with open(template_file, 'w') as f:
                f.write(f"template content {i}")
            template_files.append(template_file)
        
        # Test package creation
        package_path = self.installer.create_installation_package(
            templates=template_files,
            output_path=self.test_dir,
            package_name="test_package"
        )
        
        self.assertTrue(os.path.exists(package_path))
        self.assertTrue(package_path.endswith('.tgz'))
        
        # Test package validation
        validation_result = self.installer._validate_package(package_path)
        self.assertIsInstance(validation_result, bool)
    
    def test_job_management_api(self):
        """Test job management API."""
        # Test job creation
        job_id = self.advanced_installer.create_installation_job(
            name="Test Job",
            templates=["template1.png"],
            device_path="/mnt/kobo"
        )
        
        self.assertIsNotNone(job_id)
        self.assertIsInstance(job_id, str)
        
        # Test job status retrieval
        job = self.advanced_installer.get_job_status(job_id)
        self.assertIsNotNone(job)
        
        # Test job listing
        jobs = self.advanced_installer.list_jobs()
        self.assertIsInstance(jobs, list)
        
        # Test statistics
        stats = self.advanced_installer.get_installation_statistics()
        self.assertIsInstance(stats, dict)
        self.assertIn('total_jobs', stats)
        self.assertIn('pending_jobs', stats)
        self.assertIn('completed_jobs', stats)


class TestDeviceManagementAPI(unittest.TestCase):
    """Test the device management API contracts."""
    
    def setUp(self):
        """Set up test environment."""
        self.device_manager = DeviceManager()
        self.diagnostics = DeviceDiagnostics()
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_device_manager_api(self):
        """Test device manager API."""
        # Test that all required methods exist
        self.assertTrue(hasattr(self.device_manager, 'detect_devices'))
        self.assertTrue(hasattr(self.device_manager, '_is_kobo_device'))
        self.assertTrue(hasattr(self.device_manager, '_get_device_info'))
        self.assertTrue(hasattr(self.device_manager, 'has_connected_device'))
        self.assertTrue(hasattr(self.device_manager, 'create_backup'))
        self.assertTrue(hasattr(self.device_manager, 'restore_backup'))
        
        # Test that methods are callable
        self.assertTrue(callable(self.device_manager.detect_devices))
        self.assertTrue(callable(self.device_manager._is_kobo_device))
        self.assertTrue(callable(self.device_manager._get_device_info))
        self.assertTrue(callable(self.device_manager.has_connected_device))
        self.assertTrue(callable(self.device_manager.create_backup))
        self.assertTrue(callable(self.device_manager.restore_backup))
    
    def test_device_diagnostics_api(self):
        """Test device diagnostics API."""
        # Test that all required methods exist
        self.assertTrue(hasattr(self.diagnostics, 'run_full_diagnostics'))
        self.assertTrue(hasattr(self.diagnostics, '_check_device_connectivity'))
        self.assertTrue(hasattr(self.diagnostics, '_check_storage_health'))
        self.assertTrue(hasattr(self.diagnostics, '_check_firmware_health'))
        self.assertTrue(hasattr(self.diagnostics, '_check_database_health'))
        self.assertTrue(hasattr(self.diagnostics, '_check_template_health'))
        self.assertTrue(hasattr(self.diagnostics, 'save_health_report'))
        self.assertTrue(hasattr(self.diagnostics, 'load_health_report'))
        
        # Test that methods are callable
        self.assertTrue(callable(self.diagnostics.run_full_diagnostics))
        self.assertTrue(callable(self.diagnostics._check_device_connectivity))
        self.assertTrue(callable(self.diagnostics._check_storage_health))
        self.assertTrue(callable(self.diagnostics._check_firmware_health))
        self.assertTrue(callable(self.diagnostics._check_database_health))
        self.assertTrue(callable(self.diagnostics._check_template_health))
        self.assertTrue(callable(self.diagnostics.save_health_report))
        self.assertTrue(callable(self.diagnostics.load_health_report))
    
    def test_device_detection_api(self):
        """Test device detection API."""
        # Test device detection
        devices = self.device_manager.detect_devices()
        self.assertIsInstance(devices, list)
        
        # Test connected device check
        has_device = self.device_manager.has_connected_device()
        self.assertIsInstance(has_device, bool)
    
    def test_diagnostics_api(self):
        """Test diagnostics API."""
        # Test full diagnostics
        health = self.diagnostics.run_full_diagnostics("/nonexistent/path")
        
        # Check API contract
        self.assertIsNotNone(health)
        self.assertIn('overall_status', health.__dict__)
        self.assertIn('score', health.__dict__)
        self.assertIn('diagnostics', health.__dict__)
        self.assertIn('last_checked', health.__dict__)
        self.assertIn('recommendations', health.__dict__)


class TestIntegrationAPI(unittest.TestCase):
    """Test integration between different components."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.generator = TemplateGenerator()
        self.manager = TemplateManager(self.test_dir)
        self.installer = KoboInstaller()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_template_generation_to_management(self):
        """Test integration between template generation and management."""
        # Generate a template
        template = self.generator.generate_lined_template()
        
        # Save template
        template_path = os.path.join(self.test_dir, "test_template.png")
        self.generator.save_template(template, template_path)
        
        # Get template info through manager
        info = self.manager.get_template_info(Path(template_path))
        self.assertIsNotNone(info)
        self.assertEqual(info['filename'], 'test_template.png')
        
        # Validate template through manager
        validation = self.manager.validate_template(template_path)
        self.assertIsInstance(validation, dict)
        self.assertIn('valid', validation)
    
    def test_template_management_to_installation(self):
        """Test integration between template management and installation."""
        # Create test template files
        template_files = []
        for i in range(3):
            template_file = os.path.join(self.test_dir, f"template_{i}.png")
            with open(template_file, 'w') as f:
                f.write(f"template content {i}")
            template_files.append(template_file)
        
        # Create installation package
        package_path = self.installer.create_installation_package(
            templates=template_files,
            output_path=self.test_dir,
            package_name="integration_test_package"
        )
        
        self.assertTrue(os.path.exists(package_path))
        
        # Validate package
        validation = self.installer._validate_package(package_path)
        self.assertTrue(validation)
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow."""
        # 1. Generate template
        template = self.generator.generate_cornell_template()
        
        # 2. Save template
        template_path = os.path.join(self.test_dir, "workflow_template.png")
        self.generator.save_template(template, template_path)
        
        # 3. Validate template
        validation = self.generator.validate_template(template)
        self.assertIsInstance(validation, dict)
        
        # 4. Get template info
        info = self.manager.get_template_info(Path(template_path))
        self.assertIsNotNone(info)
        
        # 5. Create installation package
        package_path = self.installer.create_installation_package(
            templates=[template_path],
            output_path=self.test_dir,
            package_name="workflow_package"
        )
        
        self.assertTrue(os.path.exists(package_path))
        
        # 6. Validate package
        package_validation = self.installer._validate_package(package_path)
        self.assertTrue(package_validation)
    
    def test_error_handling_integration(self):
        """Test error handling across components."""
        # Test with non-existent template
        with self.assertRaises(Exception):
            self.generator.create_template_from_image("/nonexistent/image.png")
        
        # Test with invalid template path
        info = self.manager.get_template_info(Path("/nonexistent/template.png"))
        self.assertEqual(info, {})
        
        # Test with non-existent package
        validation = self.installer._validate_package("/nonexistent/package.tgz")
        self.assertFalse(validation)


if __name__ == '__main__':
    unittest.main()