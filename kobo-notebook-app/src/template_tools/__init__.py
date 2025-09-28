"""
Template creation and validation tools for Kobo Notebook App.

This module provides functionality to create, validate, and manage
notebook templates for Kobo Elipsa 2e devices.
"""

# Create the template_tools directory if it doesn't exist
import os
template_tools_dir = os.path.dirname(__file__)
if not os.path.exists(template_tools_dir):
    os.makedirs(template_tools_dir)