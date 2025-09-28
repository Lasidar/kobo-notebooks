#!/usr/bin/env python3
"""
Setup script for Kobo Notebook App
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="kobo-notebook-app",
    version="0.1.0",
    author="Kobo Notebook App Team",
    author_email="",
    description="Custom notebook background application for Kobo Elipsa 2e",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/kobo-notebook-app",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "kobo-notebook=kobo_notebook_app.main:main",
        ],
        "gui_scripts": [
            "kobo-notebook-gui=kobo_notebook_app.desktop_app.main:main",
        ],
    },
    package_data={
        "kobo_notebook_app": [
            "templates/*.png",
            "templates/*.jpg",
            "docs/*.md",
            "*.md",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)