"""
Template generation utilities for creating custom notebook backgrounds.

This module provides functionality to generate various types of notebook
templates optimized for the Kobo Elipsa 2e device specifications.
"""

import os
import math
from typing import Tuple, Optional, Dict, Any
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    # Create dummy classes for testing
    class Image:
        @staticmethod
        def new(mode, size, color):
            return None
        
        @staticmethod
        def open(path):
            return None
        
        def save(self, path, format=None):
            pass
        
        def convert(self, mode):
            return self
        
        def resize(self, size, resample=None):
            return self
    
    class ImageDraw:
        @staticmethod
        def Draw(img):
            return ImageDraw()
        
        def __init__(self):
            pass
        
        def line(self, xy, fill=None, width=1):
            pass
        
        def rectangle(self, xy, outline=None, fill=None, width=1):
            pass
        
        def ellipse(self, xy, fill=None, outline=None):
            pass
        
        def text(self, xy, text, fill=None, font=None):
            pass
    
    class ImageFont:
        @staticmethod
        def load_default():
            return None

from utils.logger import setup_logger


class TemplateGenerator:
    """Generates notebook templates for Kobo Elipsa 2e."""
    
    # Kobo Elipsa 2e specifications
    DEVICE_WIDTH = 1404
    DEVICE_HEIGHT = 1872
    DPI = 300  # Assumed DPI for the device
    
    def __init__(self):
        """Initialize the template generator."""
        self.logger = setup_logger()
        
    def generate_lined_template(
        self, 
        line_spacing: int = 7, 
        margin_top: int = 50,
        margin_bottom: int = 50,
        margin_left: int = 40,
        margin_right: int = 40,
        line_color: str = "#000000"
    ) -> Any:
        """
        Generate a lined notebook template.
        
        Args:
            line_spacing (int): Spacing between lines in pixels
            margin_top (int): Top margin in pixels
            margin_bottom (int): Bottom margin in pixels
            margin_left (int): Left margin in pixels
            margin_right (int): Right margin in pixels
            line_color (str): Color of the lines (hex format)
            
        Returns:
            Any: Generated lined template
        """
        try:
            # Create a white background
            img = Image.new('RGB', (self.DEVICE_WIDTH, self.DEVICE_HEIGHT), 'white')
            draw = ImageDraw.Draw(img)
            
            # Calculate line positions
            start_y = margin_top
            end_y = self.DEVICE_HEIGHT - margin_bottom
            
            # Draw horizontal lines
            y = start_y
            while y <= end_y:
                draw.line(
                    [(margin_left, y), (self.DEVICE_WIDTH - margin_right, y)],
                    fill=line_color,
                    width=1
                )
                y += line_spacing
            
            self.logger.info(f"Generated lined template with {line_spacing}px spacing")
            return img
            
        except Exception as e:
            self.logger.error(f"Error generating lined template: {e}")
            raise
    
    def generate_grid_template(
        self,
        grid_size: int = 5,
        margin_top: int = 50,
        margin_bottom: int = 50,
        margin_left: int = 40,
        margin_right: int = 40,
        grid_color: str = "#000000"
    ) -> Any:
        """
        Generate a grid notebook template.
        
        Args:
            grid_size (int): Size of grid squares in pixels
            margin_top (int): Top margin in pixels
            margin_bottom (int): Bottom margin in pixels
            margin_left (int): Left margin in pixels
            margin_right (int): Right margin in pixels
            grid_color (str): Color of the grid lines (hex format)
            
        Returns:
            Any: Generated grid template
        """
        try:
            # Create a white background
            img = Image.new('RGB', (self.DEVICE_WIDTH, self.DEVICE_HEIGHT), 'white')
            draw = ImageDraw.Draw(img)
            
            # Calculate grid boundaries
            start_x = margin_left
            end_x = self.DEVICE_WIDTH - margin_right
            start_y = margin_top
            end_y = self.DEVICE_HEIGHT - margin_bottom
            
            # Draw vertical lines
            x = start_x
            while x <= end_x:
                draw.line(
                    [(x, start_y), (x, end_y)],
                    fill=grid_color,
                    width=1
                )
                x += grid_size
            
            # Draw horizontal lines
            y = start_y
            while y <= end_y:
                draw.line(
                    [(start_x, y), (end_x, y)],
                    fill=grid_color,
                    width=1
                )
                y += grid_size
            
            self.logger.info(f"Generated grid template with {grid_size}px squares")
            return img
            
        except Exception as e:
            self.logger.error(f"Error generating grid template: {e}")
            raise
    
    def generate_dot_grid_template(
        self,
        dot_spacing: int = 5,
        margin_top: int = 50,
        margin_bottom: int = 50,
        margin_left: int = 40,
        margin_right: int = 40,
        dot_color: str = "#000000",
        dot_size: int = 1
    ) -> Any:
        """
        Generate a dot grid notebook template.
        
        Args:
            dot_spacing (int): Spacing between dots in pixels
            margin_top (int): Top margin in pixels
            margin_bottom (int): Bottom margin in pixels
            margin_left (int): Left margin in pixels
            margin_right (int): Right margin in pixels
            dot_color (str): Color of the dots (hex format)
            dot_size (int): Size of the dots in pixels
            
        Returns:
            Any: Generated dot grid template
        """
        try:
            # Create a white background
            img = Image.new('RGB', (self.DEVICE_WIDTH, self.DEVICE_HEIGHT), 'white')
            draw = ImageDraw.Draw(img)
            
            # Calculate dot boundaries
            start_x = margin_left
            end_x = self.DEVICE_WIDTH - margin_right
            start_y = margin_top
            end_y = self.DEVICE_HEIGHT - margin_bottom
            
            # Draw dots
            y = start_y
            while y <= end_y:
                x = start_x
                while x <= end_x:
                    # Draw a small circle for the dot
                    draw.ellipse(
                        [x - dot_size, y - dot_size, x + dot_size, y + dot_size],
                        fill=dot_color
                    )
                    x += dot_spacing
                y += dot_spacing
            
            self.logger.info(f"Generated dot grid template with {dot_spacing}px spacing")
            return img
            
        except Exception as e:
            self.logger.error(f"Error generating dot grid template: {e}")
            raise
    
    def generate_cornell_template(
        self,
        line_spacing: int = 7,
        margin_top: int = 50,
        margin_bottom: int = 50,
        margin_left: int = 40,
        margin_right: int = 40,
        note_width_ratio: float = 0.7,
        cue_width_ratio: float = 0.2,
        summary_height_ratio: float = 0.25,
        line_color: str = "#000000"
    ) -> Any:
        """
        Generate a Cornell note-taking template.
        
        Args:
            line_spacing (int): Spacing between lines in pixels
            margin_top (int): Top margin in pixels
            margin_bottom (int): Bottom margin in pixels
            margin_left (int): Left margin in pixels
            margin_right (int): Right margin in pixels
            note_width_ratio (float): Ratio of width for notes section (0.0-1.0)
            cue_width_ratio (float): Ratio of width for cues section (0.0-1.0)
            summary_height_ratio (float): Ratio of height for summary section (0.0-1.0)
            line_color (str): Color of the lines (hex format)
            
        Returns:
            Any: Generated Cornell template
        """
        try:
            # Create a white background
            img = Image.new('RGB', (self.DEVICE_WIDTH, self.DEVICE_HEIGHT), 'white')
            draw = ImageDraw.Draw(img)
            
            # Calculate dimensions
            usable_width = self.DEVICE_WIDTH - margin_left - margin_right
            usable_height = self.DEVICE_HEIGHT - margin_top - margin_bottom
            
            # Calculate section boundaries
            notes_width = int(usable_width * note_width_ratio)
            cues_width = int(usable_width * cue_width_ratio)
            summary_height = int(usable_height * summary_height_ratio)
            notes_height = usable_height - summary_height
            
            # Draw main sections
            # Notes section
            notes_start_x = margin_left
            notes_end_x = notes_start_x + notes_width
            notes_start_y = margin_top
            notes_end_y = notes_start_y + notes_height
            
            # Cues section
            cues_start_x = notes_end_x + 10  # Small gap
            cues_end_x = cues_start_x + cues_width
            
            # Summary section
            summary_start_y = notes_end_y + 10  # Small gap
            summary_end_y = summary_start_y + summary_height
            
            # Draw section borders
            # Notes section border
            draw.rectangle(
                [notes_start_x, notes_start_y, notes_end_x, notes_end_y],
                outline=line_color,
                width=2
            )
            
            # Cues section border
            draw.rectangle(
                [cues_start_x, notes_start_y, cues_end_x, notes_end_y],
                outline=line_color,
                width=2
            )
            
            # Summary section border
            draw.rectangle(
                [notes_start_x, summary_start_y, notes_end_x, summary_end_y],
                outline=line_color,
                width=2
            )
            
            # Draw lines in notes section
            y = notes_start_y + 20  # Start lines below title area
            while y < notes_end_y:
                draw.line(
                    [(notes_start_x + 10, y), (notes_end_x - 10, y)],
                    fill=line_color,
                    width=1
                )
                y += line_spacing
            
            # Add section labels
            try:
                # Try to use a system font
                font = ImageFont.load_default()
                font_size = 12
            except:
                font = None
                font_size = 12
            
            # Notes label
            draw.text(
                (notes_start_x + 10, notes_start_y + 5),
                "Notes",
                fill=line_color,
                font=font
            )
            
            # Cues label
            draw.text(
                (cues_start_x + 5, notes_start_y + 5),
                "Cues",
                fill=line_color,
                font=font
            )
            
            # Summary label
            draw.text(
                (notes_start_x + 10, summary_start_y + 5),
                "Summary",
                fill=line_color,
                font=font
            )
            
            self.logger.info("Generated Cornell note-taking template")
            return img
            
        except Exception as e:
            self.logger.error(f"Error generating Cornell template: {e}")
            raise
    
    def generate_blank_template(self) -> Any:
        """
        Generate a blank template.
        
        Returns:
            Any: Generated blank template
        """
        try:
            # Create a white background
            img = Image.new('RGB', (self.DEVICE_WIDTH, self.DEVICE_HEIGHT), 'white')
            
            self.logger.info("Generated blank template")
            return img
            
        except Exception as e:
            self.logger.error(f"Error generating blank template: {e}")
            raise
    
    def save_template(self, template: Any, filepath: str, format: str = 'PNG') -> None:
        """
        Save a template to file.
        
        Args:
            template (Any): Template image to save
            filepath (str): Path where to save the template
            format (str): Image format (PNG, JPEG, etc.)
        """
        try:
            # Ensure the directory exists
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            # Save the template
            template.save(filepath, format)
            
            self.logger.info(f"Template saved to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error saving template: {e}")
            raise
    
    def create_template_from_image(self, image_path: str, resize: bool = True) -> Any:
        """
        Create a template from an existing image file.
        
        Args:
            image_path (str): Path to the source image
            resize (bool): Whether to resize to device dimensions
            
        Returns:
            Any: Processed template image
        """
        try:
            # Load the image
            img = Image.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to device dimensions if requested
            if resize:
                img = img.resize((self.DEVICE_WIDTH, self.DEVICE_HEIGHT), Image.Resampling.LANCZOS)
            
            self.logger.info(f"Created template from image: {image_path}")
            return img
            
        except Exception as e:
            self.logger.error(f"Error creating template from image: {e}")
            raise
    
    def validate_template(self, template: Any) -> Dict[str, Any]:
        """
        Validate a template against device specifications.
        
        Args:
            template (Any): Template to validate
            
        Returns:
            Dict[str, Any]: Validation results
        """
        validation_result = {
            "valid": True,
            "warnings": [],
            "errors": []
        }
        
        try:
            # Check dimensions
            if template.size != (self.DEVICE_WIDTH, self.DEVICE_HEIGHT):
                validation_result["warnings"].append(
                    f"Template size {template.size} doesn't match device size "
                    f"({self.DEVICE_WIDTH}, {self.DEVICE_HEIGHT})"
                )
            
            # Check color mode
            if template.mode not in ['RGB', 'L']:
                validation_result["warnings"].append(
                    f"Template mode '{template.mode}' may not be optimal for e-ink display"
                )
            
            # Check file size (estimate)
            estimated_size = template.size[0] * template.size[1] * 3  # RGB = 3 bytes per pixel
            if estimated_size > 10 * 1024 * 1024:  # 10MB
                validation_result["warnings"].append(
                    "Template file size may be large for device storage"
                )
            
            self.logger.info("Template validation completed")
            
        except Exception as e:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Validation error: {e}")
            self.logger.error(f"Template validation error: {e}")
        
        return validation_result