"""
Installation system for Kobo Notebook App.

This module provides functionality to create KoboRoot.tgz packages
and install custom templates on Kobo Elipsa 2e devices.
"""

# Create the installation directory if it doesn't exist
import os
installation_dir = os.path.dirname(__file__)
if not os.path.exists(installation_dir):
    os.makedirs(installation_dir)