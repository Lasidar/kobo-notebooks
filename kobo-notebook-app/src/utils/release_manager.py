#!/usr/bin/env python3
"""
Release Management System for Kobo Notebook App

This module provides tools for preparing, building, and distributing
release packages for the application.
"""

import os
import json
import shutil
import subprocess
import zipfile
import tarfile
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.logger import setup_logger


class ReleaseManager:
    """Manages application releases and distribution."""
    
    def __init__(self, project_root: Path = None):
        self.logger = setup_logger()
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.version = self._get_version()
        self.release_dir = self.project_root / "dist" / f"release_{self.version}"
        self.release_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_version(self) -> str:
        """Get the current version from setup.py or version file."""
        try:
            # Try to get version from setup.py
            setup_py = self.project_root / "setup.py"
            if setup_py.exists():
                with open(setup_py, 'r') as f:
                    content = f.read()
                    for line in content.split('\n'):
                        if 'version=' in line:
                            version = line.split('=')[1].strip().strip('"\'')
                            return version
            
            # Fallback to version file
            version_file = self.project_root / "VERSION"
            if version_file.exists():
                return version_file.read_text().strip()
            
            # Default version
            return "1.0.0"
        except Exception as e:
            self.logger.error(f"Error getting version: {e}")
            return "1.0.0"
    
    def create_release_package(self, platform: str = "all") -> Dict[str, Any]:
        """Create a release package for the specified platform."""
        self.logger.info(f"Creating release package for platform: {platform}")
        
        release_info = {
            "version": self.version,
            "platform": platform,
            "created": datetime.now().isoformat(),
            "files": [],
            "checksums": {}
        }
        
        try:
            if platform == "all" or platform == "source":
                self._create_source_package(release_info)
            
            if platform == "all" or platform == "windows":
                self._create_windows_package(release_info)
            
            if platform == "all" or platform == "linux":
                self._create_linux_package(release_info)
            
            if platform == "all" or platform == "macos":
                self._create_macos_package(release_info)
            
            # Save release info
            release_info_file = self.release_dir / "release_info.json"
            with open(release_info_file, 'w') as f:
                json.dump(release_info, f, indent=2)
            
            self.logger.info(f"Release package created successfully: {self.release_dir}")
            return release_info
            
        except Exception as e:
            self.logger.error(f"Error creating release package: {e}")
            raise
    
    def _create_source_package(self, release_info: Dict[str, Any]) -> None:
        """Create source code package."""
        self.logger.info("Creating source package...")
        
        source_dir = self.release_dir / "source"
        source_dir.mkdir(exist_ok=True)
        
        # Files to include in source package
        include_files = [
            "src/",
            "tests/",
            "docs/",
            "templates/",
            "requirements.txt",
            "setup.py",
            "README.md",
            "LICENSE",
            "CHANGELOG.md"
        ]
        
        # Files to exclude
        exclude_patterns = [
            "__pycache__/",
            "*.pyc",
            "*.pyo",
            ".git/",
            ".gitignore",
            "logs/",
            "dist/",
            "*.egg-info/",
            ".pytest_cache/",
            "venv/",
            "env/"
        ]
        
        # Copy files
        for file_path in include_files:
            src_path = self.project_root / file_path
            dst_path = source_dir / file_path
            
            if src_path.is_file():
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dst_path)
            elif src_path.is_dir():
                shutil.copytree(src_path, dst_path, ignore=shutil.ignore_patterns(*exclude_patterns))
        
        # Create source archive
        archive_name = f"kobo-notebook-app-{self.version}-source.tar.gz"
        archive_path = self.release_dir / archive_name
        
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(source_dir, arcname=f"kobo-notebook-app-{self.version}")
        
        # Calculate checksum
        checksum = self._calculate_checksum(archive_path)
        
        release_info["files"].append({
            "name": archive_name,
            "type": "source",
            "path": str(archive_path),
            "size": archive_path.stat().st_size,
            "checksum": checksum
        })
        release_info["checksums"][archive_name] = checksum
        
        # Clean up temporary directory
        shutil.rmtree(source_dir)
        
        self.logger.info(f"Source package created: {archive_name}")
    
    def _create_windows_package(self, release_info: Dict[str, Any]) -> None:
        """Create Windows executable package."""
        self.logger.info("Creating Windows package...")
        
        # Create Windows-specific files
        windows_dir = self.release_dir / "windows"
        windows_dir.mkdir(exist_ok=True)
        
        # Create batch file for installation
        install_bat = windows_dir / "install.bat"
        install_bat.write_text("""
@echo off
echo Installing Kobo Notebook App...
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create desktop shortcut
echo Creating desktop shortcut...
python -c "
import os
from pathlib import Path
import winshell
from win32com.client import Dispatch

desktop = winshell.desktop()
shortcut_path = os.path.join(desktop, 'Kobo Notebook App.lnk')
target = os.path.join(os.getcwd(), 'src', 'desktop_app', 'main.py')

shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(shortcut_path)
shortcut.Targetpath = 'python'
shortcut.Arguments = target
shortcut.WorkingDirectory = os.getcwd()
shortcut.IconLocation = target
shortcut.save()
"

echo Installation complete!
echo You can now run the application from the desktop shortcut.
pause
""")
        
        # Create uninstall script
        uninstall_bat = windows_dir / "uninstall.bat"
        uninstall_bat.write_text("""
@echo off
echo Uninstalling Kobo Notebook App...
echo.

REM Remove desktop shortcut
echo Removing desktop shortcut...
del "%USERPROFILE%\\Desktop\\Kobo Notebook App.lnk" 2>nul

REM Remove application files
echo Removing application files...
rd /s /q "%~dp0" 2>nul

echo Uninstallation complete!
pause
""")
        
        # Copy application files
        self._copy_application_files(windows_dir)
        
        # Create Windows archive
        archive_name = f"kobo-notebook-app-{self.version}-windows.zip"
        archive_path = self.release_dir / archive_name
        
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(windows_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(windows_dir)
                    zipf.write(file_path, arcname)
        
        # Calculate checksum
        checksum = self._calculate_checksum(archive_path)
        
        release_info["files"].append({
            "name": archive_name,
            "type": "windows",
            "path": str(archive_path),
            "size": archive_path.stat().st_size,
            "checksum": checksum
        })
        release_info["checksums"][archive_name] = checksum
        
        # Clean up temporary directory
        shutil.rmtree(windows_dir)
        
        self.logger.info(f"Windows package created: {archive_name}")
    
    def _create_linux_package(self, release_info: Dict[str, Any]) -> None:
        """Create Linux package."""
        self.logger.info("Creating Linux package...")
        
        linux_dir = self.release_dir / "linux"
        linux_dir.mkdir(exist_ok=True)
        
        # Create desktop entry
        desktop_entry = linux_dir / "kobo-notebook-app.desktop"
        desktop_entry.write_text(f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Kobo Notebook App
Comment=Custom notebook template manager for Kobo Elipsa 2e
Exec=python3 {self.project_root}/src/desktop_app/main.py
Icon=kobo-notebook-app
Terminal=false
Categories=Office;Graphics;
""")
        
        # Create installation script
        install_sh = linux_dir / "install.sh"
        install_sh.write_text("""#!/bin/bash

echo "Installing Kobo Notebook App..."
echo

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Create desktop entry
echo "Creating desktop entry..."
desktop_dir="$HOME/.local/share/applications"
mkdir -p "$desktop_dir"
cp kobo-notebook-app.desktop "$desktop_dir/"

# Make desktop entry executable
chmod +x "$desktop_dir/kobo-notebook-app.desktop"

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$desktop_dir"
fi

echo "Installation complete!"
echo "You can find the application in your applications menu."
""")
        
        # Create uninstall script
        uninstall_sh = linux_dir / "uninstall.sh"
        uninstall_sh.write_text("""#!/bin/bash

echo "Uninstalling Kobo Notebook App..."
echo

# Remove desktop entry
desktop_dir="$HOME/.local/share/applications"
rm -f "$desktop_dir/kobo-notebook-app.desktop"

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$desktop_dir"
fi

# Remove application files
echo "Removing application files..."
rm -rf "$(dirname "$0")"

echo "Uninstallation complete!"
""")
        
        # Make scripts executable
        install_sh.chmod(0o755)
        uninstall_sh.chmod(0o755)
        
        # Copy application files
        self._copy_application_files(linux_dir)
        
        # Create Linux archive
        archive_name = f"kobo-notebook-app-{self.version}-linux.tar.gz"
        archive_path = self.release_dir / archive_name
        
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(linux_dir, arcname=f"kobo-notebook-app-{self.version}")
        
        # Calculate checksum
        checksum = self._calculate_checksum(archive_path)
        
        release_info["files"].append({
            "name": archive_name,
            "type": "linux",
            "path": str(archive_path),
            "size": archive_path.stat().st_size,
            "checksum": checksum
        })
        release_info["checksums"][archive_name] = checksum
        
        # Clean up temporary directory
        shutil.rmtree(linux_dir)
        
        self.logger.info(f"Linux package created: {archive_name}")
    
    def _create_macos_package(self, release_info: Dict[str, Any]) -> None:
        """Create macOS package."""
        self.logger.info("Creating macOS package...")
        
        macos_dir = self.release_dir / "macos"
        macos_dir.mkdir(exist_ok=True)
        
        # Create macOS-specific files
        install_sh = macos_dir / "install.sh"
        install_sh.write_text("""#!/bin/bash

echo "Installing Kobo Notebook App..."
echo

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Create Applications directory entry
echo "Creating application entry..."
app_dir="$HOME/Applications/Kobo Notebook App"
mkdir -p "$app_dir"

# Copy application files
cp -r . "$app_dir/"

# Create launcher script
launcher="$app_dir/launch.sh"
cat > "$launcher" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 src/desktop_app/main.py
EOF

chmod +x "$launcher"

# Create Applications directory entry
app_entry="$app_dir/Kobo Notebook App.app"
mkdir -p "$app_entry/Contents/MacOS"
mkdir -p "$app_entry/Contents/Resources"

# Create Info.plist
cat > "$app_entry/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>launch.sh</string>
    <key>CFBundleIdentifier</key>
    <string>com.kobo-notebook-app</string>
    <key>CFBundleName</key>
    <string>Kobo Notebook App</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
</dict>
</plist>
EOF

# Create symbolic link to launcher
ln -sf "../launch.sh" "$app_entry/Contents/MacOS/launch.sh"

echo "Installation complete!"
echo "You can find the application in your Applications folder."
""")
        
        # Make script executable
        install_sh.chmod(0o755)
        
        # Copy application files
        self._copy_application_files(macos_dir)
        
        # Create macOS archive
        archive_name = f"kobo-notebook-app-{self.version}-macos.tar.gz"
        archive_path = self.release_dir / archive_name
        
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(macos_dir, arcname=f"kobo-notebook-app-{self.version}")
        
        # Calculate checksum
        checksum = self._calculate_checksum(archive_path)
        
        release_info["files"].append({
            "name": archive_name,
            "type": "macos",
            "path": str(archive_path),
            "size": archive_path.stat().st_size,
            "checksum": checksum
        })
        release_info["checksums"][archive_name] = checksum
        
        # Clean up temporary directory
        shutil.rmtree(macos_dir)
        
        self.logger.info(f"macOS package created: {archive_name}")
    
    def _copy_application_files(self, target_dir: Path) -> None:
        """Copy application files to target directory."""
        # Copy source code
        src_dir = target_dir / "src"
        shutil.copytree(self.project_root / "src", src_dir)
        
        # Copy templates
        templates_dir = target_dir / "templates"
        if (self.project_root / "templates").exists():
            shutil.copytree(self.project_root / "templates", templates_dir)
        
        # Copy documentation
        docs_dir = target_dir / "docs"
        shutil.copytree(self.project_root / "docs", docs_dir)
        
        # Copy configuration files
        config_files = [
            "requirements.txt",
            "setup.py",
            "README.md",
            "LICENSE",
            "CHANGELOG.md"
        ]
        
        for config_file in config_files:
            src_file = self.project_root / config_file
            if src_file.exists():
                shutil.copy2(src_file, target_dir / config_file)
    
    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA-256 checksum of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def create_checksums_file(self, release_info: Dict[str, Any]) -> Path:
        """Create a checksums file for all release files."""
        checksums_file = self.release_dir / "checksums.txt"
        
        with open(checksums_file, 'w') as f:
            f.write(f"Kobo Notebook App {self.version} - File Checksums\n")
            f.write("=" * 50 + "\n\n")
            
            for filename, checksum in release_info.get('checksums', {}).items():
                f.write(f"{checksum}  {filename}\n")
        
        self.logger.info(f"Checksums file created: {checksums_file}")
        return checksums_file
    
    def create_release_notes(self, changes: List[str] = None) -> Path:
        """Create release notes for the current version."""
        release_notes_file = self.release_dir / "RELEASE_NOTES.md"
        
        notes_content = f"""# Kobo Notebook App {self.version} - Release Notes

## Release Date
{datetime.now().strftime('%Y-%m-%d')}

## What's New

"""
        
        if changes:
            for change in changes:
                notes_content += f"- {change}\n"
        else:
            notes_content += """- Initial release of Kobo Notebook App
- Support for Kobo Elipsa 2e device
- Template generation and management
- Installation package creation
- Device diagnostics and health monitoring
- Cross-platform desktop application
- Comprehensive testing framework
"""
        
        notes_content += f"""

## System Requirements

- Python 3.8 or higher
- Kobo Elipsa 2e device (for template installation)
- USB connection for device communication

## Installation

1. Download the appropriate package for your platform
2. Extract the archive
3. Run the installation script
4. Launch the application

## Documentation

- User Guide: `docs/USER_GUIDE.md`
- Developer Guide: `docs/DEVELOPER_GUIDE.md`
- Troubleshooting: `docs/TROUBLESHOOTING.md`

## Support

For support and bug reports, please visit:
https://github.com/yourusername/kobo-notebook-app/issues

## License

This software is licensed under the MIT License.
See LICENSE file for details.
"""
        
        with open(release_notes_file, 'w') as f:
            f.write(notes_content)
        
        self.logger.info(f"Release notes created: {release_notes_file}")
        return release_notes_file
    
    def validate_release(self) -> Dict[str, Any]:
        """Validate the release package."""
        self.logger.info("Validating release package...")
        
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "files_checked": 0,
            "files_valid": 0
        }
        
        try:
            # Check if release directory exists
            if not self.release_dir.exists():
                validation_result["valid"] = False
                validation_result["errors"].append("Release directory does not exist")
                return validation_result
            
            # Check release info file
            release_info_file = self.release_dir / "release_info.json"
            if not release_info_file.exists():
                validation_result["valid"] = False
                validation_result["errors"].append("Release info file not found")
                return validation_result
            
            # Load release info
            with open(release_info_file, 'r') as f:
                release_info = json.load(f)
            
            # Validate each file
            for file_info in release_info.get("files", []):
                validation_result["files_checked"] += 1
                file_path = Path(file_info["path"])
                
                if file_path.exists():
                    # Check file size
                    actual_size = file_path.stat().st_size
                    expected_size = file_info["size"]
                    
                    if actual_size != expected_size:
                        validation_result["warnings"].append(
                            f"File size mismatch for {file_info['name']}: "
                            f"expected {expected_size}, got {actual_size}"
                        )
                    
                    # Verify checksum
                    actual_checksum = self._calculate_checksum(file_path)
                    expected_checksum = file_info["checksum"]
                    
                    if actual_checksum != expected_checksum:
                        validation_result["valid"] = False
                        validation_result["errors"].append(
                            f"Checksum mismatch for {file_info['name']}"
                        )
                    else:
                        validation_result["files_valid"] += 1
                else:
                    validation_result["valid"] = False
                    validation_result["errors"].append(
                        f"File not found: {file_info['name']}"
                    )
            
            # Check for required files
            required_files = ["checksums.txt", "RELEASE_NOTES.md"]
            for required_file in required_files:
                if not (self.release_dir / required_file).exists():
                    validation_result["warnings"].append(f"Required file missing: {required_file}")
            
        except Exception as e:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Validation error: {e}")
        
        self.logger.info(f"Release validation completed: {'PASS' if validation_result['valid'] else 'FAIL'}")
        return validation_result
    
    def upload_release(self, upload_config: Dict[str, Any]) -> bool:
        """Upload release to distribution platforms."""
        self.logger.info("Uploading release...")
        
        try:
            # GitHub Releases
            if upload_config.get("github", {}).get("enabled", False):
                self._upload_to_github(upload_config["github"])
            
            # PyPI
            if upload_config.get("pypi", {}).get("enabled", False):
                self._upload_to_pypi(upload_config["pypi"])
            
            # Custom server
            if upload_config.get("server", {}).get("enabled", False):
                self._upload_to_server(upload_config["server"])
            
            self.logger.info("Release upload completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Release upload failed: {e}")
            return False
    
    def _upload_to_github(self, config: Dict[str, Any]) -> None:
        """Upload release to GitHub."""
        # This would integrate with GitHub API
        self.logger.info("Uploading to GitHub Releases...")
        # Implementation would use GitHub API or gh CLI
    
    def _upload_to_pypi(self, config: Dict[str, Any]) -> None:
        """Upload package to PyPI."""
        # This would build and upload to PyPI
        self.logger.info("Uploading to PyPI...")
        # Implementation would use twine or similar
    
    def _upload_to_server(self, config: Dict[str, Any]) -> None:
        """Upload to custom server."""
        # This would upload to a custom server
        self.logger.info("Uploading to custom server...")
        # Implementation would use FTP, SCP, or similar


if __name__ == "__main__":
    # Example usage
    release_manager = ReleaseManager()
    
    # Create release package
    release_info = release_manager.create_release_package(platform="all")
    
    # Create additional files
    release_manager.create_checksums_file(release_info)
    release_manager.create_release_notes([
        "Added new template types",
        "Improved device detection",
        "Fixed installation issues",
        "Enhanced user interface"
    ])
    
    # Validate release
    validation_result = release_manager.validate_release()
    
    print(f"Release created: {release_info['version']}")
    print(f"Files created: {len(release_info['files'])}")
    print(f"Validation: {'PASS' if validation_result['valid'] else 'FAIL'}")
    
    if not validation_result['valid']:
        print("Errors:")
        for error in validation_result['errors']:
            print(f"  - {error}")