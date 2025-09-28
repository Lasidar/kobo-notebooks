# Installation Guide

## Prerequisites

Before installing the Kobo Notebook App, ensure you have the following:

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **Storage**: At least 100MB free disk space
- **USB Port**: For connecting your Kobo Elipsa 2e device

### Device Requirements
- **Device**: Kobo Elipsa 2e (10.3" E Ink Carta 1200)
- **Storage**: At least 1GB free space on device
- **Firmware**: Latest firmware version (recommended)

## Installation Steps

### 1. Download the Application

Download the latest release from the project repository or clone the source code:

```bash
git clone <repository-url>
cd kobo-notebook-app
```

### 2. Install Python Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Run the Application

Start the desktop application:

```bash
python src/desktop_app/main.py
```

Or use the console version:

```bash
python -m kobo_notebook_app.main
```

## First-Time Setup

### 1. Connect Your Device

1. Connect your Kobo Elipsa 2e to your computer via USB
2. Wait for the device to be recognized by your operating system
3. The application should automatically detect your device

### 2. Create a Backup

**IMPORTANT**: Always create a backup before making any modifications to your device.

1. In the application, go to the "Device" tab
2. Click "Create Backup"
3. Choose a location to save your backup
4. Wait for the backup to complete

### 3. Test Template Creation

1. Go to the "Create Template" tab
2. Select a template type (e.g., "Lined")
3. Adjust the parameters as needed
4. Click "Preview Template" to see how it looks
5. Click "Create Template" to generate the template

## Troubleshooting

### Device Not Detected

If your device is not automatically detected:

1. **Check USB Connection**: Ensure the USB cable is properly connected
2. **Enable File Transfer**: On your Kobo device, enable file transfer mode
3. **Check Mount Point**: Verify the device appears in your file manager
4. **Try Different USB Port**: Some USB ports may not work properly
5. **Restart Application**: Close and reopen the application

### Permission Errors

If you encounter permission errors:

1. **Linux/macOS**: Run with appropriate permissions or use `sudo`
2. **Windows**: Run as administrator
3. **Check Device Mount**: Ensure the device is not mounted as read-only

### Template Creation Fails

If template creation fails:

1. **Check Disk Space**: Ensure you have enough free space
2. **Check Permissions**: Verify write permissions in the templates directory
3. **Update Dependencies**: Ensure all Python packages are up to date
4. **Check Logs**: Review the application logs for detailed error messages

## Uninstallation

To remove the application:

1. **Remove Templates**: Use the application to uninstall any installed templates
2. **Delete Application Files**: Remove the application directory
3. **Clean Python Packages**: Uninstall Python dependencies if desired

```bash
pip uninstall kobo-notebook-app
```

## Support

If you encounter issues:

1. **Check Documentation**: Review the troubleshooting section
2. **Review Logs**: Check the application logs for error details
3. **Community Support**: Visit the project repository for community help
4. **Report Issues**: Create an issue on the project repository

## Safety Reminders

⚠️ **Important Safety Information**:

- Always backup your device before making modifications
- Test on a secondary device if possible
- Understand that modifications may void your warranty
- Keep your original firmware backup safe
- Do not interrupt the installation process

## Legal Notice

This application modifies your Kobo device's firmware. By using this software, you acknowledge that:

- You understand the risks involved
- You are responsible for any damage to your device
- The developers are not liable for any issues
- You may void your device warranty

Use this software at your own risk.