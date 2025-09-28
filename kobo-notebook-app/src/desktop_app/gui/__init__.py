"""
GUI components for the Kobo Notebook App desktop application.
"""

# Create the gui directory if it doesn't exist
import os
gui_dir = os.path.dirname(__file__)
if not os.path.exists(gui_dir):
    os.makedirs(gui_dir)