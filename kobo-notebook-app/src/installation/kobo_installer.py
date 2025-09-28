"""
Kobo installation system for custom templates.

This module provides functionality to create KoboRoot.tgz packages
and install custom templates on Kobo Elipsa 2e devices.
"""

import os
import tarfile
import json
import shutil
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

from utils.logger import setup_logger


class KoboInstaller:
    """Handles installation of custom templates on Kobo devices."""
    
    def __init__(self):
        """Initialize the Kobo installer."""
        self.logger = setup_logger()
        
    def create_installation_package(
        self,
        templates: List[str],
        output_path: str,
        package_name: Optional[str] = None
    ) -> str:
        """
        Create a KoboRoot.tgz installation package.
        
        Args:
            templates (List[str]): List of template file paths to include
            output_path (str): Directory where to save the package
            package_name (Optional[str]): Name for the package (defaults to timestamp)
            
        Returns:
            str: Path to the created package
        """
        try:
            if not package_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                package_name = f"kobo_templates_{timestamp}"
            
            # Create temporary directory for package contents
            temp_dir = Path(output_path) / "temp_package"
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            # Create the installation structure
            self._create_installation_structure(temp_dir, templates)
            
            # Create the KoboRoot.tgz package
            package_path = Path(output_path) / f"{package_name}.tgz"
            
            with tarfile.open(package_path, "w:gz") as tar:
                tar.add(temp_dir, arcname=".")
            
            # Clean up temporary directory
            shutil.rmtree(temp_dir)
            
            self.logger.info(f"Created installation package: {package_path}")
            return str(package_path)
            
        except Exception as e:
            self.logger.error(f"Error creating installation package: {e}")
            raise
    
    def _create_installation_structure(self, temp_dir: Path, templates: List[str]) -> None:
        """
        Create the directory structure for the installation package.
        
        Args:
            temp_dir (Path): Temporary directory for package contents
            templates (List[str]): List of template files to include
        """
        try:
            # This is a placeholder implementation based on research findings
            # The actual directory structure will need to be determined through
            # reverse engineering of the Kobo Elipsa 2e firmware
            
            # Create the package manifest
            manifest = self._create_manifest(templates)
            manifest_file = temp_dir / "manifest.json"
            with open(manifest_file, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            # Create template directories
            # These paths are speculative and will need to be verified
            template_dirs = [
                "usr/local/kobo/notebook/templates",
                "usr/local/kobo/templates",
                ".kobo/templates"
            ]
            
            for template_dir in template_dirs:
                (temp_dir / template_dir).mkdir(parents=True, exist_ok=True)
            
            # Copy templates to appropriate locations
            for template_path in templates:
                template_file = Path(template_path)
                if template_file.exists():
                    # Copy to each potential template directory
                    for template_dir in template_dirs:
                        dest_dir = temp_dir / template_dir
                        shutil.copy2(template_file, dest_dir / template_file.name)
            
            # Create installation scripts
            self._create_installation_scripts(temp_dir)
            
            self.logger.info("Created installation structure")
            
        except Exception as e:
            self.logger.error(f"Error creating installation structure: {e}")
            raise
    
    def _create_manifest(self, templates: List[str]) -> Dict:
        """
        Create a manifest for the installation package.
        
        Args:
            templates (List[str]): List of template files
            
        Returns:
            Dict: Package manifest
        """
        manifest = {
            "package_name": "kobo_custom_templates",
            "version": "0.1.0",
            "description": "Custom notebook templates for Kobo Elipsa 2e",
            "author": "Kobo Notebook App",
            "created": datetime.now().isoformat(),
            "device_compatibility": ["Kobo Elipsa 2e"],
            "templates": [],
            "installation_notes": [
                "This package installs custom notebook templates",
                "Backup your device before installation",
                "Restart your device after installation"
            ]
        }
        
        for template_path in templates:
            template_file = Path(template_path)
            if template_file.exists():
                template_info = {
                    "filename": template_file.name,
                    "size": template_file.stat().st_size,
                    "created": datetime.fromtimestamp(
                        template_file.stat().st_ctime
                    ).isoformat()
                }
                manifest["templates"].append(template_info)
        
        return manifest
    
    def _create_installation_scripts(self, temp_dir: Path) -> None:
        """
        Create installation scripts for the package.
        
        Args:
            temp_dir (Path): Temporary directory for package contents
        """
        try:
            # Create pre-installation script
            pre_install_script = temp_dir / "preinstall"
            with open(pre_install_script, 'w') as f:
                f.write("""#!/bin/sh
# Pre-installation script for Kobo custom templates

echo "Preparing to install custom notebook templates..."

# Create backup of existing templates
if [ -d "/mnt/onboard/.kobo/templates" ]; then
    echo "Backing up existing templates..."
    cp -r /mnt/onboard/.kobo/templates /mnt/onboard/.kobo/templates.backup.$(date +%Y%m%d_%H%M%S)
fi

echo "Pre-installation completed."
""")
            os.chmod(pre_install_script, 0o755)
            
            # Create post-installation script
            post_install_script = temp_dir / "postinstall"
            with open(post_install_script, 'w') as f:
                f.write("""#!/bin/sh
# Post-installation script for Kobo custom templates

echo "Installing custom notebook templates..."

# Set proper permissions
if [ -d "/mnt/onboard/.kobo/templates" ]; then
    chmod -R 644 /mnt/onboard/.kobo/templates/*
    chmod 755 /mnt/onboard/.kobo/templates
fi

# Update template database (placeholder)
# This would need to be implemented based on reverse engineering
echo "Updating template database..."

echo "Custom templates installed successfully."
echo "Please restart your device to see the new templates."
""")
            os.chmod(post_install_script, 0o755)
            
            self.logger.info("Created installation scripts")
            
        except Exception as e:
            self.logger.error(f"Error creating installation scripts: {e}")
            raise
    
    def install_package(self, package_path: str, device_path: str) -> bool:
        """
        Install a package on a Kobo device.
        
        Args:
            package_path (str): Path to the KoboRoot.tgz package
            device_path (str): Path to the mounted Kobo device
            
        Returns:
            bool: True if installation was successful
        """
        try:
            # Validate package
            if not self._validate_package(package_path):
                raise ValueError("Invalid package format")
            
            # Copy package to device
            device_package_path = Path(device_path) / "KoboRoot.tgz"
            shutil.copy2(package_path, device_package_path)
            
            self.logger.info(f"Package copied to device: {device_package_path}")
            
            # Installation will be completed when device restarts
            self.logger.info("Package installed. Device restart required.")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error installing package: {e}")
            return False
    
    def _validate_package(self, package_path: str) -> bool:
        """
        Validate a KoboRoot.tgz package.
        
        Args:
            package_path (str): Path to the package
            
        Returns:
            bool: True if package is valid
        """
        try:
            if not os.path.exists(package_path):
                return False
            
            # Check if it's a valid tar.gz file
            with tarfile.open(package_path, "r:gz") as tar:
                # Check for required files
                required_files = ["manifest.json", "preinstall", "postinstall"]
                tar_files = tar.getnames()
                
                for required_file in required_files:
                    if required_file not in tar_files:
                        self.logger.warning(f"Missing required file: {required_file}")
                        return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating package: {e}")
            return False
    
    def uninstall_templates(self, device_path: str, template_names: List[str]) -> bool:
        """
        Uninstall specific templates from a device.
        
        Args:
            device_path (str): Path to the mounted Kobo device
            template_names (List[str]): Names of templates to uninstall
            
        Returns:
            bool: True if uninstallation was successful
        """
        try:
            # This is a placeholder implementation
            # The actual uninstallation process will depend on how templates
            # are stored and managed on the device
            
            template_dir = Path(device_path) / ".kobo" / "templates"
            
            if not template_dir.exists():
                self.logger.warning("Template directory not found")
                return False
            
            removed_count = 0
            for template_name in template_names:
                template_file = template_dir / template_name
                if template_file.exists():
                    template_file.unlink()
                    removed_count += 1
                    self.logger.info(f"Removed template: {template_name}")
            
            self.logger.info(f"Uninstalled {removed_count} templates")
            return True
            
        except Exception as e:
            self.logger.error(f"Error uninstalling templates: {e}")
            return False
    
    def list_installed_templates(self, device_path: str) -> List[Dict]:
        """
        List templates installed on a device.
        
        Args:
            device_path (str): Path to the mounted Kobo device
            
        Returns:
            List[Dict]: List of installed template information
        """
        templates = []
        
        try:
            # Check multiple possible template locations
            template_dirs = [
                Path(device_path) / ".kobo" / "templates",
                Path(device_path) / "usr" / "local" / "kobo" / "templates",
                Path(device_path) / ".kobo" / "notebook" / "templates"
            ]
            
            for template_dir in template_dirs:
                if template_dir.exists():
                    for template_file in template_dir.glob("*"):
                        if template_file.is_file() and template_file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                            template_info = {
                                "name": template_file.name,
                                "path": str(template_file),
                                "size": template_file.stat().st_size,
                                "created": datetime.fromtimestamp(
                                    template_file.stat().st_ctime
                                ).isoformat(),
                                "directory": str(template_dir)
                            }
                            templates.append(template_info)
            
            self.logger.info(f"Found {len(templates)} installed templates")
            
        except Exception as e:
            self.logger.error(f"Error listing installed templates: {e}")
        
        return templates