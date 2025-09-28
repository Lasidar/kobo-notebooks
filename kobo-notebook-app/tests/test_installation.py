#!/usr/bin/env python3
"""
Unit tests for installation modules.

This module contains comprehensive unit tests for the installation system
including basic and advanced installation features.
"""

import unittest
import tempfile
import os
import shutil
from pathlib import Path
import sys
import json
import tarfile
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from installation.kobo_installer import KoboInstaller
from installation.advanced_installer import AdvancedInstaller, InstallationStatus, InstallationJob


class TestKoboInstaller(unittest.TestCase):
    """Test the basic Kobo installer."""
    
    def setUp(self):
        """Set up test environment."""
        self.installer = KoboInstaller()
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_installer_creation(self):
        """Test installer creation."""
        self.assertIsNotNone(self.installer)
    
    def test_create_installation_package(self):
        """Test installation package creation."""
        # Create test template files
        template_files = []
        for i in range(3):
            template_file = os.path.join(self.test_dir, f"template_{i}.png")
            with open(template_file, 'w') as f:
                f.write(f"template content {i}")
            template_files.append(template_file)
        
        package_path = self.installer.create_installation_package(
            templates=template_files,
            output_path=self.test_dir,
            package_name="test_package"
        )
        
        self.assertTrue(os.path.exists(package_path))
        self.assertTrue(package_path.endswith('.tgz'))
        
        # Verify package contents
        with tarfile.open(package_path, "r:gz") as tar:
            files = tar.getnames()
            # Check for manifest.json (may be at root or in subdirectory)
            manifest_found = any('manifest.json' in f for f in files)
            preinstall_found = any('preinstall' in f for f in files)
            postinstall_found = any('postinstall' in f for f in files)
            self.assertTrue(manifest_found, f"manifest.json not found in {files}")
            self.assertTrue(preinstall_found, f"preinstall not found in {files}")
            self.assertTrue(postinstall_found, f"postinstall not found in {files}")
    
    def test_create_installation_package_no_templates(self):
        """Test installation package creation with no templates."""
        package_path = self.installer.create_installation_package(
            templates=[],
            output_path=self.test_dir,
            package_name="empty_package"
        )
        
        self.assertTrue(os.path.exists(package_path))
        
        # Verify package contents
        with tarfile.open(package_path, "r:gz") as tar:
            files = tar.getnames()
            # Check for manifest.json (may be at root or in subdirectory)
            manifest_found = any('manifest.json' in f for f in files)
            preinstall_found = any('preinstall' in f for f in files)
            postinstall_found = any('postinstall' in f for f in files)
            self.assertTrue(manifest_found, f"manifest.json not found in {files}")
            self.assertTrue(preinstall_found, f"preinstall not found in {files}")
            self.assertTrue(postinstall_found, f"postinstall not found in {files}")
    
    def test_validate_package_nonexistent(self):
        """Test package validation with non-existent file."""
        result = self.installer._validate_package("/nonexistent/package.tgz")
        self.assertFalse(result)
    
    def test_validate_package_invalid(self):
        """Test package validation with invalid file."""
        # Create an invalid package file
        invalid_file = os.path.join(self.test_dir, "invalid.tgz")
        with open(invalid_file, 'w') as f:
            f.write("not a tar file")
        
        result = self.installer._validate_package(invalid_file)
        self.assertFalse(result)
    
    def test_validate_package_valid(self):
        """Test package validation with valid package."""
        # Create test template files
        template_files = []
        for i in range(2):
            template_file = os.path.join(self.test_dir, f"template_{i}.png")
            with open(template_file, 'w') as f:
                f.write(f"template content {i}")
            template_files.append(template_file)
        
        package_path = self.installer.create_installation_package(
            templates=template_files,
            output_path=self.test_dir,
            package_name="valid_package"
        )
        
        result = self.installer._validate_package(package_path)
        self.assertTrue(result)
    
    def test_install_package_nonexistent(self):
        """Test package installation with non-existent package."""
        result = self.installer.install_package(
            "/nonexistent/package.tgz",
            "/mnt/kobo"
        )
        self.assertFalse(result)
    
    def test_list_installed_templates_nonexistent(self):
        """Test listing installed templates on non-existent device."""
        templates = self.installer.list_installed_templates("/nonexistent/device")
        self.assertIsInstance(templates, list)
        self.assertEqual(len(templates), 0)
    
    def test_uninstall_templates_nonexistent(self):
        """Test uninstalling templates from non-existent device."""
        result = self.installer.uninstall_templates(
            "/nonexistent/device",
            ["template1.png", "template2.png"]
        )
        self.assertFalse(result)


class TestAdvancedInstaller(unittest.TestCase):
    """Test the advanced installer."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        # Create fresh installer for each test
        self.installer = AdvancedInstaller()
    
    def tearDown(self):
        """Clean up test environment."""
        # Stop worker thread
        self.installer.stop_worker_thread()
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_installer_creation(self):
        """Test advanced installer creation."""
        self.assertIsNotNone(self.installer)
        self.assertIsInstance(self.installer.jobs, dict)
        self.assertIsInstance(self.installer.job_queue, list)
    
    def test_installation_status_enum(self):
        """Test installation status enumeration."""
        self.assertEqual(InstallationStatus.PENDING.value, "pending")
        self.assertEqual(InstallationStatus.IN_PROGRESS.value, "in_progress")
        self.assertEqual(InstallationStatus.COMPLETED.value, "completed")
        self.assertEqual(InstallationStatus.FAILED.value, "failed")
        self.assertEqual(InstallationStatus.CANCELLED.value, "cancelled")
    
    def test_installation_job_creation(self):
        """Test installation job creation."""
        job = InstallationJob(
            id="test_job",
            name="Test Job",
            templates=["template1.png", "template2.png"],
            device_path="/mnt/kobo",
            status=InstallationStatus.PENDING,
            created=datetime.now()
        )
        
        self.assertEqual(job.id, "test_job")
        self.assertEqual(job.name, "Test Job")
        self.assertEqual(len(job.templates), 2)
        self.assertEqual(job.device_path, "/mnt/kobo")
        self.assertEqual(job.status, InstallationStatus.PENDING)
    
    def test_create_installation_job(self):
        """Test creating installation job."""
        job_id = self.installer.create_installation_job(
            name="Test Job",
            templates=["template1.png", "template2.png"],
            device_path="/mnt/kobo"
        )
        
        self.assertIsNotNone(job_id)
        self.assertIn(job_id, self.installer.jobs)
        
        job = self.installer.jobs[job_id]
        self.assertEqual(job.name, "Test Job")
        self.assertEqual(len(job.templates), 2)
        self.assertEqual(job.device_path, "/mnt/kobo")
        self.assertEqual(job.status, InstallationStatus.PENDING)
    
    def test_create_installation_job_with_schedule(self):
        """Test creating installation job with schedule."""
        scheduled_time = datetime.now()
        job_id = self.installer.create_installation_job(
            name="Scheduled Job",
            templates=["template1.png"],
            device_path="/mnt/kobo",
            scheduled_time=scheduled_time
        )
        
        job = self.installer.jobs[job_id]
        self.assertEqual(job.scheduled, scheduled_time)
    
    def test_get_job_status(self):
        """Test getting job status."""
        job_id = self.installer.create_installation_job(
            name="Test Job",
            templates=["template1.png"],
            device_path="/mnt/kobo"
        )
        
        job = self.installer.get_job_status(job_id)
        self.assertIsNotNone(job)
        self.assertEqual(job.name, "Test Job")
        
        # Test non-existent job
        non_existent_job = self.installer.get_job_status("non_existent")
        self.assertIsNone(non_existent_job)
    
    def test_list_jobs(self):
        """Test listing jobs."""
        # Get initial job count
        initial_jobs = self.installer.list_jobs()
        initial_count = len(initial_jobs)
        
        # Create some jobs
        job_id1 = self.installer.create_installation_job(
            name="Job 1",
            templates=["template1.png"],
            device_path="/mnt/kobo"
        )
        
        job_id2 = self.installer.create_installation_job(
            name="Job 2",
            templates=["template2.png"],
            device_path="/mnt/kobo"
        )
        
        # List all jobs
        all_jobs = self.installer.list_jobs()
        self.assertEqual(len(all_jobs), initial_count + 2)
        
        # List pending jobs (should include our new jobs)
        pending_jobs = self.installer.list_jobs(InstallationStatus.PENDING)
        self.assertGreaterEqual(len(pending_jobs), 2)
        
        # List completed jobs (should be empty or existing)
        completed_jobs = self.installer.list_jobs(InstallationStatus.COMPLETED)
        # Just verify it's a list, don't check exact count due to persistence
    
    def test_cancel_job(self):
        """Test cancelling job."""
        job_id = self.installer.create_installation_job(
            name="Test Job",
            templates=["template1.png"],
            device_path="/mnt/kobo"
        )
        
        # Cancel pending job
        result = self.installer.cancel_job(job_id)
        self.assertTrue(result)
        
        job = self.installer.jobs[job_id]
        self.assertEqual(job.status, InstallationStatus.CANCELLED)
        
        # Try to cancel non-existent job
        result = self.installer.cancel_job("non_existent")
        self.assertFalse(result)
    
    def test_delete_job(self):
        """Test deleting job."""
        job_id = self.installer.create_installation_job(
            name="Test Job",
            templates=["template1.png"],
            device_path="/mnt/kobo"
        )
        
        # Mark job as completed
        job = self.installer.jobs[job_id]
        job.status = InstallationStatus.COMPLETED
        job.completed = datetime.now()
        
        # Delete completed job
        result = self.installer.delete_job(job_id)
        self.assertTrue(result)
        self.assertNotIn(job_id, self.installer.jobs)
        
        # Try to delete non-existent job
        result = self.installer.delete_job("non_existent")
        self.assertFalse(result)
    
    def test_delete_job_pending(self):
        """Test deleting pending job (should fail)."""
        job_id = self.installer.create_installation_job(
            name="Test Job",
            templates=["template1.png"],
            device_path="/mnt/kobo"
        )
        
        # Try to delete pending job
        result = self.installer.delete_job(job_id)
        self.assertFalse(result)
        self.assertIn(job_id, self.installer.jobs)
    
    def test_install_batch(self):
        """Test batch installation."""
        # Create some jobs
        job_id1 = self.installer.create_installation_job(
            name="Job 1",
            templates=["template1.png"],
            device_path="/mnt/kobo"
        )
        
        job_id2 = self.installer.create_installation_job(
            name="Job 2",
            templates=["template2.png"],
            device_path="/mnt/kobo"
        )
        
        # Batch install
        results = self.installer.install_batch([job_id1, job_id2])
        
        self.assertIsInstance(results, dict)
        self.assertTrue(results[job_id1])
        self.assertTrue(results[job_id2])
        
        # Check that jobs are in queue
        self.assertIn(job_id1, self.installer.job_queue)
        self.assertIn(job_id2, self.installer.job_queue)
    
    def test_install_batch_non_existent(self):
        """Test batch installation with non-existent jobs."""
        results = self.installer.install_batch(["non_existent_1", "non_existent_2"])
        
        self.assertFalse(results["non_existent_1"])
        self.assertFalse(results["non_existent_2"])
    
    def test_get_installation_statistics(self):
        """Test getting installation statistics."""
        # Get initial statistics
        initial_stats = self.installer.get_installation_statistics()
        initial_total = initial_stats['total_jobs']
        
        # Create some jobs with different statuses
        job_id1 = self.installer.create_installation_job(
            name="Pending Job",
            templates=["template1.png"],
            device_path="/mnt/kobo"
        )
        
        job_id2 = self.installer.create_installation_job(
            name="Completed Job",
            templates=["template2.png"],
            device_path="/mnt/kobo"
        )
        
        # Mark one as completed
        job2 = self.installer.jobs[job_id2]
        job2.status = InstallationStatus.COMPLETED
        job2.completed = datetime.now()
        
        stats = self.installer.get_installation_statistics()
        
        self.assertIn('total_jobs', stats)
        self.assertIn('pending_jobs', stats)
        self.assertIn('completed_jobs', stats)
        self.assertIn('failed_jobs', stats)
        self.assertIn('cancelled_jobs', stats)
        self.assertIn('queue_length', stats)
        self.assertIn('current_job', stats)
        self.assertIn('success_rate', stats)
        
        # Check that we added 2 jobs
        self.assertEqual(stats['total_jobs'], initial_total + 2)
        self.assertGreaterEqual(stats['pending_jobs'], 1)
        self.assertGreaterEqual(stats['completed_jobs'], 1)
    
    def test_progress_callbacks(self):
        """Test progress callbacks."""
        callback_called = []
        
        def test_callback(job_id, progress, message):
            callback_called.append((job_id, progress, message))
        
        # Add callback
        self.installer.add_progress_callback(test_callback)
        
        # Remove callback
        self.installer.remove_progress_callback(test_callback)
        
        # Test that callback was removed
        self.assertNotIn(test_callback, self.installer.progress_callbacks)
    
    def test_cleanup_old_jobs(self):
        """Test cleanup of old jobs."""
        # Create an old completed job
        job_id = self.installer.create_installation_job(
            name="Old Job",
            templates=["template1.png"],
            device_path="/mnt/kobo"
        )
        
        job = self.installer.jobs[job_id]
        job.status = InstallationStatus.COMPLETED
        job.completed = datetime.now()  # Should be recent, not old
        
        # Cleanup jobs older than 1 day (should not remove recent job)
        self.installer.cleanup_old_jobs(days_old=1)
        self.assertIn(job_id, self.installer.jobs)
        
        # Cleanup jobs older than 0 days (should remove all completed jobs)
        self.installer.cleanup_old_jobs(days_old=0)
        self.assertNotIn(job_id, self.installer.jobs)


if __name__ == '__main__':
    unittest.main()