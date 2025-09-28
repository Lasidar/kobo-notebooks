"""
Template management and sharing utilities.

This module provides functionality for importing, exporting, and sharing
templates between users and devices.
"""

import os
import json
import shutil
import zipfile
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib

from utils.logger import setup_logger


class TemplateManager:
    """Manages template import/export and sharing functionality."""
    
    def __init__(self, templates_dir: str = None):
        """Initialize the template manager."""
        self.logger = setup_logger()
        
        if templates_dir:
            self.templates_dir = Path(templates_dir)
        else:
            # Default templates directory
            self.templates_dir = Path(__file__).parent.parent.parent.parent / "templates"
        
        self.templates_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.import_dir = self.templates_dir / "imports"
        self.export_dir = self.templates_dir / "exports"
        self.shared_dir = self.templates_dir / "shared"
        
        for directory in [self.import_dir, self.export_dir, self.shared_dir]:
            directory.mkdir(exist_ok=True)
    
    def get_template_info(self, template_path: Path) -> Dict[str, Any]:
        """
        Get information about a template file.
        
        Args:
            template_path (Path): Path to the template file
            
        Returns:
            Dict[str, Any]: Template information
        """
        try:
            if not template_path.exists():
                return {}
            
            stat = template_path.stat()
            
            # Calculate file hash for integrity checking
            with open(template_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            
            info = {
                "filename": template_path.name,
                "path": str(template_path),
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "hash": file_hash,
                "extension": template_path.suffix.lower(),
                "category": self._determine_category(template_path.name)
            }
            
            return info
            
        except Exception as e:
            self.logger.error(f"Error getting template info for {template_path}: {e}")
            return {}
    
    def _determine_category(self, filename: str) -> str:
        """Determine template category based on filename."""
        filename_lower = filename.lower()
        
        if any(keyword in filename_lower for keyword in ["lined", "line"]):
            return "lined"
        elif "dot_grid" in filename_lower or ("dot" in filename_lower and "grid" in filename_lower):
            return "dot_grid"
        elif any(keyword in filename_lower for keyword in ["grid"]):
            return "grid"
        elif any(keyword in filename_lower for keyword in ["cornell"]):
            return "cornell"
        elif any(keyword in filename_lower for keyword in ["blank"]):
            return "blank"
        elif any(keyword in filename_lower for keyword in ["academic", "study"]):
            return "academic"
        elif any(keyword in filename_lower for keyword in ["creative", "writing"]):
            return "creative"
        elif any(keyword in filename_lower for keyword in ["meeting", "business"]):
            return "professional"
        elif any(keyword in filename_lower for keyword in ["technical", "drawing"]):
            return "technical"
        elif any(keyword in filename_lower for keyword in ["bullet", "journal"]):
            return "journaling"
        else:
            return "other"
    
    def list_templates(self, category: str = None) -> List[Dict[str, Any]]:
        """
        List all available templates.
        
        Args:
            category (str): Optional category filter
            
        Returns:
            List[Dict[str, Any]]: List of template information
        """
        templates = []
        
        try:
            # Get all template files
            template_files = []
            for ext in ['.png', '.jpg', '.jpeg']:
                template_files.extend(self.templates_dir.glob(f"*{ext}"))
            
            for template_file in template_files:
                info = self.get_template_info(template_file)
                if info:
                    if category is None or info.get('category') == category:
                        templates.append(info)
            
            # Sort by creation date (newest first)
            templates.sort(key=lambda x: x.get('created', ''), reverse=True)
            
            self.logger.info(f"Listed {len(templates)} templates")
            
        except Exception as e:
            self.logger.error(f"Error listing templates: {e}")
        
        return templates
    
    def export_template(self, template_path: str, export_path: str = None, 
                       include_metadata: bool = True) -> str:
        """
        Export a template to a file.
        
        Args:
            template_path (str): Path to the template to export
            export_path (str): Path where to export (optional)
            include_metadata (bool): Whether to include metadata file
            
        Returns:
            str: Path to the exported file
        """
        try:
            template_file = Path(template_path)
            if not template_file.exists():
                raise FileNotFoundError(f"Template not found: {template_path}")
            
            # Determine export path
            if export_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                export_filename = f"{template_file.stem}_export_{timestamp}.png"
                export_path = self.export_dir / export_filename
            
            export_path = Path(export_path)
            
            # Copy template file
            shutil.copy2(template_file, export_path)
            
            # Create metadata file if requested
            if include_metadata:
                metadata = self.get_template_info(template_file)
                metadata_path = export_path.with_suffix('.json')
                
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
            
            self.logger.info(f"Exported template to {export_path}")
            return str(export_path)
            
        except Exception as e:
            self.logger.error(f"Error exporting template: {e}")
            raise
    
    def export_template_package(self, template_paths: List[str], 
                               package_path: str = None) -> str:
        """
        Export multiple templates as a package.
        
        Args:
            template_paths (List[str]): List of template paths to export
            package_path (str): Path for the package file (optional)
            
        Returns:
            str: Path to the created package
        """
        try:
            if package_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                package_path = self.export_dir / f"template_package_{timestamp}.zip"
            
            package_path = Path(package_path)
            
            with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add templates
                for template_path in template_paths:
                    template_file = Path(template_path)
                    if template_file.exists():
                        zipf.write(template_file, template_file.name)
                        
                        # Add metadata
                        metadata = self.get_template_info(template_file)
                        metadata_filename = f"{template_file.stem}.json"
                        zipf.writestr(metadata_filename, json.dumps(metadata, indent=2))
                
                # Add package manifest
                manifest = {
                    "version": "1.0.0",
                    "created": datetime.now().isoformat(),
                    "templates": len(template_paths),
                    "description": "Template package exported from Kobo Notebook App"
                }
                zipf.writestr("package_manifest.json", json.dumps(manifest, indent=2))
            
            self.logger.info(f"Created template package: {package_path}")
            return str(package_path)
            
        except Exception as e:
            self.logger.error(f"Error creating template package: {e}")
            raise
    
    def import_template(self, import_path: str, target_name: str = None) -> str:
        """
        Import a template from a file.
        
        Args:
            import_path (str): Path to the template to import
            target_name (str): Target filename (optional)
            
        Returns:
            str: Path to the imported template
        """
        try:
            import_file = Path(import_path)
            if not import_file.exists():
                raise FileNotFoundError(f"Import file not found: {import_path}")
            
            # Determine target name
            if target_name is None:
                target_name = import_file.name
            
            # Ensure unique filename
            target_path = self.templates_dir / target_name
            counter = 1
            while target_path.exists():
                stem = Path(target_name).stem
                suffix = Path(target_name).suffix
                target_name = f"{stem}_{counter}{suffix}"
                target_path = self.templates_dir / target_name
                counter += 1
            
            # Copy file
            shutil.copy2(import_file, target_path)
            
            self.logger.info(f"Imported template to {target_path}")
            return str(target_path)
            
        except Exception as e:
            self.logger.error(f"Error importing template: {e}")
            raise
    
    def import_template_package(self, package_path: str) -> List[str]:
        """
        Import templates from a package file.
        
        Args:
            package_path (str): Path to the package file
            
        Returns:
            List[str]: List of imported template paths
        """
        try:
            package_file = Path(package_path)
            if not package_file.exists():
                raise FileNotFoundError(f"Package file not found: {package_path}")
            
            imported_templates = []
            
            with zipfile.ZipFile(package_file, 'r') as zipf:
                # Read package manifest
                manifest = {}
                try:
                    manifest_data = zipf.read("package_manifest.json")
                    manifest = json.loads(manifest_data.decode('utf-8'))
                except KeyError:
                    self.logger.warning("No package manifest found")
                
                # Extract templates
                for file_info in zipf.filelist:
                    if file_info.filename.endswith(('.png', '.jpg', '.jpeg')):
                        # Extract template
                        zipf.extract(file_info, self.templates_dir)
                        template_path = self.templates_dir / file_info.filename
                        imported_templates.append(str(template_path))
                        
                        self.logger.info(f"Imported template: {file_info.filename}")
            
            self.logger.info(f"Imported {len(imported_templates)} templates from package")
            return imported_templates
            
        except Exception as e:
            self.logger.error(f"Error importing template package: {e}")
            raise
    
    def validate_template(self, template_path: str) -> Dict[str, Any]:
        """
        Validate a template file.
        
        Args:
            template_path (str): Path to the template to validate
            
        Returns:
            Dict[str, Any]: Validation results
        """
        validation_result = {
            "valid": True,
            "warnings": [],
            "errors": []
        }
        
        try:
            template_file = Path(template_path)
            
            # Check if file exists
            if not template_file.exists():
                validation_result["valid"] = False
                validation_result["errors"].append("File does not exist")
                return validation_result
            
            # Check file extension
            if template_file.suffix.lower() not in ['.png', '.jpg', '.jpeg']:
                validation_result["warnings"].append(
                    f"Unusual file extension: {template_file.suffix}"
                )
            
            # Check file size
            file_size = template_file.stat().st_size
            if file_size > 10 * 1024 * 1024:  # 10MB
                validation_result["warnings"].append(
                    f"Large file size: {file_size / (1024*1024):.1f}MB"
                )
            elif file_size < 1024:  # 1KB
                validation_result["warnings"].append(
                    f"Very small file size: {file_size} bytes"
                )
            
            # Check if it's a valid image (basic check)
            try:
                with open(template_file, 'rb') as f:
                    header = f.read(8)
                    if not (header.startswith(b'\x89PNG') or 
                           header.startswith(b'\xff\xd8\xff') or
                           header.startswith(b'GIF')):
                        validation_result["warnings"].append(
                            "File may not be a valid image format"
                        )
            except Exception:
                validation_result["warnings"].append(
                    "Could not read file header"
                )
            
            self.logger.info(f"Validated template: {template_path}")
            
        except Exception as e:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Validation error: {e}")
            self.logger.error(f"Error validating template {template_path}: {e}")
        
        return validation_result
    
    def delete_template(self, template_path: str) -> bool:
        """
        Delete a template file.
        
        Args:
            template_path (str): Path to the template to delete
            
        Returns:
            bool: True if deletion was successful
        """
        try:
            template_file = Path(template_path)
            
            if not template_file.exists():
                self.logger.warning(f"Template not found for deletion: {template_path}")
                return False
            
            # Move to trash/recycle bin instead of permanent deletion
            trash_dir = self.templates_dir / "trash"
            trash_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            trash_name = f"{template_file.stem}_{timestamp}{template_file.suffix}"
            trash_path = trash_dir / trash_name
            
            shutil.move(template_file, trash_path)
            
            self.logger.info(f"Moved template to trash: {template_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting template {template_path}: {e}")
            return False
    
    def restore_template(self, trash_name: str) -> bool:
        """
        Restore a template from trash.
        
        Args:
            trash_name (str): Name of the file in trash
            
        Returns:
            bool: True if restoration was successful
        """
        try:
            trash_dir = self.templates_dir / "trash"
            trash_path = trash_dir / trash_name
            
            if not trash_path.exists():
                self.logger.warning(f"Template not found in trash: {trash_name}")
                return False
            
            # Restore to templates directory
            original_name = trash_name.split('_')[:-1]  # Remove timestamp
            original_name = '_'.join(original_name) + Path(trash_name).suffix
            restore_path = self.templates_dir / original_name
            
            # Ensure unique filename
            counter = 1
            while restore_path.exists():
                stem = Path(original_name).stem
                suffix = Path(original_name).suffix
                original_name = f"{stem}_{counter}{suffix}"
                restore_path = self.templates_dir / original_name
                counter += 1
            
            shutil.move(trash_path, restore_path)
            
            self.logger.info(f"Restored template: {original_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error restoring template {trash_name}: {e}")
            return False
    
    def get_trash_templates(self) -> List[Dict[str, Any]]:
        """
        Get list of templates in trash.
        
        Returns:
            List[Dict[str, Any]]: List of trashed template information
        """
        trash_templates = []
        
        try:
            trash_dir = self.templates_dir / "trash"
            if not trash_dir.exists():
                return trash_templates
            
            for template_file in trash_dir.glob("*"):
                if template_file.is_file():
                    info = self.get_template_info(template_file)
                    if info:
                        trash_templates.append(info)
            
            trash_templates.sort(key=lambda x: x.get('modified', ''), reverse=True)
            
        except Exception as e:
            self.logger.error(f"Error getting trash templates: {e}")
        
        return trash_templates