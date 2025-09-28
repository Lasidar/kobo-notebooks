#!/usr/bin/env python3
"""
Unit tests for utility modules.

This module contains comprehensive unit tests for the utility functions
including logging, device management, and diagnostics.
"""

import unittest
import tempfile
import os
import shutil
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.logger import setup_logger
from utils.device_manager import DeviceManager
from utils.device_diagnostics import DeviceDiagnostics, HealthStatus, DiagnosticResult


class TestLogger(unittest.TestCase):
    """Test the logging utility."""
    
    def setUp(self):
        """Set up test environment."""
        self.logger = setup_logger("test_logger")
    
    def test_logger_creation(self):
        """Test that logger is created successfully."""
        self.assertIsNotNone(self.logger)
        self.assertEqual(self.logger.name, "test_logger")
    
    def test_logging_levels(self):
        """Test different logging levels."""
        # These should not raise exceptions
        self.logger.debug("Debug message")
        self.logger.info("Info message")
        self.logger.warning("Warning message")
        self.logger.error("Error message")
        self.logger.critical("Critical message")
    
    def test_logger_name(self):
        """Test logger name setting."""
        logger2 = setup_logger("different_name")
        self.assertEqual(logger2.name, "different_name")
        self.assertNotEqual(self.logger.name, logger2.name)


class TestDeviceManager(unittest.TestCase):
    """Test the device manager."""
    
    def setUp(self):
        """Set up test environment."""
        self.device_manager = DeviceManager()
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_device_manager_creation(self):
        """Test device manager creation."""
        self.assertIsNotNone(self.device_manager)
        self.assertIsNone(self.device_manager.connected_device)
    
    def test_detect_devices_empty(self):
        """Test device detection with no devices."""
        devices = self.device_manager.detect_devices()
        self.assertIsInstance(devices, list)
        # Should return empty list in test environment
    
    def test_is_kobo_device_false(self):
        """Test Kobo device detection with non-Kobo directory."""
        # Create a temporary directory that's not a Kobo device
        test_dir = os.path.join(self.test_dir, "regular_device")
        os.makedirs(test_dir)
        
        # Create a file to make it look like a regular directory
        with open(os.path.join(test_dir, "random_file.txt"), 'w') as f:
            f.write("not a kobo device")
        
        result = self.device_manager._is_kobo_device(test_dir)
        self.assertFalse(result)
    
    def test_is_kobo_device_true(self):
        """Test Kobo device detection with Kobo directory."""
        # Create a temporary directory that looks like a Kobo device
        test_dir = os.path.join(self.test_dir, "kobo_device")
        os.makedirs(test_dir)
        
        # Create .kobo directory
        kobo_dir = os.path.join(test_dir, ".kobo")
        os.makedirs(kobo_dir)
        
        result = self.device_manager._is_kobo_device(test_dir)
        self.assertTrue(result)
    
    def test_get_device_info_nonexistent(self):
        """Test getting device info for non-existent device."""
        result = self.device_manager._get_device_info("/nonexistent/path")
        self.assertIsNone(result)
    
    def test_has_connected_device_false(self):
        """Test connected device check with no device."""
        result = self.device_manager.has_connected_device()
        self.assertFalse(result)
    
    def test_create_backup_no_device(self):
        """Test backup creation with no connected device."""
        with self.assertRaises(ValueError):
            self.device_manager.create_backup("/tmp/backup")
    
    def test_restore_backup_no_device(self):
        """Test backup restore with no connected device."""
        with self.assertRaises(ValueError):
            self.device_manager.restore_backup("/tmp/backup.kobo_backup")


class TestDeviceDiagnostics(unittest.TestCase):
    """Test the device diagnostics system."""
    
    def setUp(self):
        """Set up test environment."""
        self.diagnostics = DeviceDiagnostics()
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_diagnostics_creation(self):
        """Test diagnostics system creation."""
        self.assertIsNotNone(self.diagnostics)
    
    def test_health_status_enum(self):
        """Test health status enumeration."""
        self.assertEqual(HealthStatus.EXCELLENT.value, "excellent")
        self.assertEqual(HealthStatus.GOOD.value, "good")
        self.assertEqual(HealthStatus.WARNING.value, "warning")
        self.assertEqual(HealthStatus.CRITICAL.value, "critical")
        self.assertEqual(HealthStatus.UNKNOWN.value, "unknown")
    
    def test_diagnostic_result_creation(self):
        """Test diagnostic result creation."""
        result = DiagnosticResult(
            name="Test Diagnostic",
            status=HealthStatus.GOOD,
            message="Test message",
            details={"test": "data"},
            recommendations=["Test recommendation"],
            timestamp=None
        )
        
        self.assertEqual(result.name, "Test Diagnostic")
        self.assertEqual(result.status, HealthStatus.GOOD)
        self.assertEqual(result.message, "Test message")
        self.assertEqual(result.details["test"], "data")
        self.assertEqual(result.recommendations[0], "Test recommendation")
    
    def test_check_device_connectivity_nonexistent(self):
        """Test device connectivity check with non-existent device."""
        result = self.diagnostics._check_device_connectivity("/nonexistent/path")
        
        self.assertEqual(result.name, "Device Connectivity")
        self.assertEqual(result.status, HealthStatus.CRITICAL)
        self.assertIn("not accessible", result.message)
    
    def test_check_storage_health_nonexistent(self):
        """Test storage health check with non-existent device."""
        result = self.diagnostics._check_storage_health("/nonexistent/path")
        
        self.assertEqual(result.name, "Storage Health")
        self.assertEqual(result.status, HealthStatus.CRITICAL)
        self.assertIn("Storage check failed", result.message)
    
    def test_check_firmware_health_nonexistent(self):
        """Test firmware health check with non-existent device."""
        result = self.diagnostics._check_firmware_health("/nonexistent/path")
        
        self.assertEqual(result.name, "Firmware Health")
        self.assertEqual(result.status, HealthStatus.WARNING)
        self.assertIn("Firmware version file not found", result.message)
    
    def test_check_database_health_nonexistent(self):
        """Test database health check with non-existent device."""
        result = self.diagnostics._check_database_health("/nonexistent/path")
        
        self.assertEqual(result.name, "Database Health")
        self.assertEqual(result.status, HealthStatus.CRITICAL)
        self.assertIn("Main database not found", result.message)
    
    def test_check_template_health_nonexistent(self):
        """Test template health check with non-existent device."""
        result = self.diagnostics._check_template_health("/nonexistent/path")
        
        self.assertEqual(result.name, "Template Health")
        self.assertEqual(result.status, HealthStatus.WARNING)
        self.assertIn("No template directories found", result.message)
    
    def test_calculate_overall_health_empty(self):
        """Test overall health calculation with empty diagnostics."""
        status, score = self.diagnostics._calculate_overall_health([])
        
        self.assertEqual(status, HealthStatus.UNKNOWN)
        self.assertEqual(score, 0.0)
    
    def test_calculate_overall_health_single(self):
        """Test overall health calculation with single diagnostic."""
        diagnostic = DiagnosticResult(
            name="Test",
            status=HealthStatus.EXCELLENT,
            message="Test",
            details={},
            recommendations=[],
            timestamp=None
        )
        
        status, score = self.diagnostics._calculate_overall_health([diagnostic])
        
        self.assertEqual(status, HealthStatus.EXCELLENT)
        self.assertEqual(score, 100.0)
    
    def test_generate_recommendations_empty(self):
        """Test recommendation generation with empty diagnostics."""
        recommendations = self.diagnostics._generate_recommendations([])
        
        self.assertIsInstance(recommendations, list)
        self.assertEqual(len(recommendations), 0)
    
    def test_generate_recommendations_with_data(self):
        """Test recommendation generation with diagnostic data."""
        diagnostic = DiagnosticResult(
            name="Test",
            status=HealthStatus.WARNING,
            message="Test",
            details={},
            recommendations=["Test recommendation"],
            timestamp=None
        )
        
        recommendations = self.diagnostics._generate_recommendations([diagnostic])
        
        self.assertIsInstance(recommendations, list)
        self.assertIn("Test recommendation", recommendations)
    
    def test_run_full_diagnostics_nonexistent(self):
        """Test full diagnostics with non-existent device."""
        health = self.diagnostics.run_full_diagnostics("/nonexistent/path")
        
        self.assertIsNotNone(health)
        self.assertEqual(health.overall_status, HealthStatus.CRITICAL)
        self.assertIsInstance(health.diagnostics, list)
        self.assertGreater(len(health.diagnostics), 0)


if __name__ == '__main__':
    unittest.main()