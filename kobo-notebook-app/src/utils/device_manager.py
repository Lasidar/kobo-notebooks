"""
Device management utilities for Kobo Elipsa 2e.

This module provides functionality to detect, manage, and interact with
Kobo Elipsa 2e devices.
"""

import os
import shutil
import json
from pathlib import Path
from typing import List, Dict, Optional
import sqlite3
import re

from .logger import setup_logger


class DeviceManager:
    """Manages Kobo device detection and operations."""
    
    def __init__(self):
        """Initialize the device manager."""
        self.logger = setup_logger()
        self.connected_device = None
        
    def detect_devices(self) -> List[Dict]:
        """
        Detect connected Kobo devices.
        
        Returns:
            List[Dict]: List of detected device information
        """
        devices = []
        
        try:
            # Common mount points for Kobo devices
            mount_points = [
                "/media", "/mnt", "/Volumes",  # Linux/macOS
                "D:", "E:", "F:", "G:", "H:", "I:", "J:", "K:", "L:", "M:",  # Windows
            ]
            
            for mount_point in mount_points:
                if os.path.exists(mount_point):
                    for item in os.listdir(mount_point):
                        device_path = os.path.join(mount_point, item)
                        if os.path.isdir(device_path):
                            # Check if this looks like a Kobo device
                            if self._is_kobo_device(device_path):
                                device_info = self._get_device_info(device_path)
                                if device_info:
                                    devices.append(device_info)
                                    self.connected_device = device_path
                                    break
            
            self.logger.info(f"Detected {len(devices)} Kobo device(s)")
            
        except Exception as e:
            self.logger.error(f"Error detecting devices: {e}")
            
        return devices
    
    def _is_kobo_device(self, path: str) -> bool:
        """
        Check if a path contains a Kobo device.
        
        Args:
            path (str): Path to check
            
        Returns:
            bool: True if this appears to be a Kobo device
        """
        try:
            # Check for Kobo-specific files and directories
            kobo_indicators = [
                ".kobo",
                "KoboReader.sqlite",
                ".adobe-digital-editions",
                ".kobo-kana"
            ]
            
            for indicator in kobo_indicators:
                if os.path.exists(os.path.join(path, indicator)):
                    return True
                    
            # Check if the device name contains "Kobo" or "Elipsa"
            device_name = os.path.basename(path).lower()
            if "kobo" in device_name or "elipsa" in device_name:
                return True
                
        except Exception as e:
            self.logger.debug(f"Error checking device at {path}: {e}")
            
        return False
    
    def _get_device_info(self, device_path: str) -> Optional[Dict]:
        """
        Get information about a Kobo device.
        
        Args:
            device_path (str): Path to the device
            
        Returns:
            Optional[Dict]: Device information dictionary
        """
        try:
            device_info = {
                "path": device_path,
                "model": "Unknown",
                "firmware": "Unknown",
                "storage": "Unknown",
                "template_count": 0
            }
            
            # Try to get model information
            device_info["model"] = self._get_device_model(device_path)
            
            # Try to get firmware version
            device_info["firmware"] = self._get_firmware_version(device_path)
            
            # Try to get storage information
            device_info["storage"] = self._get_storage_info(device_path)
            
            # Try to count existing templates
            device_info["template_count"] = self._count_templates(device_path)
            
            return device_info
            
        except Exception as e:
            self.logger.error(f"Error getting device info for {device_path}: {e}")
            return None
    
    def _get_device_model(self, device_path: str) -> str:
        """Get the device model from device information."""
        try:
            # Check for model information in various locations
            model_files = [
                ".kobo/version",
                ".kobo/device",
                "KoboReader.sqlite"
            ]
            
            for model_file in model_files:
                file_path = os.path.join(device_path, model_file)
                if os.path.exists(file_path):
                    if file_path.endswith('.sqlite'):
                        # Query database for model info
                        return self._get_model_from_db(file_path)
                    else:
                        # Read from text file
                        with open(file_path, 'r') as f:
                            content = f.read()
                            if 'elipsa' in content.lower():
                                return "Kobo Elipsa 2e"
                            elif 'elipsa' in content.lower():
                                return "Kobo Elipsa"
                            
        except Exception as e:
            self.logger.debug(f"Error getting device model: {e}")
            
        return "Kobo Elipsa 2e"  # Default assumption
    
    def _get_firmware_version(self, device_path: str) -> str:
        """Get the firmware version."""
        try:
            version_file = os.path.join(device_path, ".kobo", "version")
            if os.path.exists(version_file):
                with open(version_file, 'r') as f:
                    return f.read().strip()
        except Exception as e:
            self.logger.debug(f"Error getting firmware version: {e}")
            
        return "Unknown"
    
    def _get_storage_info(self, device_path: str) -> str:
        """Get storage information."""
        try:
            # Get total and free space
            total, used, free = shutil.disk_usage(device_path)
            
            # Convert to human readable format
            def format_bytes(bytes_size):
                for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                    if bytes_size < 1024.0:
                        return f"{bytes_size:.1f} {unit}"
                    bytes_size /= 1024.0
                return f"{bytes_size:.1f} PB"
            
            return f"{format_bytes(free)} free of {format_bytes(total)}"
            
        except Exception as e:
            self.logger.debug(f"Error getting storage info: {e}")
            
        return "Unknown"
    
    def _get_model_from_db(self, db_path: str) -> str:
        """Get model information from KoboReader.sqlite."""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Try to get device information
            cursor.execute("SELECT value FROM settings WHERE key = 'deviceName'")
            result = cursor.fetchone()
            if result:
                return result[0]
                
        except Exception as e:
            self.logger.debug(f"Error querying database for model: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
                
        return "Unknown"
    
    def _count_templates(self, device_path: str) -> int:
        """Count existing templates on the device."""
        try:
            # This is a placeholder - we'll need to determine the actual
            # template location through reverse engineering
            template_dirs = [
                ".kobo/templates",
                ".kobo/notebook_templates",
                ".kobo/apps/notebook/templates"
            ]
            
            for template_dir in template_dirs:
                full_path = os.path.join(device_path, template_dir)
                if os.path.exists(full_path):
                    # Count image files in template directory
                    count = 0
                    for file in os.listdir(full_path):
                        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                            count += 1
                    return count
                    
        except Exception as e:
            self.logger.debug(f"Error counting templates: {e}")
            
        return 0
    
    def has_connected_device(self) -> bool:
        """Check if a device is currently connected."""
        return self.connected_device is not None and os.path.exists(self.connected_device)
    
    def create_backup(self, backup_dir: str) -> None:
        """
        Create a backup of the connected device.
        
        Args:
            backup_dir (str): Directory to store the backup
        """
        if not self.has_connected_device():
            raise ValueError("No connected device")
            
        try:
            backup_path = Path(backup_dir)
            backup_path.mkdir(parents=True, exist_ok=True)
            
            # Create timestamped backup directory
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            device_backup_dir = backup_path / f"kobo_backup_{timestamp}"
            device_backup_dir.mkdir()
            
            # Backup critical directories
            critical_dirs = [".kobo", "KoboReader.sqlite"]
            
            for item in critical_dirs:
                src = os.path.join(self.connected_device, item)
                if os.path.exists(src):
                    dst = device_backup_dir / item
                    if os.path.isdir(src):
                        shutil.copytree(src, dst)
                    else:
                        shutil.copy2(src, dst)
            
            # Create backup manifest
            manifest = {
                "timestamp": timestamp,
                "device_path": self.connected_device,
                "backup_items": critical_dirs,
                "version": "0.1.0"
            }
            
            manifest_file = device_backup_dir / "backup_manifest.json"
            with open(manifest_file, 'w') as f:
                json.dump(manifest, f, indent=2)
                
            self.logger.info(f"Backup created: {device_backup_dir}")
            
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
            raise
    
    def restore_backup(self, backup_file: str) -> None:
        """
        Restore a backup to the connected device.
        
        Args:
            backup_file (str): Path to the backup file
        """
        if not self.has_connected_device():
            raise ValueError("No connected device")
            
        try:
            # This is a placeholder implementation
            # In a real implementation, we would:
            # 1. Validate the backup file
            # 2. Create a new backup of current state
            # 3. Restore the backup files
            # 4. Verify the restoration
            
            self.logger.info(f"Restoring backup from {backup_file}")
            # Implementation would go here
            
        except Exception as e:
            self.logger.error(f"Error restoring backup: {e}")
            raise