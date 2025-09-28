#!/usr/bin/env python3
"""
Main entry point for the Kobo Notebook App desktop application.

This module provides the main GUI application for creating and installing
custom notebook templates on Kobo Elipsa 2e devices.
"""

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    TKINTER_AVAILABLE = True
except ImportError:
    # Use mock tkinter for testing
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'gui'))
    from mock_tkinter import *
    import mock_tkinter as tk
    TKINTER_AVAILABLE = False
import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from desktop_app.gui.main_window import MainWindow
from utils.device_manager import DeviceManager
from utils.logger import setup_logger


def main():
    """Main entry point for the desktop application."""
    try:
        # Setup logging
        logger = setup_logger()
        logger.info("Starting Kobo Notebook App")
        
        # Create the main application window
        root = tk.Tk()
        
        # Initialize the main window
        app = MainWindow(root)
        
        # Start the GUI event loop
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Fatal error starting application: {e}")
        messagebox.showerror("Error", f"Failed to start application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()