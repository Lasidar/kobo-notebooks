"""
Utility modules for the Kobo Notebook App.
"""

# Create the utils directory if it doesn't exist
import os
utils_dir = os.path.dirname(__file__)
if not os.path.exists(utils_dir):
    os.makedirs(utils_dir)