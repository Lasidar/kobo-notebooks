# Kobo Notebook App - Developer Guide

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Development Setup](#development-setup)
4. [Code Structure](#code-structure)
5. [API Reference](#api-reference)
6. [Testing](#testing)
7. [Contributing](#contributing)
8. [Troubleshooting](#troubleshooting)

## Project Overview

The Kobo Notebook App is a desktop application that allows users to create and install custom notebook templates on Kobo Elipsa 2e devices. The application provides a user-friendly interface for template generation, management, and installation.

### Key Features
- **Template Generation**: Create various notebook templates (lined, grid, dot grid, Cornell notes, etc.)
- **Device Management**: Detect and manage Kobo Elipsa 2e devices
- **Installation System**: Create KoboRoot.tgz packages for template installation
- **Template Library**: Organize and manage custom templates
- **Advanced Features**: Batch operations, scheduling, and diagnostics

### Target Device
- **Model**: Kobo Elipsa 2e
- **Display**: 10.3" E Ink Carta 1200
- **Resolution**: 1404 x 1872 pixels
- **Storage**: 32GB

## Architecture

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Desktop App   │    │  Template Tools │    │  Installation   │
│   (GUI Layer)   │◄──►│   (Core Logic)  │◄──►│    (Package)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Device Manager │    │ Template Manager│    │ Kobo Installer  │
│   & Diagnostics │    │   & Generator   │    │ & Advanced      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Core Components

#### 1. Desktop Application (`desktop_app/`)
- **Main Window**: Primary GUI interface with tabbed layout
- **Template Preview**: Preview generated templates
- **Device Interface**: Device detection and management UI

#### 2. Template Tools (`template_tools/`)
- **Template Generator**: Creates basic notebook templates
- **Advanced Generator**: Creates specialized templates
- **Template Manager**: Manages template library and metadata

#### 3. Installation System (`installation/`)
- **Kobo Installer**: Creates KoboRoot.tgz packages
- **Advanced Installer**: Handles batch operations and scheduling

#### 4. Utilities (`utils/`)
- **Device Manager**: Device detection and management
- **Device Diagnostics**: Health monitoring and analysis
- **Logger**: Centralized logging system
- **Device Tester**: Comprehensive testing framework
- **User Testing**: User experience testing tools

## Development Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/kobo-notebook-app.git
   cd kobo-notebook-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

### Development Environment

#### Recommended IDE Setup
- **VS Code**: Install Python extension and recommended extensions
- **PyCharm**: Professional or Community edition
- **Vim/Neovim**: With Python plugins

#### Code Formatting
The project uses Black for code formatting:
```bash
black src/ tests/
```

#### Linting
The project uses flake8 for linting:
```bash
flake8 src/ tests/
```

#### Type Checking
The project uses mypy for type checking:
```bash
mypy src/
```

## Code Structure

### Directory Layout
```
kobo-notebook-app/
├── src/                          # Source code
│   ├── desktop_app/             # GUI application
│   │   ├── gui/                 # GUI components
│   │   │   ├── main_window.py   # Main application window
│   │   │   ├── template_preview.py  # Template preview dialog
│   │   │   └── mock_tkinter.py  # Mock GUI for testing
│   │   └── main.py              # Application entry point
│   ├── template_tools/          # Template generation and management
│   │   ├── template_generator.py        # Basic template generation
│   │   ├── advanced_template_generator.py  # Advanced templates
│   │   ├── template_manager.py          # Template library management
│   │   └── create_sample_templates.py   # Sample template creation
│   ├── installation/            # Installation system
│   │   ├── kobo_installer.py    # Basic installer
│   │   └── advanced_installer.py # Advanced installer with scheduling
│   └── utils/                   # Utility modules
│       ├── device_manager.py    # Device detection and management
│       ├── device_diagnostics.py # Device health monitoring
│       ├── device_tester.py     # Device testing framework
│       ├── user_testing.py      # User testing framework
│       └── logger.py            # Logging system
├── tests/                       # Test suite
│   ├── test_utils.py           # Utility tests
│   ├── test_template_tools.py  # Template tool tests
│   ├── test_installation.py    # Installation tests
│   ├── test_desktop_app.py     # Desktop app tests
│   ├── test_api.py             # API integration tests
│   └── run_tests.py            # Test runner
├── templates/                   # Sample templates
├── docs/                        # Documentation
├── dist/                        # Distribution files
└── logs/                        # Application logs
```

### Key Design Patterns

#### 1. Factory Pattern
Used in template generation to create different types of templates:
```python
class TemplateGenerator:
    def generate_lined_template(self, **kwargs):
        # Implementation
    def generate_grid_template(self, **kwargs):
        # Implementation
```

#### 2. Observer Pattern
Used in the advanced installer for progress callbacks:
```python
class AdvancedInstaller:
    def create_installation_job(self, on_progress=None, on_complete=None):
        # Implementation with callbacks
```

#### 3. Strategy Pattern
Used in template validation for different validation strategies:
```python
class TemplateValidator:
    def validate_template(self, template, strategy="basic"):
        # Implementation
```

## API Reference

### Template Generator API

#### `TemplateGenerator`
Main class for generating notebook templates.

```python
from template_tools.template_generator import TemplateGenerator

generator = TemplateGenerator()

# Generate a lined template
template = generator.generate_lined_template(
    line_spacing=7,
    margin_top=50,
    margin_bottom=50,
    margin_left=40,
    margin_right=40,
    line_color="#000000"
)

# Save template
generator.save_template(template, "my_template.png")

# Validate template
validation = generator.validate_template(template)
```

#### Methods
- `generate_lined_template(**kwargs)` - Generate lined notebook template
- `generate_grid_template(**kwargs)` - Generate grid template
- `generate_dot_grid_template(**kwargs)` - Generate dot grid template
- `generate_cornell_template(**kwargs)` - Generate Cornell notes template
- `generate_blank_template(**kwargs)` - Generate blank template
- `save_template(template, filepath, format="PNG")` - Save template to file
- `validate_template(template)` - Validate template format

### Device Manager API

#### `DeviceManager`
Manages Kobo device detection and operations.

```python
from utils.device_manager import DeviceManager

device_manager = DeviceManager()

# Detect connected devices
devices = device_manager.detect_devices()

# Check if device is connected
has_device = device_manager.has_connected_device()

# Create backup
device_manager.create_backup(Path("/backup/path"))

# Restore backup
device_manager.restore_backup(Path("/backup/path"))
```

#### Methods
- `detect_devices()` - Detect connected Kobo devices
- `has_connected_device()` - Check if device is connected
- `create_backup(backup_path)` - Create device backup
- `restore_backup(backup_path)` - Restore device from backup

### Installation API

#### `KoboInstaller`
Creates KoboRoot.tgz installation packages.

```python
from installation.kobo_installer import KoboInstaller

installer = KoboInstaller()

# Create installation package
package_path = installer.create_installation_package(
    templates=["template1.png", "template2.png"],
    output_path="/output/path",
    package_name="my_templates.tgz"
)

# Validate package
is_valid = installer.validate_package(package_path)
```

#### `AdvancedInstaller`
Advanced installation with job management and scheduling.

```python
from installation.advanced_installer import AdvancedInstaller

installer = AdvancedInstaller()

# Create installation job
job_id = installer.create_installation_job(
    name="My Installation",
    templates=["template1.png"],
    device_path="/mnt/kobo"
)

# Get job status
status = installer.get_job_status(job_id)

# List all jobs
jobs = installer.list_jobs()
```

## Testing

### Running Tests

#### Run All Tests
```bash
python tests/run_tests.py
```

#### Run Specific Test Modules
```bash
python -m unittest tests.test_template_tools
python -m unittest tests.test_installation
python -m unittest tests.test_desktop_app
```

#### Run Device Tests
```bash
python src/utils/device_tester.py
```

### Test Structure

#### Unit Tests
- **test_utils.py**: Tests for utility modules
- **test_template_tools.py**: Tests for template generation and management
- **test_installation.py**: Tests for installation system
- **test_desktop_app.py**: Tests for GUI components
- **test_api.py**: Integration tests and API contracts

#### Test Categories
1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test component interactions
3. **API Tests**: Test API contracts and interfaces
4. **Device Tests**: Test device-specific functionality
5. **User Tests**: Test user experience and workflows

### Mock System

The project includes comprehensive mock implementations for testing:

#### Mock Tkinter
```python
from desktop_app.gui.mock_tkinter import *
import desktop_app.gui.mock_tkinter as tk

# Use mock tkinter for testing
root = tk.Tk()
```

#### Mock PIL
```python
# PIL is automatically mocked when not available
from template_tools.template_generator import PIL_AVAILABLE

if not PIL_AVAILABLE:
    # Mock PIL classes are used automatically
```

### Writing Tests

#### Test Structure
```python
import unittest
from unittest.mock import patch, MagicMock

class TestMyModule(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_my_function(self):
        """Test my function."""
        result = my_function()
        self.assertEqual(result, expected_value)
```

#### Best Practices
1. **Isolation**: Each test should be independent
2. **Cleanup**: Always clean up test resources
3. **Mocking**: Use mocks for external dependencies
4. **Coverage**: Aim for high test coverage
5. **Documentation**: Document test purpose and expected behavior

## Contributing

### Contribution Guidelines

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```
3. **Make changes and add tests**
4. **Run tests to ensure everything works**
   ```bash
   python tests/run_tests.py
   ```
5. **Commit changes**
   ```bash
   git commit -m "Add my feature"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/my-feature
   ```
7. **Create a pull request**

### Code Style

#### Python Style Guide
- Follow PEP 8
- Use Black for formatting
- Use type hints where appropriate
- Write docstrings for all public methods

#### Naming Conventions
- **Classes**: PascalCase (e.g., `TemplateGenerator`)
- **Functions/Methods**: snake_case (e.g., `generate_template`)
- **Constants**: UPPER_CASE (e.g., `DEVICE_WIDTH`)
- **Variables**: snake_case (e.g., `template_path`)

### Pull Request Process

1. **Ensure tests pass**
2. **Update documentation if needed**
3. **Add changelog entry**
4. **Request review from maintainers**
5. **Address feedback**
6. **Merge after approval**

## Troubleshooting

### Common Issues

#### 1. Import Errors
**Problem**: Module not found errors
**Solution**: Ensure the `src/` directory is in Python path
```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
```

#### 2. PIL/Pillow Not Available
**Problem**: Image processing fails
**Solution**: Install Pillow or use mock implementation
```bash
pip install Pillow
```

#### 3. Tkinter Not Available
**Problem**: GUI components fail to load
**Solution**: Use mock tkinter for testing
```python
# Mock tkinter is automatically used when tkinter is not available
```

#### 4. Device Not Detected
**Problem**: Kobo device not found
**Solution**: Check device connection and permissions
```bash
# Check if device is mounted
ls /media/  # Linux
ls /Volumes/  # macOS
```

### Debug Mode

Enable debug logging:
```python
from utils.logger import setup_logger

logger = setup_logger(level=logging.DEBUG)
```

### Performance Issues

#### Memory Usage
- Use generators for large datasets
- Clear temporary files regularly
- Monitor memory usage in long-running operations

#### CPU Usage
- Use threading for I/O operations
- Implement progress callbacks for long operations
- Profile code to identify bottlenecks

### Getting Help

1. **Check the logs**: Look in `logs/` directory
2. **Run diagnostics**: Use device diagnostics tools
3. **Check issues**: Look at GitHub issues
4. **Ask community**: Post in discussions or forums

### Reporting Bugs

When reporting bugs, include:
1. **System information**: OS, Python version, device model
2. **Steps to reproduce**: Clear reproduction steps
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Log files**: Relevant log entries
6. **Screenshots**: If applicable

---

*This developer guide is maintained by the project team. Please keep it updated as the project evolves.*