# User Guide

## Overview

The Kobo Notebook App allows you to create and install custom notebook templates on your Kobo Elipsa 2e device. These templates become native options in your device's notebook application, providing a seamless writing experience.

## Getting Started

### Launching the Application

1. Start the application by running:
   ```bash
   python src/desktop_app/main.py
   ```

2. The main window will open with four tabs:
   - **Device**: Manage your connected Kobo device
   - **Create Template**: Design custom notebook templates
   - **Template Library**: Browse and manage your templates
   - **Settings**: Configure application preferences

## Device Management

### Connecting Your Device

1. Connect your Kobo Elipsa 2e to your computer via USB
2. On your Kobo device, select "Connect to Computer" when prompted
3. In the application, click "Refresh" in the Device tab
4. Your device information should appear

### Device Information

The Device tab displays:
- **Status**: Connection status and device model
- **Firmware**: Current firmware version
- **Storage**: Available storage space
- **Templates**: Number of installed templates

### Creating Backups

**Always create a backup before making any changes to your device.**

1. Click "Create Backup" in the Device tab
2. Choose a location to save your backup
3. Wait for the backup process to complete
4. The backup includes your device's configuration and templates

### Restoring Backups

If you need to restore a backup:

1. Click "Restore Backup" in the Device tab
2. Select your backup file
3. Confirm the restoration process
4. Your device will be restored to the backup state

## Creating Templates

### Template Types

The application supports several template types:

#### Lined Templates
- **Use Case**: General writing, note-taking
- **Parameters**: Line spacing (5mm, 7mm, 10mm)
- **Features**: Consistent line spacing, margins

#### Grid Templates
- **Use Case**: Technical drawings, diagrams, structured notes
- **Parameters**: Grid size (5mm, 10mm)
- **Features**: Square grid pattern

#### Dot Grid Templates
- **Use Case**: Bullet journaling, flexible layouts
- **Parameters**: Dot spacing (5mm, 7mm)
- **Features**: Subtle dot pattern, versatile layout

#### Cornell Note Templates
- **Use Case**: Academic note-taking, study notes
- **Features**: Notes section, cues section, summary section
- **Benefits**: Structured note-taking format

#### Blank Templates
- **Use Case**: Free-form drawing, custom layouts
- **Features**: Clean white background

### Creating a Template

1. Go to the "Create Template" tab
2. Select your desired template type from the dropdown
3. Adjust the parameters:
   - **Line Spacing**: For lined templates (5-20 pixels)
   - **Grid Size**: For grid templates (3-20 pixels)
4. Click "Preview Template" to see how it looks
5. Click "Create Template" to generate and save the template

### Importing Templates

You can import existing templates:

1. Click "Import Template" in the Create Template tab
2. Select an image file (PNG, JPG, JPEG)
3. The template will be processed and added to your library
4. Ensure imported templates are 1404x1872 pixels for best results

## Template Library

### Managing Templates

The Template Library tab shows all your available templates:

- **Name**: Template filename
- **Type**: Template category
- **Size**: File size
- **Created**: Creation date

### Installing Templates

1. Select a template from the library
2. Click "Install Selected"
3. Confirm the installation
4. The template will be packaged and installed on your device
5. Restart your Kobo device to see the new template

### Exporting Templates

To share templates with others:

1. Select a template from the library
2. Click "Export Template"
3. Choose a location to save the file
4. The template will be exported as a PNG file

### Deleting Templates

To remove templates from your library:

1. Select a template from the library
2. Click "Delete Template"
3. Confirm the deletion
4. The template will be removed from your library

## Settings

### General Settings

- **Auto-detect devices**: Automatically detect connected Kobo devices
- **Backup Directory**: Location where backups are stored
- **Template Directory**: Location where templates are stored

### Application Information

The Settings tab also displays:
- Application version
- Important disclaimers and warnings
- Support information

## Best Practices

### Template Design

- **Keep it simple**: Complex designs may not display well on e-ink
- **Use high contrast**: Ensure text and lines are clearly visible
- **Test on device**: Always test templates on your actual device
- **Consider margins**: Leave adequate margins for comfortable writing

### Device Management

- **Regular backups**: Create backups before making changes
- **Test first**: Try new templates on a small scale first
- **Keep originals**: Save original template files
- **Monitor storage**: Keep track of available device storage

### Safety

- **Read warnings**: Always read and understand the safety warnings
- **Backup first**: Never skip the backup step
- **One change at a time**: Make incremental changes to identify issues
- **Keep logs**: Save installation logs for troubleshooting

## Troubleshooting

### Common Issues

#### Templates Not Appearing on Device
1. Restart your Kobo device
2. Check that templates were properly installed
3. Verify template format and size
4. Check device storage space

#### Installation Fails
1. Ensure device is properly connected
2. Check device storage space
3. Verify template format
4. Try creating a new template

#### Device Not Detected
1. Check USB connection
2. Enable file transfer mode on device
3. Try a different USB port
4. Restart the application

### Getting Help

If you encounter issues:

1. **Check Logs**: Review application logs for error details
2. **Documentation**: Check the troubleshooting guides
3. **Community**: Visit the project repository for community support
4. **Report Issues**: Create an issue with detailed information

## Advanced Usage

### Custom Template Formats

For advanced users, you can create templates with specific requirements:

- **Resolution**: 1404x1872 pixels (Kobo Elipsa 2e native resolution)
- **Format**: PNG format recommended
- **Color**: Black and white for best e-ink display
- **DPI**: 300 DPI for crisp lines

### Batch Operations

You can process multiple templates at once by:
1. Creating templates in bulk using the template generator
2. Installing multiple templates in a single package
3. Managing template libraries with external tools

## Legal and Safety Information

### Important Disclaimers

- **Warranty**: Modifying your device may void the warranty
- **Risk**: There is always a risk of damaging your device
- **Backup**: Always maintain current backups
- **Support**: No official support from Kobo for modified devices

### Terms of Use

By using this application, you agree to:
- Use the software at your own risk
- Accept responsibility for any device damage
- Not hold the developers liable for issues
- Understand the limitations and risks

## Support and Updates

### Getting Updates

Check the project repository regularly for:
- New template types
- Bug fixes
- Security updates
- Feature enhancements

### Contributing

The project welcomes contributions:
- Bug reports
- Feature requests
- Template submissions
- Documentation improvements
- Code contributions

### Community

Join the community for:
- Template sharing
- Usage tips
- Troubleshooting help
- Feature discussions