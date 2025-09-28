"""
Device diagnostics and health monitoring utilities.

This module provides functionality to monitor device health, diagnose
issues, and provide recommendations for optimal performance.
"""

import os
import shutil
import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from utils.logger import setup_logger


class HealthStatus(Enum):
    """Device health status enumeration."""
    EXCELLENT = "excellent"
    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


@dataclass
class DiagnosticResult:
    """Represents a diagnostic test result."""
    name: str
    status: HealthStatus
    message: str
    details: Dict[str, Any]
    recommendations: List[str]
    timestamp: datetime


@dataclass
class DeviceHealth:
    """Represents overall device health."""
    overall_status: HealthStatus
    score: float  # 0-100
    diagnostics: List[DiagnosticResult]
    last_checked: datetime
    recommendations: List[str]


class DeviceDiagnostics:
    """Device diagnostics and health monitoring system."""
    
    def __init__(self):
        """Initialize the device diagnostics system."""
        self.logger = setup_logger()
        
    def run_full_diagnostics(self, device_path: str) -> DeviceHealth:
        """
        Run full device diagnostics.
        
        Args:
            device_path (str): Path to the device
            
        Returns:
            DeviceHealth: Complete device health report
        """
        try:
            self.logger.info(f"Running full diagnostics on device: {device_path}")
            
            diagnostics = []
            
            # Run individual diagnostic tests
            diagnostics.append(self._check_device_connectivity(device_path))
            diagnostics.append(self._check_storage_health(device_path))
            diagnostics.append(self._check_firmware_health(device_path))
            diagnostics.append(self._check_database_health(device_path))
            diagnostics.append(self._check_template_health(device_path))
            diagnostics.append(self._check_file_system_health(device_path))
            diagnostics.append(self._check_performance_health(device_path))
            
            # Calculate overall health
            overall_status, score = self._calculate_overall_health(diagnostics)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(diagnostics)
            
            health = DeviceHealth(
                overall_status=overall_status,
                score=score,
                diagnostics=diagnostics,
                last_checked=datetime.now(),
                recommendations=recommendations
            )
            
            self.logger.info(f"Diagnostics completed. Overall status: {overall_status.value}, Score: {score}")
            
            return health
            
        except Exception as e:
            self.logger.error(f"Error running diagnostics: {e}")
            # Return error health status
            return DeviceHealth(
                overall_status=HealthStatus.UNKNOWN,
                score=0.0,
                diagnostics=[],
                last_checked=datetime.now(),
                recommendations=[f"Diagnostic error: {e}"]
            )
    
    def _check_device_connectivity(self, device_path: str) -> DiagnosticResult:
        """Check device connectivity and basic access."""
        try:
            if not os.path.exists(device_path):
                return DiagnosticResult(
                    name="Device Connectivity",
                    status=HealthStatus.CRITICAL,
                    message="Device not accessible",
                    details={"path": device_path, "exists": False},
                    recommendations=["Check USB connection", "Verify device is mounted"],
                    timestamp=datetime.now()
                )
            
            # Check if we can read from the device
            try:
                os.listdir(device_path)
                readable = True
            except PermissionError:
                readable = False
            
            if not readable:
                return DiagnosticResult(
                    name="Device Connectivity",
                    status=HealthStatus.CRITICAL,
                    message="Device not readable",
                    details={"path": device_path, "readable": False},
                    recommendations=["Check file permissions", "Run as administrator"],
                    timestamp=datetime.now()
                )
            
            # Check for Kobo-specific files
            kobo_files = [".kobo", "KoboReader.sqlite"]
            found_files = []
            for file in kobo_files:
                if os.path.exists(os.path.join(device_path, file)):
                    found_files.append(file)
            
            if len(found_files) == len(kobo_files):
                status = HealthStatus.EXCELLENT
                message = "Device fully accessible"
            elif len(found_files) > 0:
                status = HealthStatus.GOOD
                message = "Device partially accessible"
            else:
                status = HealthStatus.WARNING
                message = "Device accessible but may not be a Kobo device"
            
            return DiagnosticResult(
                name="Device Connectivity",
                status=status,
                message=message,
                details={
                    "path": device_path,
                    "readable": True,
                    "kobo_files_found": found_files
                },
                recommendations=[],
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return DiagnosticResult(
                name="Device Connectivity",
                status=HealthStatus.CRITICAL,
                message=f"Connectivity check failed: {e}",
                details={"error": str(e)},
                recommendations=["Check device connection", "Restart device"],
                timestamp=datetime.now()
            )
    
    def _check_storage_health(self, device_path: str) -> DiagnosticResult:
        """Check device storage health."""
        try:
            # Get disk usage
            total, used, free = shutil.disk_usage(device_path)
            
            # Calculate percentages
            used_percent = (used / total) * 100
            free_percent = (free / total) * 100
            
            # Determine status based on free space
            if free_percent > 20:
                status = HealthStatus.EXCELLENT
                message = f"Plenty of free space ({free_percent:.1f}%)"
            elif free_percent > 10:
                status = HealthStatus.GOOD
                message = f"Good free space ({free_percent:.1f}%)"
            elif free_percent > 5:
                status = HealthStatus.WARNING
                message = f"Low free space ({free_percent:.1f}%)"
            else:
                status = HealthStatus.CRITICAL
                message = f"Critical low space ({free_percent:.1f}%)"
            
            recommendations = []
            if free_percent < 10:
                recommendations.append("Free up storage space")
                recommendations.append("Remove unused files")
            if free_percent < 5:
                recommendations.append("URGENT: Free up space immediately")
            
            return DiagnosticResult(
                name="Storage Health",
                status=status,
                message=message,
                details={
                    "total_bytes": total,
                    "used_bytes": used,
                    "free_bytes": free,
                    "used_percent": used_percent,
                    "free_percent": free_percent
                },
                recommendations=recommendations,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return DiagnosticResult(
                name="Storage Health",
                status=HealthStatus.CRITICAL,
                message=f"Storage check failed: {e}",
                details={"error": str(e)},
                recommendations=["Check device storage", "Restart device"],
                timestamp=datetime.now()
            )
    
    def _check_firmware_health(self, device_path: str) -> DiagnosticResult:
        """Check firmware health and version."""
        try:
            version_file = os.path.join(device_path, ".kobo", "version")
            
            if not os.path.exists(version_file):
                return DiagnosticResult(
                    name="Firmware Health",
                    status=HealthStatus.WARNING,
                    message="Firmware version file not found",
                    details={"version_file_exists": False},
                    recommendations=["Check device firmware", "Update firmware if needed"],
                    timestamp=datetime.now()
                )
            
            # Read firmware version
            with open(version_file, 'r') as f:
                firmware_version = f.read().strip()
            
            # Check if firmware is recent (basic check)
            # This would need to be updated with actual version checking logic
            status = HealthStatus.GOOD
            message = f"Firmware version: {firmware_version}"
            recommendations = []
            
            # Add recommendations based on version (placeholder logic)
            if "4.0" in firmware_version:
                recommendations.append("Consider updating to latest firmware")
            
            return DiagnosticResult(
                name="Firmware Health",
                status=status,
                message=message,
                details={
                    "version_file_exists": True,
                    "firmware_version": firmware_version
                },
                recommendations=recommendations,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return DiagnosticResult(
                name="Firmware Health",
                status=HealthStatus.WARNING,
                message=f"Firmware check failed: {e}",
                details={"error": str(e)},
                recommendations=["Check firmware status", "Update firmware"],
                timestamp=datetime.now()
            )
    
    def _check_database_health(self, device_path: str) -> DiagnosticResult:
        """Check database health."""
        try:
            db_path = os.path.join(device_path, "KoboReader.sqlite")
            
            if not os.path.exists(db_path):
                return DiagnosticResult(
                    name="Database Health",
                    status=HealthStatus.CRITICAL,
                    message="Main database not found",
                    details={"database_exists": False},
                    recommendations=["Check device integrity", "Restore from backup"],
                    timestamp=datetime.now()
                )
            
            # Check database integrity
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Run integrity check
            cursor.execute("PRAGMA integrity_check")
            integrity_result = cursor.fetchone()
            
            # Check database size
            db_size = os.path.getsize(db_path)
            
            # Check for common tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            conn.close()
            
            # Determine status
            if integrity_result[0] == "ok":
                status = HealthStatus.EXCELLENT
                message = "Database integrity check passed"
            else:
                status = HealthStatus.CRITICAL
                message = f"Database integrity issues: {integrity_result[0]}"
            
            recommendations = []
            if integrity_result[0] != "ok":
                recommendations.append("Backup database immediately")
                recommendations.append("Consider database repair")
            
            return DiagnosticResult(
                name="Database Health",
                status=status,
                message=message,
                details={
                    "database_exists": True,
                    "database_size": db_size,
                    "integrity_check": integrity_result[0],
                    "tables_count": len(tables),
                    "tables": tables[:10]  # First 10 tables
                },
                recommendations=recommendations,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return DiagnosticResult(
                name="Database Health",
                status=HealthStatus.CRITICAL,
                message=f"Database check failed: {e}",
                details={"error": str(e)},
                recommendations=["Check database integrity", "Backup database"],
                timestamp=datetime.now()
            )
    
    def _check_template_health(self, device_path: str) -> DiagnosticResult:
        """Check template-related health."""
        try:
            # Check for template directories
            template_dirs = [
                ".kobo/templates",
                ".kobo/notebook_templates",
                ".kobo/apps/notebook/templates"
            ]
            
            found_dirs = []
            template_count = 0
            
            for template_dir in template_dirs:
                full_path = os.path.join(device_path, template_dir)
                if os.path.exists(full_path):
                    found_dirs.append(template_dir)
                    # Count template files
                    for file in os.listdir(full_path):
                        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                            template_count += 1
            
            if found_dirs:
                status = HealthStatus.GOOD
                message = f"Found {template_count} templates in {len(found_dirs)} directories"
            else:
                status = HealthStatus.WARNING
                message = "No template directories found"
            
            recommendations = []
            if not found_dirs:
                recommendations.append("Template system may not be initialized")
            if template_count == 0:
                recommendations.append("No custom templates found")
            
            return DiagnosticResult(
                name="Template Health",
                status=status,
                message=message,
                details={
                    "template_directories": found_dirs,
                    "template_count": template_count
                },
                recommendations=recommendations,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return DiagnosticResult(
                name="Template Health",
                status=HealthStatus.WARNING,
                message=f"Template check failed: {e}",
                details={"error": str(e)},
                recommendations=["Check template system"],
                timestamp=datetime.now()
            )
    
    def _check_file_system_health(self, device_path: str) -> DiagnosticResult:
        """Check file system health."""
        try:
            # Check for common issues
            issues = []
            
            # Check for hidden files
            hidden_files = []
            for root, dirs, files in os.walk(device_path):
                for file in files:
                    if file.startswith('.'):
                        hidden_files.append(os.path.join(root, file))
            
            # Check for large files
            large_files = []
            for root, dirs, files in os.walk(device_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        size = os.path.getsize(file_path)
                        if size > 100 * 1024 * 1024:  # 100MB
                            large_files.append((file, size))
                    except:
                        pass
            
            # Check for permission issues
            permission_issues = []
            try:
                test_file = os.path.join(device_path, ".kobo", "test_write")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
            except:
                permission_issues.append("Cannot write to .kobo directory")
            
            # Determine status
            if not issues and not permission_issues:
                status = HealthStatus.EXCELLENT
                message = "File system appears healthy"
            elif len(issues) < 3:
                status = HealthStatus.GOOD
                message = "File system mostly healthy"
            else:
                status = HealthStatus.WARNING
                message = "File system has some issues"
            
            recommendations = []
            if permission_issues:
                recommendations.append("Check file permissions")
            if large_files:
                recommendations.append("Consider cleaning up large files")
            
            return DiagnosticResult(
                name="File System Health",
                status=status,
                message=message,
                details={
                    "hidden_files_count": len(hidden_files),
                    "large_files_count": len(large_files),
                    "permission_issues": permission_issues
                },
                recommendations=recommendations,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return DiagnosticResult(
                name="File System Health",
                status=HealthStatus.WARNING,
                message=f"File system check failed: {e}",
                details={"error": str(e)},
                recommendations=["Check file system integrity"],
                timestamp=datetime.now()
            )
    
    def _check_performance_health(self, device_path: str) -> DiagnosticResult:
        """Check device performance indicators."""
        try:
            # Measure file access speed
            start_time = datetime.now()
            
            # Try to read a small file
            test_files = [
                os.path.join(device_path, ".kobo", "version"),
                os.path.join(device_path, "KoboReader.sqlite")
            ]
            
            read_times = []
            for test_file in test_files:
                if os.path.exists(test_file):
                    start = datetime.now()
                    try:
                        with open(test_file, 'rb') as f:
                            f.read(1024)  # Read 1KB
                        end = datetime.now()
                        read_times.append((end - start).total_seconds())
                    except:
                        pass
            
            # Calculate average read time
            if read_times:
                avg_read_time = sum(read_times) / len(read_times)
            else:
                avg_read_time = 0
            
            # Determine status based on read time
            if avg_read_time < 0.1:
                status = HealthStatus.EXCELLENT
                message = "Excellent performance"
            elif avg_read_time < 0.5:
                status = HealthStatus.GOOD
                message = "Good performance"
            elif avg_read_time < 1.0:
                status = HealthStatus.WARNING
                message = "Slow performance"
            else:
                status = HealthStatus.CRITICAL
                message = "Very slow performance"
            
            recommendations = []
            if avg_read_time > 0.5:
                recommendations.append("Device may be slow - check for issues")
            if avg_read_time > 1.0:
                recommendations.append("Consider device maintenance")
            
            return DiagnosticResult(
                name="Performance Health",
                status=status,
                message=message,
                details={
                    "average_read_time": avg_read_time,
                    "read_times": read_times
                },
                recommendations=recommendations,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return DiagnosticResult(
                name="Performance Health",
                status=HealthStatus.WARNING,
                message=f"Performance check failed: {e}",
                details={"error": str(e)},
                recommendations=["Check device performance"],
                timestamp=datetime.now()
            )
    
    def _calculate_overall_health(self, diagnostics: List[DiagnosticResult]) -> Tuple[HealthStatus, float]:
        """Calculate overall device health."""
        if not diagnostics:
            return HealthStatus.UNKNOWN, 0.0
        
        # Weight different diagnostics
        weights = {
            "Device Connectivity": 0.25,
            "Storage Health": 0.20,
            "Firmware Health": 0.15,
            "Database Health": 0.20,
            "Template Health": 0.10,
            "File System Health": 0.05,
            "Performance Health": 0.05
        }
        
        # Convert status to numeric score
        status_scores = {
            HealthStatus.EXCELLENT: 100,
            HealthStatus.GOOD: 80,
            HealthStatus.WARNING: 60,
            HealthStatus.CRITICAL: 20,
            HealthStatus.UNKNOWN: 0
        }
        
        total_score = 0.0
        total_weight = 0.0
        
        for diagnostic in diagnostics:
            weight = weights.get(diagnostic.name, 0.1)
            score = status_scores.get(diagnostic.status, 0)
            total_score += score * weight
            total_weight += weight
        
        if total_weight > 0:
            final_score = total_score / total_weight
        else:
            final_score = 0.0
        
        # Determine overall status
        if final_score >= 90:
            overall_status = HealthStatus.EXCELLENT
        elif final_score >= 75:
            overall_status = HealthStatus.GOOD
        elif final_score >= 50:
            overall_status = HealthStatus.WARNING
        else:
            overall_status = HealthStatus.CRITICAL
        
        return overall_status, final_score
    
    def _generate_recommendations(self, diagnostics: List[DiagnosticResult]) -> List[str]:
        """Generate overall recommendations based on diagnostics."""
        recommendations = []
        
        # Collect all recommendations
        for diagnostic in diagnostics:
            recommendations.extend(diagnostic.recommendations)
        
        # Remove duplicates and prioritize
        unique_recommendations = list(set(recommendations))
        
        # Prioritize critical recommendations
        critical_keywords = ["URGENT", "immediately", "critical", "backup"]
        normal_recommendations = []
        
        for rec in unique_recommendations:
            if any(keyword in rec.lower() for keyword in critical_keywords):
                recommendations.insert(0, rec)
            else:
                normal_recommendations.append(rec)
        
        recommendations.extend(normal_recommendations)
        
        return recommendations[:10]  # Limit to top 10 recommendations
    
    def save_health_report(self, health: DeviceHealth, device_path: str) -> str:
        """Save health report to file."""
        try:
            reports_dir = Path.home() / ".kobo_notebook_app" / "reports"
            reports_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = health.last_checked.strftime("%Y%m%d_%H%M%S")
            device_name = os.path.basename(device_path).replace(" ", "_")
            report_file = reports_dir / f"health_report_{device_name}_{timestamp}.json"
            
            # Convert to serializable format
            report_data = {
                "overall_status": health.overall_status.value,
                "score": health.score,
                "last_checked": health.last_checked.isoformat(),
                "recommendations": health.recommendations,
                "diagnostics": []
            }
            
            for diagnostic in health.diagnostics:
                report_data["diagnostics"].append({
                    "name": diagnostic.name,
                    "status": diagnostic.status.value,
                    "message": diagnostic.message,
                    "details": diagnostic.details,
                    "recommendations": diagnostic.recommendations,
                    "timestamp": diagnostic.timestamp.isoformat()
                })
            
            with open(report_file, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            self.logger.info(f"Saved health report: {report_file}")
            return str(report_file)
            
        except Exception as e:
            self.logger.error(f"Error saving health report: {e}")
            return ""
    
    def load_health_report(self, report_path: str) -> Optional[DeviceHealth]:
        """Load health report from file."""
        try:
            with open(report_path, 'r') as f:
                report_data = json.load(f)
            
            diagnostics = []
            for diag_data in report_data["diagnostics"]:
                diagnostic = DiagnosticResult(
                    name=diag_data["name"],
                    status=HealthStatus(diag_data["status"]),
                    message=diag_data["message"],
                    details=diag_data["details"],
                    recommendations=diag_data["recommendations"],
                    timestamp=datetime.fromisoformat(diag_data["timestamp"])
                )
                diagnostics.append(diagnostic)
            
            health = DeviceHealth(
                overall_status=HealthStatus(report_data["overall_status"]),
                score=report_data["score"],
                diagnostics=diagnostics,
                last_checked=datetime.fromisoformat(report_data["last_checked"]),
                recommendations=report_data["recommendations"]
            )
            
            return health
            
        except Exception as e:
            self.logger.error(f"Error loading health report: {e}")
            return None