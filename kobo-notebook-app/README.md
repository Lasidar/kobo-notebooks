# Kobo Elipsa 2e Custom Notebook Background Application

A desktop application that allows users to create and install custom notebook backgrounds as native templates on Kobo Elipsa 2e devices.

## ⚠️ Important Disclaimer

**WARNING**: This application modifies your Kobo device's firmware and file system. Use at your own risk. Modifications may:
- Void your device warranty
- Potentially damage your device if used incorrectly
- Require technical knowledge to troubleshoot issues

Always backup your device before making any modifications.

## Features

- 🎨 Create custom notebook templates with various grid patterns
- 📱 Install templates as native Kobo templates (not PDF overlays)
- 🔧 Template validation and format compliance checking
- 📦 Automated installation via KoboRoot.tgz packages
- 💾 Backup and restore functionality
- 🖥️ Cross-platform desktop application (Windows, macOS, Linux)

## Project Status

🚧 **Development Phase**: This project is currently in active development. The roadmap includes:

- ✅ Project structure setup
- 🔄 Desktop application framework
- ⏳ Template creation tools
- ⏳ Installation system development
- ⏳ Device testing and validation

## Installation

### Prerequisites

- Python 3.8 or higher
- Kobo Elipsa 2e device
- USB cable for device connection

### Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd kobo-notebook-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/desktop_app/main.py
```

## Usage

1. **Connect your Kobo Elipsa 2e** to your computer via USB
2. **Launch the application** and select your device
3. **Create or import templates** using the built-in tools
4. **Preview templates** before installation
5. **Install templates** using the automated installer
6. **Restart your Kobo device** to see the new templates

## Development

### Project Structure

```
kobo-notebook-app/
├── src/
│   ├── desktop_app/          # Main desktop application
│   ├── template_tools/       # Template creation and validation
│   ├── installation/         # KoboRoot.tgz creation and installation
│   └── utils/               # Utility functions
├── templates/               # Sample template library
├── docs/                   # Documentation
├── tests/                  # Test suite
└── dist/                   # Distribution packages
```

### Running Tests

```bash
pytest tests/
```

### Building Distribution Packages

```bash
python setup.py build
```

## Contributing

This project is in early development. Contributions are welcome, but please:

1. Read the roadmap document (`KOBO_NOTEBOOK_APP_PLAN.md`)
2. Understand the risks involved in device modification
3. Test thoroughly on secondary devices
4. Follow the established code structure

## License

[License to be determined]

## Support

- 📖 Check the documentation in the `docs/` folder
- 🐛 Report issues via GitHub Issues
- 💬 Join the Kobo developer community discussions

## Acknowledgments

- Kobo developer community for reverse engineering insights
- KoboPatch and KoboMods projects for inspiration
- Etsy template creators for understanding user needs

---

**Remember**: Always backup your device before making any modifications!