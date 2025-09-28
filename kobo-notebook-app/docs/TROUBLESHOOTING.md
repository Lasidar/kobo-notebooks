# Kobo Notebook App - Troubleshooting Guide

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [Device Connection Problems](#device-connection-problems)
3. [Template Generation Issues](#template-generation-issues)
4. [Installation Package Problems](#installation-package-problems)
5. [GUI Issues](#gui-issues)
6. [Performance Problems](#performance-problems)
7. [Device-Specific Issues](#device-specific-issues)
8. [Error Codes](#error-codes)
9. [Advanced Troubleshooting](#advanced-troubleshooting)
10. [Getting Help](#getting-help)

## Installation Issues

### Problem: Application Won't Start

#### Symptoms
- Application crashes on startup
- "Module not found" errors
- GUI doesn't appear

#### Solutions

**1. Check Python Version**
```bash
python --version
```
Ensure you have Python 3.8 or higher.

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

**3. Check Virtual Environment**
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

**4. Check File Permissions**
```bash
# Make sure the application has execute permissions
chmod +x src/desktop_app/main.py
```

**5. Check Log Files**
Look in the `logs/` directory for error messages:
```bash
tail -f logs/app.log
```

### Problem: Dependencies Missing

#### Symptoms
- "No module named 'PIL'" errors
- Import errors for tkinter

#### Solutions

**1. Install Pillow**
```bash
pip install Pillow
```

**2. Install tkinter (Linux)**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install tkinter
```

**3. Use Mock Implementations**
The application includes mock implementations for testing. If you encounter import errors, the mocks will be used automatically.

## Device Connection Problems

### Problem: Device Not Detected

#### Symptoms
- "No devices found" message
- Device doesn't appear in the device list
- Connection timeout errors

#### Solutions

**1. Check USB Connection**
- Ensure USB cable is properly connected
- Try a different USB port
- Try a different USB cable

**2. Check Device Mounting**
```bash
# Linux
ls /media/
ls /mnt/

# macOS
ls /Volumes/

# Windows
# Check in File Explorer for Kobo device
```

**3. Enable File Transfer Mode**
On your Kobo device:
1. Go to Settings
2. Select "Device information"
3. Enable "USB connection"
4. Select "Connect to computer"

**4. Check Device Permissions**
```bash
# Linux - check if device is accessible
ls -la /media/kobo/
```

**5. Restart Device**
1. Power off the Kobo device
2. Wait 10 seconds
3. Power on and reconnect

### Problem: Permission Denied

#### Symptoms
- "Permission denied" errors
- Cannot access device files
- Backup/restore fails

#### Solutions

**1. Check File Permissions**
```bash
# Linux - check device permissions
ls -la /media/kobo/
```

**2. Run with Appropriate Permissions**
```bash
# Linux - run with sudo (not recommended for production)
sudo python src/desktop_app/main.py
```

**3. Add User to Groups**
```bash
# Linux - add user to plugdev group
sudo usermod -a -G plugdev $USER
```

**4. Check Device Ownership**
```bash
# Linux - change ownership if needed
sudo chown -R $USER:$USER /media/kobo/
```

## Template Generation Issues

### Problem: Templates Not Generated

#### Symptoms
- Template generation fails
- Empty or corrupted template files
- "PIL not available" warnings

#### Solutions

**1. Install Pillow**
```bash
pip install Pillow
```

**2. Check Available Memory**
```bash
# Check system memory
free -h  # Linux
vm_stat  # macOS
```

**3. Check Disk Space**
```bash
df -h
```

**4. Verify Template Parameters**
Ensure template parameters are within valid ranges:
- Line spacing: 1-50 pixels
- Margins: 0-200 pixels
- Colors: Valid hex codes

### Problem: Template Validation Fails

#### Symptoms
- Templates marked as invalid
- Validation errors in logs
- Templates don't work on device

#### Solutions

**1. Check Template Dimensions**
Templates must be exactly 1404 x 1872 pixels for Kobo Elipsa 2e.

**2. Check Image Format**
Templates should be in PNG format for best compatibility.

**3. Check Color Mode**
Use RGB or grayscale mode for templates.

**4. Verify File Integrity**
```bash
# Check if template file is valid
file my_template.png
```

## Installation Package Problems

### Problem: Package Creation Fails

#### Symptoms
- "Failed to create package" errors
- Corrupted .tgz files
- Package validation fails

#### Solutions

**1. Check Template Files**
Ensure all template files exist and are valid:
```bash
ls -la templates/
```

**2. Check Disk Space**
Ensure sufficient disk space for package creation:
```bash
df -h
```

**3. Check File Permissions**
Ensure write permissions for output directory:
```bash
chmod 755 /path/to/output/directory
```

**4. Validate Templates**
Run template validation before package creation:
```python
from template_tools.template_generator import TemplateGenerator

generator = TemplateGenerator()
validation = generator.validate_template(template)
if not validation['valid']:
    print("Template validation failed:", validation['errors'])
```

### Problem: Installation Fails

#### Symptoms
- Package installation fails
- Device doesn't recognize package
- Installation hangs

#### Solutions

**1. Check Package Format**
Ensure the package is a valid .tgz file:
```bash
file my_package.tgz
```

**2. Verify Package Contents**
```bash
tar -tzf my_package.tgz
```

**3. Check Device Storage**
Ensure device has sufficient storage:
```bash
# Check device storage
df -h /media/kobo/
```

**4. Restart Device**
After installation, restart the Kobo device to apply changes.

## GUI Issues

### Problem: GUI Won't Load

#### Symptoms
- Application starts but no GUI appears
- "tkinter not available" errors
- GUI components missing

#### Solutions

**1. Install tkinter**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install tkinter
```

**2. Check Display Environment**
```bash
# Linux - check if display is available
echo $DISPLAY
```

**3. Use Mock GUI**
The application includes mock GUI components for testing without tkinter.

**4. Run in Headless Mode**
For server environments, the application can run without GUI:
```python
# Use mock tkinter
from desktop_app.gui.mock_tkinter import *
```

### Problem: GUI Freezes

#### Symptoms
- Application becomes unresponsive
- GUI doesn't update
- Mouse/keyboard input ignored

#### Solutions

**1. Check System Resources**
```bash
# Check CPU and memory usage
top
htop
```

**2. Check for Long-Running Operations**
Look for operations that might be blocking the GUI thread.

**3. Restart Application**
Close and restart the application.

**4. Check Log Files**
Look for error messages in the logs.

## Performance Problems

### Problem: Slow Template Generation

#### Symptoms
- Template generation takes too long
- Application becomes unresponsive
- High CPU usage

#### Solutions

**1. Check System Resources**
```bash
# Monitor CPU and memory
top
```

**2. Reduce Template Complexity**
- Use simpler templates
- Reduce image resolution for testing
- Limit number of templates

**3. Use Threading**
Long operations should run in background threads to avoid blocking GUI.

**4. Optimize Image Processing**
- Use appropriate image formats
- Implement caching for repeated operations

### Problem: High Memory Usage

#### Symptoms
- Application uses excessive memory
- System becomes slow
- Out of memory errors

#### Solutions

**1. Monitor Memory Usage**
```bash
# Check memory usage
free -h
ps aux | grep python
```

**2. Implement Memory Management**
- Clear temporary files
- Use generators for large datasets
- Implement proper cleanup

**3. Limit Concurrent Operations**
- Process templates one at a time
- Implement queuing system

## Device-Specific Issues

### Problem: Templates Don't Appear on Device

#### Symptoms
- Installation succeeds but templates don't show up
- Device doesn't recognize new templates
- Templates appear but don't work

#### Solutions

**1. Check Device Firmware**
Ensure device firmware is compatible:
- Kobo Elipsa 2e firmware 4.30+
- Check for firmware updates

**2. Restart Device**
After installation, restart the device:
1. Power off device
2. Wait 10 seconds
3. Power on device

**3. Check Template Location**
Verify templates are installed in correct location:
```
.kobo/templates/
```

**4. Check File Permissions**
Ensure templates have correct permissions:
```bash
chmod 644 /media/kobo/.kobo/templates/*.png
```

### Problem: Device Becomes Unresponsive

#### Symptoms
- Device doesn't respond to input
- Screen doesn't update
- Device won't power on

#### Solutions

**1. Hard Reset**
1. Hold power button for 15 seconds
2. Release and wait 10 seconds
3. Press power button to restart

**2. Factory Reset**
⚠️ **WARNING**: This will erase all data on the device
1. Go to Settings > Device information
2. Select "Factory reset"
3. Confirm reset

**3. Restore from Backup**
If you have a backup:
1. Connect device to computer
2. Restore backup files
3. Restart device

## Error Codes

### Common Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| `DEVICE_NOT_FOUND` | No Kobo device detected | Check USB connection and device mounting |
| `PERMISSION_DENIED` | Insufficient permissions | Check file permissions and user groups |
| `TEMPLATE_INVALID` | Template validation failed | Check template format and dimensions |
| `PACKAGE_CORRUPT` | Installation package corrupted | Recreate package |
| `INSTALLATION_FAILED` | Package installation failed | Check device storage and restart device |
| `GUI_NOT_AVAILABLE` | GUI components not available | Install tkinter or use mock GUI |

### Error Logging

Check error logs for detailed information:
```bash
# View recent errors
tail -n 50 logs/app.log | grep ERROR

# Monitor logs in real-time
tail -f logs/app.log
```

## Advanced Troubleshooting

### Debug Mode

Enable debug mode for detailed logging:
```python
from utils.logger import setup_logger
import logging

logger = setup_logger(level=logging.DEBUG)
```

### Device Diagnostics

Run comprehensive device diagnostics:
```python
from utils.device_diagnostics import DeviceDiagnostics

diagnostics = DeviceDiagnostics()
health_report = diagnostics.run_full_diagnostics("/media/kobo")
print(health_report)
```

### System Information

Gather system information for troubleshooting:
```bash
# Python version
python --version

# Installed packages
pip list

# System information
uname -a  # Linux
system_profiler SPSoftwareDataType  # macOS
systeminfo  # Windows

# Device information
lsusb  # Linux
system_profiler SPUSBDataType  # macOS
```

### Network Troubleshooting

If downloading templates or updates fails:
```bash
# Test internet connection
ping google.com

# Check DNS resolution
nslookup github.com

# Test HTTPS connectivity
curl -I https://github.com
```

## Getting Help

### Self-Help Resources

1. **Check Documentation**
   - User Guide: `docs/USER_GUIDE.md`
   - Developer Guide: `docs/DEVELOPER_GUIDE.md`
   - Installation Guide: `docs/INSTALLATION.md`

2. **Run Diagnostics**
   ```bash
   python src/utils/device_diagnostics.py
   ```

3. **Check Logs**
   ```bash
   tail -f logs/app.log
   ```

### Community Support

1. **GitHub Issues**
   - Report bugs: Create an issue with detailed information
   - Request features: Use the feature request template
   - Ask questions: Use the Q&A label

2. **Community Forums**
   - Reddit: r/kobo
   - Kobo Community Forums
   - Discord: Kobo Developer Community

3. **Developer Support**
   - Email: developer@kobo-notebook-app.com
   - Discord: Direct message to developers

### Reporting Issues

When reporting issues, include:

1. **System Information**
   - Operating system and version
   - Python version
   - Device model and firmware version

2. **Error Details**
   - Complete error message
   - Steps to reproduce
   - Expected vs actual behavior

3. **Log Files**
   - Relevant log entries
   - Screenshots if applicable

4. **Environment**
   - Virtual environment details
   - Installed packages
   - Device connection status

### Emergency Recovery

If the device becomes completely unresponsive:

1. **Immediate Actions**
   - Disconnect from computer
   - Hold power button for 30 seconds
   - Wait 2 minutes before attempting restart

2. **Recovery Options**
   - Factory reset (⚠️ data loss)
   - Restore from backup
   - Contact Kobo support

3. **Prevention**
   - Always backup before modifications
   - Test on secondary device first
   - Keep firmware updated

---

*This troubleshooting guide is maintained by the project team. Please keep it updated as new issues are discovered and resolved.*