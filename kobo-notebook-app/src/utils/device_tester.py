#!/usr/bin/env python3
"""
Device Testing Module for Kobo Elipsa 2e

This module provides comprehensive testing tools for validating
the application's functionality across different devices and firmware versions.
"""

import os
import time
import json
import shutil
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import subprocess
import hashlib

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.logger import setup_logger
from utils.device_manager import DeviceManager
from utils.device_diagnostics import DeviceDiagnostics
from template_tools.template_generator import TemplateGenerator
from template_tools.template_manager import TemplateManager
from installation.kobo_installer import KoboInstaller
from installation.advanced_installer import AdvancedInstaller


class DeviceTestResult:
    """Represents the result of a device test."""
    
    def __init__(self, test_name: str, success: bool, message: str = "", 
                 duration: float = 0.0, details: Dict[str, Any] = None):
        self.test_name = test_name
        self.success = success
        self.message = message
        self.duration = duration
        self.details = details or {}
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_name": self.test_name,
            "success": self.success,
            "message": self.message,
            "duration": self.duration,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }


class DeviceTestSuite:
    """Comprehensive test suite for Kobo device validation."""
    
    def __init__(self):
        self.logger = setup_logger()
        self.device_manager = DeviceManager()
        self.diagnostics = DeviceDiagnostics()
        self.generator = TemplateGenerator()
        self.installer = KoboInstaller()
        self.test_results: List[DeviceTestResult] = []
    
    def run_test(self, test_func, test_name: str) -> DeviceTestResult:
        """Run a single test and record the result."""
        self.logger.info(f"Running test: {test_name}")
        start_time = time.time()
        
        try:
            result = test_func()
            duration = time.time() - start_time
            
            if isinstance(result, tuple):
                success, message = result
                details = {}
            elif isinstance(result, dict):
                success = result.get('success', False)
                message = result.get('message', '')
                details = result.get('details', {})
            else:
                success = bool(result)
                message = "Test completed" if success else "Test failed"
                details = {}
            
            test_result = DeviceTestResult(test_name, success, message, duration, details)
            self.test_results.append(test_result)
            
            status = "✓ PASS" if success else "✗ FAIL"
            self.logger.info(f"{status}: {test_name} - {message}")
            
            return test_result
            
        except Exception as e:
            duration = time.time() - start_time
            error_msg = f"Test error: {str(e)}"
            test_result = DeviceTestResult(test_name, False, error_msg, duration)
            self.test_results.append(test_result)
            
            self.logger.error(f"✗ ERROR: {test_name} - {error_msg}")
            return test_result
    
    def test_device_detection(self) -> DeviceTestResult:
        """Test device detection functionality."""
        def _test():
            devices = self.device_manager.detect_devices()
            if not devices:
                return False, "No devices detected"
            
            device = devices[0]
            required_fields = ['path', 'model', 'firmware']
            for field in required_fields:
                if field not in device:
                    return False, f"Missing field: {field}"
            
            return True, f"Detected {len(devices)} device(s)"
        
        return self.run_test(_test, "Device Detection")
    
    def test_device_connectivity(self) -> DeviceTestResult:
        """Test device connectivity and file system access."""
        def _test():
            devices = self.device_manager.detect_devices()
            if not devices:
                return False, "No devices available for connectivity test"
            
            device_path = devices[0]['path']
            
            # Test basic file system access
            if not os.path.exists(device_path):
                return False, f"Device path does not exist: {device_path}"
            
            # Test write access (create a temporary file)
            test_file = os.path.join(device_path, "test_connectivity.tmp")
            try:
                with open(test_file, 'w') as f:
                    f.write("test")
                
                # Clean up
                os.remove(test_file)
                
                return True, "Device connectivity verified"
            except PermissionError:
                return False, "No write permission to device"
            except Exception as e:
                return False, f"Connectivity test failed: {e}"
        
        return self.run_test(_test, "Device Connectivity")
    
    def test_template_generation(self) -> DeviceTestResult:
        """Test template generation functionality."""
        def _test():
            test_dir = tempfile.mkdtemp()
            try:
                # Test all template types
                template_types = [
                    ("Lined", self.generator.generate_lined_template),
                    ("Grid", self.generator.generate_grid_template),
                    ("Dot Grid", self.generator.generate_dot_grid_template),
                    ("Cornell", self.generator.generate_cornell_template),
                    ("Blank", self.generator.generate_blank_template)
                ]
                
                generated_templates = []
                for template_name, generator_func in template_types:
                    try:
                        template = generator_func()
                        if template is None:
                            return False, f"Failed to generate {template_name} template"
                        
                        # Save template
                        template_path = os.path.join(test_dir, f"{template_name.lower()}.png")
                        self.generator.save_template(template, template_path)
                        
                        if not os.path.exists(template_path):
                            return False, f"Failed to save {template_name} template"
                        
                        generated_templates.append(template_name)
                        
                    except Exception as e:
                        return False, f"Error generating {template_name}: {e}"
                
                return True, f"Generated {len(generated_templates)} templates: {', '.join(generated_templates)}"
            
            finally:
                shutil.rmtree(test_dir, ignore_errors=True)
        
        return self.run_test(_test, "Template Generation")
    
    def test_template_validation(self) -> DeviceTestResult:
        """Test template validation functionality."""
        def _test():
            # Generate a test template
            template = self.generator.generate_lined_template()
            
            # Test validation
            validation_result = self.generator.validate_template(template)
            
            if not isinstance(validation_result, dict):
                return False, "Validation result is not a dictionary"
            
            required_fields = ['valid', 'warnings', 'errors']
            for field in required_fields:
                if field not in validation_result:
                    return False, f"Missing validation field: {field}"
            
            return True, f"Validation passed: {validation_result['valid']}"
        
        return self.run_test(_test, "Template Validation")
    
    def test_package_creation(self) -> DeviceTestResult:
        """Test installation package creation."""
        def _test():
            test_dir = tempfile.mkdtemp()
            try:
                # Create test templates
                template_files = []
                for i in range(3):
                    template_file = os.path.join(test_dir, f"test_template_{i}.png")
                    with open(template_file, 'w') as f:
                        f.write(f"test template {i}")
                    template_files.append(template_file)
                
                # Create package
                package_path = self.installer.create_installation_package(
                    templates=template_files,
                    output_path=test_dir,
                    package_name="test_package.tgz"
                )
                
                if not os.path.exists(package_path):
                    return False, "Package file was not created"
                
                # Validate package
                validation = self.installer._validate_package(package_path)
                if not validation:
                    return False, "Package validation failed"
                
                return True, f"Package created and validated: {os.path.basename(package_path)}"
            
            finally:
                shutil.rmtree(test_dir, ignore_errors=True)
        
        return self.run_test(_test, "Package Creation")
    
    def test_installation_simulation(self) -> DeviceTestResult:
        """Test installation process (simulated)."""
        def _test():
            devices = self.device_manager.detect_devices()
            if not devices:
                return False, "No devices available for installation test"
            
            device_path = devices[0]['path']
            
            # Create a test package
            test_dir = tempfile.mkdtemp()
            try:
                # Create test template
                template_file = os.path.join(test_dir, "test_install.png")
                with open(template_file, 'w') as f:
                    f.write("test installation template")
                
                # Create package
                package_path = self.installer.create_installation_package(
                    templates=[template_file],
                    output_path=test_dir,
                    package_name="test_install.tgz"
                )
                
                # Simulate installation (copy to device)
                device_package_path = os.path.join(device_path, "KoboRoot.tgz")
                try:
                    shutil.copy(package_path, device_package_path)
                    
                    # Verify installation
                    if os.path.exists(device_package_path):
                        # Clean up
                        os.remove(device_package_path)
                        return True, "Installation simulation successful"
                    else:
                        return False, "Installation file not found on device"
                
                except PermissionError:
                    return False, "No permission to install to device"
                except Exception as e:
                    return False, f"Installation failed: {e}"
            
            finally:
                shutil.rmtree(test_dir, ignore_errors=True)
        
        return self.run_test(_test, "Installation Simulation")
    
    def test_performance_benchmarks(self) -> DeviceTestResult:
        """Test application performance benchmarks."""
        def _test():
            benchmarks = {}
            
            # Template generation performance
            start_time = time.time()
            for _ in range(5):
                self.generator.generate_lined_template()
            benchmarks['template_generation'] = time.time() - start_time
            
            # Package creation performance
            test_dir = tempfile.mkdtemp()
            try:
                template_files = []
                for i in range(10):
                    template_file = os.path.join(test_dir, f"perf_test_{i}.png")
                    with open(template_file, 'w') as f:
                        f.write(f"performance test {i}")
                    template_files.append(template_file)
                
                start_time = time.time()
                package_path = self.installer.create_installation_package(
                    templates=template_files,
                    output_path=test_dir,
                    package_name="perf_test.tgz"
                )
                benchmarks['package_creation'] = time.time() - start_time
                
                # Package validation performance
                start_time = time.time()
                self.installer._validate_package(package_path)
                benchmarks['package_validation'] = time.time() - start_time
                
            finally:
                shutil.rmtree(test_dir, ignore_errors=True)
            
            # Check if benchmarks are within acceptable limits
            acceptable_limits = {
                'template_generation': 10.0,  # 10 seconds for 5 templates
                'package_creation': 30.0,     # 30 seconds for 10 templates
                'package_validation': 5.0     # 5 seconds for validation
            }
            
            failed_benchmarks = []
            for benchmark, time_taken in benchmarks.items():
                if time_taken > acceptable_limits.get(benchmark, float('inf')):
                    failed_benchmarks.append(f"{benchmark}: {time_taken:.2f}s")
            
            if failed_benchmarks:
                return False, f"Performance issues: {', '.join(failed_benchmarks)}"
            
            return True, f"All benchmarks passed: {benchmarks}"
        
        return self.run_test(_test, "Performance Benchmarks")
    
    def test_device_health(self) -> DeviceTestResult:
        """Test device health and diagnostics."""
        def _test():
            devices = self.device_manager.detect_devices()
            if not devices:
                return False, "No devices available for health test"
            
            device_path = devices[0]['path']
            
            # Run diagnostics
            health_report = self.diagnostics.run_full_diagnostics(device_path)
            
            if not health_report:
                return False, "Failed to generate health report"
            
            # Check overall health
            if hasattr(health_report, 'overall_status'):
                status = health_report.overall_status
                score = getattr(health_report, 'score', 0)
                
                if score < 70:  # Health score threshold
                    return False, f"Device health score too low: {score}"
                
                return True, f"Device health OK: {status} (score: {score})"
            else:
                return False, "Invalid health report format"
        
        return self.run_test(_test, "Device Health")
    
    def run_full_test_suite(self) -> Dict[str, Any]:
        """Run the complete test suite."""
        self.logger.info("Starting comprehensive device test suite...")
        self.test_results.clear()
        
        # Define test order
        tests = [
            self.test_device_detection,
            self.test_device_connectivity,
            self.test_template_generation,
            self.test_template_validation,
            self.test_package_creation,
            self.test_installation_simulation,
            self.test_performance_benchmarks,
            self.test_device_health
        ]
        
        # Run all tests
        for test_func in tests:
            test_func()
        
        # Generate summary
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.success)
        failed_tests = total_tests - passed_tests
        
        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "test_results": [result.to_dict() for result in self.test_results],
            "timestamp": datetime.now().isoformat(),
            "device_info": self.device_manager.detect_devices()
        }
        
        self.logger.info(f"Test suite completed: {passed_tests}/{total_tests} tests passed ({summary['success_rate']:.1f}%)")
        
        return summary
    
    def save_test_report(self, report: Dict[str, Any], filepath: str) -> None:
        """Save test report to file."""
        try:
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
            self.logger.info(f"Test report saved to: {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to save test report: {e}")
    
    def generate_test_report_html(self, report: Dict[str, Any]) -> str:
        """Generate HTML test report."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Kobo Notebook App - Device Test Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .summary {{ background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .test-result {{ margin: 10px 0; padding: 10px; border-radius: 3px; }}
                .pass {{ background-color: #d4edda; border-left: 5px solid #28a745; }}
                .fail {{ background-color: #f8d7da; border-left: 5px solid #dc3545; }}
                .device-info {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Kobo Notebook App - Device Test Report</h1>
                <p>Generated: {report['timestamp']}</p>
            </div>
            
            <div class="summary">
                <h2>Test Summary</h2>
                <p><strong>Total Tests:</strong> {report['total_tests']}</p>
                <p><strong>Passed:</strong> {report['passed_tests']}</p>
                <p><strong>Failed:</strong> {report['failed_tests']}</p>
                <p><strong>Success Rate:</strong> {report['success_rate']:.1f}%</p>
            </div>
            
            <div class="device-info">
                <h2>Device Information</h2>
                <pre>{json.dumps(report['device_info'], indent=2)}</pre>
            </div>
            
            <h2>Test Results</h2>
        """
        
        for result in report['test_results']:
            status_class = "pass" if result['success'] else "fail"
            status_icon = "✓" if result['success'] else "✗"
            
            html += f"""
            <div class="test-result {status_class}">
                <h3>{status_icon} {result['test_name']}</h3>
                <p><strong>Status:</strong> {result['message']}</p>
                <p><strong>Duration:</strong> {result['duration']:.2f} seconds</p>
                <p><strong>Timestamp:</strong> {result['timestamp']}</p>
            </div>
            """
        
        html += """
        </body>
        </html>
        """
        
        return html


if __name__ == "__main__":
    # Run test suite when executed directly
    tester = DeviceTestSuite()
    report = tester.run_full_test_suite()
    
    # Save report
    report_path = "device_test_report.json"
    tester.save_test_report(report, report_path)
    
    # Generate HTML report
    html_report = tester.generate_test_report_html(report)
    with open("device_test_report.html", 'w') as f:
        f.write(html_report)
    
    print(f"\nTest Report Summary:")
    print(f"Total Tests: {report['total_tests']}")
    print(f"Passed: {report['passed_tests']}")
    print(f"Failed: {report['failed_tests']}")
    print(f"Success Rate: {report['success_rate']:.1f}%")
    print(f"\nReports saved:")
    print(f"- JSON: {report_path}")
    print(f"- HTML: device_test_report.html")