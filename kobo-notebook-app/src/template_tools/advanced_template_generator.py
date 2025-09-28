"""
Advanced template generation utilities for specialized notebook templates.

This module provides functionality to generate specialized templates for
specific use cases like academic notes, bullet journaling, technical drawings,
and creative writing.
"""

import os
import math
from typing import Tuple, Optional, Dict, Any, List
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    # Create dummy classes for testing
    class Image:
        def __init__(self, mode=None, size=None, color=None):
            self.mode = mode
            self.size = size
            self.color = color
        
        @staticmethod
        def new(mode, size, color):
            return Image(mode, size, color)
        
        @staticmethod
        def open(path):
            return None
        
        def save(self, path, format=None):
            # Mock save - create a file
            with open(path, 'w') as f:
                f.write(f"Mock image: {self.mode}, {self.size}, {self.color}")
        
        def convert(self, mode):
            self.mode = mode
            return self
        
        def resize(self, size, resample=None):
            self.size = size
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
        
        def ellipse(self, xy, fill=None, outline=None, width=1):
            pass
        
        def text(self, xy, text, fill=None, font=None):
            pass
        
        def polygon(self, xy, fill=None, outline=None):
            pass
    
    class ImageFont:
        @staticmethod
        def load_default():
            return None

from utils.logger import setup_logger
from .template_generator import TemplateGenerator


class AdvancedTemplateGenerator(TemplateGenerator):
    """Generates specialized notebook templates for specific use cases."""
    
    def __init__(self):
        """Initialize the advanced template generator."""
        super().__init__()
        
    def generate_bullet_journal_template(
        self,
        dot_spacing: int = 5,
        margin_top: int = 50,
        margin_bottom: int = 50,
        margin_left: int = 40,
        margin_right: int = 40,
        header_height: int = 100,
        footer_height: int = 80
    ) -> Any:
        """
        Generate a bullet journal template with monthly/weekly layout.
        
        Args:
            dot_spacing (int): Spacing between dots in pixels
            margin_top (int): Top margin in pixels
            margin_bottom (int): Bottom margin in pixels
            margin_left (int): Left margin in pixels
            margin_right (int): Right margin in pixels
            header_height (int): Height of header section
            footer_height (int): Height of footer section
            
        Returns:
            Any: Generated bullet journal template
        """
        try:
            # Create a white background
            img = Image.new('RGB', (self.DEVICE_WIDTH, self.DEVICE_HEIGHT), 'white')
            draw = ImageDraw.Draw(img)
            
            # Calculate sections
            header_start = margin_top
            header_end = header_start + header_height
            footer_start = self.DEVICE_HEIGHT - margin_bottom - footer_height
            footer_end = self.DEVICE_HEIGHT - margin_bottom
            
            # Draw header section
            draw.rectangle(
                [(margin_left, header_start), (self.DEVICE_WIDTH - margin_right, header_end)],
                outline="#000000",
                width=2
            )
            
            # Draw footer section
            draw.rectangle(
                [(margin_left, footer_start), (self.DEVICE_WIDTH - margin_right, footer_end)],
                outline="#000000",
                width=2
            )
            
            # Add header labels
            try:
                font = ImageFont.load_default()
            except:
                font = None
            
            # Header labels
            draw.text((margin_left + 10, header_start + 10), "MONTH:", fill="#000000", font=font)
            draw.text((margin_left + 10, header_start + 30), "YEAR:", fill="#000000", font=font)
            draw.text((margin_left + 10, header_start + 50), "GOALS:", fill="#000000", font=font)
            
            # Footer labels
            draw.text((margin_left + 10, footer_start + 10), "NOTES:", fill="#000000", font=font)
            draw.text((margin_left + 10, footer_start + 30), "REFLECTION:", fill="#000000", font=font)
            
            # Draw dot grid in main area
            start_x = margin_left
            end_x = self.DEVICE_WIDTH - margin_right
            start_y = header_end + 20
            end_y = footer_start - 20
            
            y = start_y
            while y <= end_y:
                x = start_x
                while x <= end_x:
                    draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill="#000000")
                    x += dot_spacing
                y += dot_spacing
            
            # Add monthly calendar grid (7x5)
            calendar_width = 200
            calendar_height = 150
            calendar_x = self.DEVICE_WIDTH - margin_right - calendar_width - 10
            calendar_y = header_start + 10
            
            # Draw calendar grid
            for i in range(8):  # 7 days + header
                y_pos = calendar_y + (i * calendar_height // 7)
                draw.line(
                    [(calendar_x, y_pos), (calendar_x + calendar_width, y_pos)],
                    fill="#000000",
                    width=1
                )
            
            for i in range(8):  # 7 days + header
                x_pos = calendar_x + (i * calendar_width // 7)
                draw.line(
                    [(x_pos, calendar_y), (x_pos, calendar_y + calendar_height)],
                    fill="#000000",
                    width=1
                )
            
            # Add day labels
            days = ["S", "M", "T", "W", "T", "F", "S"]
            for i, day in enumerate(days):
                x_pos = calendar_x + (i * calendar_width // 7) + 5
                draw.text((x_pos, calendar_y + 5), day, fill="#000000", font=font)
            
            self.logger.info("Generated bullet journal template")
            return img
            
        except Exception as e:
            self.logger.error(f"Error generating bullet journal template: {e}")
            raise
    
    def generate_academic_notes_template(
        self,
        line_spacing: int = 8,
        margin_top: int = 50,
        margin_bottom: int = 50,
        margin_left: int = 40,
        margin_right: int = 40,
        sidebar_width: int = 100
    ) -> Any:
        """
        Generate an academic note-taking template with sidebar for keywords.
        
        Args:
            line_spacing (int): Spacing between lines in pixels
            margin_top (int): Top margin in pixels
            margin_bottom (int): Bottom margin in pixels
            margin_left (int): Left margin in pixels
            margin_right (int): Right margin in pixels
            sidebar_width (int): Width of sidebar for keywords
            
        Returns:
            Any: Generated academic notes template
        """
        try:
            # Create a white background
            img = Image.new('RGB', (self.DEVICE_WIDTH, self.DEVICE_HEIGHT), 'white')
            draw = ImageDraw.Draw(img)
            
            # Calculate sections
            notes_start_x = margin_left
            notes_end_x = self.DEVICE_WIDTH - margin_right - sidebar_width - 20
            sidebar_start_x = notes_end_x + 20
            sidebar_end_x = self.DEVICE_WIDTH - margin_right
            
            start_y = margin_top
            end_y = self.DEVICE_HEIGHT - margin_bottom
            
            # Draw main notes area
            draw.rectangle(
                [(notes_start_x, start_y), (notes_end_x, end_y)],
                outline="#000000",
                width=2
            )
            
            # Draw sidebar
            draw.rectangle(
                [(sidebar_start_x, start_y), (sidebar_end_x, end_y)],
                outline="#000000",
                width=2
            )
            
            # Add section labels
            try:
                font = ImageFont.load_default()
            except:
                font = None
            
            # Notes section label
            draw.text((notes_start_x + 10, start_y + 10), "NOTES", fill="#000000", font=font)
            
            # Sidebar label
            draw.text((sidebar_start_x + 10, start_y + 10), "KEYWORDS", fill="#000000", font=font)
            
            # Draw lines in notes section
            y = start_y + 40
            while y < end_y - 20:
                draw.line(
                    [(notes_start_x + 10, y), (notes_end_x - 10, y)],
                    fill="#000000",
                    width=1
                )
                y += line_spacing
            
            # Add keyword lines in sidebar
            y = start_y + 40
            while y < end_y - 20:
                draw.line(
                    [(sidebar_start_x + 10, y), (sidebar_end_x - 10, y)],
                    fill="#CCCCCC",
                    width=1
                )
                y += line_spacing * 2
            
            # Add page number area
            page_num_x = self.DEVICE_WIDTH - margin_right - 50
            page_num_y = end_y - 30
            draw.text((page_num_x, page_num_y), "Page:", fill="#000000", font=font)
            
            self.logger.info("Generated academic notes template")
            return img
            
        except Exception as e:
            self.logger.error(f"Error generating academic notes template: {e}")
            raise
    
    def generate_technical_drawing_template(
        self,
        grid_size: int = 10,
        margin_top: int = 50,
        margin_bottom: int = 50,
        margin_left: int = 40,
        margin_right: int = 40,
        title_height: int = 60
    ) -> Any:
        """
        Generate a technical drawing template with grid and title block.
        
        Args:
            grid_size (int): Size of grid squares in pixels
            margin_top (int): Top margin in pixels
            margin_bottom (int): Bottom margin in pixels
            margin_left (int): Left margin in pixels
            margin_right (int): Right margin in pixels
            title_height (int): Height of title block
            
        Returns:
            Any: Generated technical drawing template
        """
        try:
            # Create a white background
            img = Image.new('RGB', (self.DEVICE_WIDTH, self.DEVICE_HEIGHT), 'white')
            draw = ImageDraw.Draw(img)
            
            # Calculate drawing area
            start_x = margin_left
            end_x = self.DEVICE_WIDTH - margin_right
            start_y = margin_top + title_height + 20
            end_y = self.DEVICE_HEIGHT - margin_bottom
            
            # Draw title block
            title_start_y = margin_top
            title_end_y = title_start_y + title_height
            draw.rectangle(
                [(start_x, title_start_y), (end_x, title_end_y)],
                outline="#000000",
                width=2
            )
            
            # Add title block fields
            try:
                font = ImageFont.load_default()
            except:
                font = None
            
            # Title block labels
            draw.text((start_x + 10, title_start_y + 10), "TITLE:", fill="#000000", font=font)
            draw.text((start_x + 10, title_start_y + 30), "DRAWING NO:", fill="#000000", font=font)
            draw.text((start_x + 200, title_start_y + 10), "SCALE:", fill="#000000", font=font)
            draw.text((start_x + 200, title_start_y + 30), "DATE:", fill="#000000", font=font)
            draw.text((end_x - 150, title_start_y + 10), "DRAWN BY:", fill="#000000", font=font)
            draw.text((end_x - 150, title_start_y + 30), "CHECKED BY:", fill="#000000", font=font)
            
            # Draw main grid
            # Vertical lines
            x = start_x
            while x <= end_x:
                draw.line(
                    [(x, start_y), (x, end_y)],
                    fill="#000000",
                    width=1
                )
                x += grid_size
            
            # Horizontal lines
            y = start_y
            while y <= end_y:
                draw.line(
                    [(start_x, y), (end_x, y)],
                    fill="#000000",
                    width=1
                )
                y += grid_size
            
            # Add border
            draw.rectangle(
                [(start_x, start_y), (end_x, end_y)],
                outline="#000000",
                width=3
            )
            
            # Add coordinate labels (every 10th line)
            label_font_size = 8
            for i in range(0, (end_x - start_x) // grid_size + 1, 10):
                x_pos = start_x + (i * grid_size)
                if x_pos <= end_x:
                    draw.text((x_pos, start_y - 20), str(i), fill="#000000", font=font)
            
            for i in range(0, (end_y - start_y) // grid_size + 1, 10):
                y_pos = start_y + (i * grid_size)
                if y_pos <= end_y:
                    draw.text((start_x - 20, y_pos), str(i), fill="#000000", font=font)
            
            self.logger.info("Generated technical drawing template")
            return img
            
        except Exception as e:
            self.logger.error(f"Error generating technical drawing template: {e}")
            raise
    
    def generate_creative_writing_template(
        self,
        line_spacing: int = 10,
        margin_top: int = 50,
        margin_bottom: int = 50,
        margin_left: int = 40,
        margin_right: int = 40,
        header_height: int = 80
    ) -> Any:
        """
        Generate a creative writing template with story structure.
        
        Args:
            line_spacing (int): Spacing between lines in pixels
            margin_top (int): Top margin in pixels
            margin_bottom (int): Bottom margin in pixels
            margin_left (int): Left margin in pixels
            margin_right (int): Right margin in pixels
            header_height (int): Height of header section
            
        Returns:
            Any: Generated creative writing template
        """
        try:
            # Create a white background
            img = Image.new('RGB', (self.DEVICE_WIDTH, self.DEVICE_HEIGHT), 'white')
            draw = ImageDraw.Draw(img)
            
            # Calculate sections
            header_start = margin_top
            header_end = header_start + header_height
            start_y = header_end + 20
            end_y = self.DEVICE_HEIGHT - margin_bottom
            
            # Draw header section
            draw.rectangle(
                [(margin_left, header_start), (self.DEVICE_WIDTH - margin_right, header_end)],
                outline="#000000",
                width=2
            )
            
            # Add header fields
            try:
                font = ImageFont.load_default()
            except:
                font = None
            
            # Header labels
            draw.text((margin_left + 10, header_start + 10), "TITLE:", fill="#000000", font=font)
            draw.text((margin_left + 10, header_start + 30), "AUTHOR:", fill="#000000", font=font)
            draw.text((margin_left + 10, header_start + 50), "DATE:", fill="#000000", font=font)
            draw.text((margin_left + 200, header_start + 10), "GENRE:", fill="#000000", font=font)
            draw.text((margin_left + 200, header_start + 30), "WORD COUNT:", fill="#000000", font=font)
            draw.text((margin_left + 200, header_start + 50), "PAGE:", fill="#000000", font=font)
            
            # Draw writing lines
            y = start_y
            while y < end_y:
                draw.line(
                    [(margin_left, y), (self.DEVICE_WIDTH - margin_right, y)],
                    fill="#000000",
                    width=1
                )
                y += line_spacing
            
            # Add margin line
            margin_line_x = margin_left + 50
            y = start_y
            while y < end_y:
                draw.line(
                    [(margin_line_x, y), (margin_line_x, y + line_spacing - 2)],
                    fill="#CCCCCC",
                    width=1
                )
                y += line_spacing
            
            # Add paragraph indicators (small dots every few lines)
            y = start_y + (line_spacing * 2)
            while y < end_y:
                draw.ellipse([margin_left - 10, y - 2, margin_left - 6, y + 2], fill="#000000")
                y += line_spacing * 5
            
            self.logger.info("Generated creative writing template")
            return img
            
        except Exception as e:
            self.logger.error(f"Error generating creative writing template: {e}")
            raise
    
    def generate_meeting_notes_template(
        self,
        line_spacing: int = 8,
        margin_top: int = 50,
        margin_bottom: int = 50,
        margin_left: int = 40,
        margin_right: int = 40,
        header_height: int = 120
    ) -> Any:
        """
        Generate a meeting notes template with structured sections.
        
        Args:
            line_spacing (int): Spacing between lines in pixels
            margin_top (int): Top margin in pixels
            margin_bottom (int): Bottom margin in pixels
            margin_left (int): Left margin in pixels
            margin_right (int): Right margin in pixels
            header_height (int): Height of header section
            
        Returns:
            Any: Generated meeting notes template
        """
        try:
            # Create a white background
            img = Image.new('RGB', (self.DEVICE_WIDTH, self.DEVICE_HEIGHT), 'white')
            draw = ImageDraw.Draw(img)
            
            # Calculate sections
            header_start = margin_top
            header_end = header_start + header_height
            start_y = header_end + 20
            end_y = self.DEVICE_HEIGHT - margin_bottom
            
            # Draw header section
            draw.rectangle(
                [(margin_left, header_start), (self.DEVICE_WIDTH - margin_right, header_end)],
                outline="#000000",
                width=2
            )
            
            # Add header fields
            try:
                font = ImageFont.load_default()
            except:
                font = None
            
            # Header labels
            draw.text((margin_left + 10, header_start + 10), "MEETING:", fill="#000000", font=font)
            draw.text((margin_left + 10, header_start + 30), "DATE:", fill="#000000", font=font)
            draw.text((margin_left + 10, header_start + 50), "TIME:", fill="#000000", font=font)
            draw.text((margin_left + 10, header_start + 70), "ATTENDEES:", fill="#000000", font=font)
            draw.text((margin_left + 10, header_start + 90), "AGENDA:", fill="#000000", font=font)
            
            # Draw main content area with sections
            content_height = end_y - start_y
            section_height = content_height // 4
            
            sections = ["DISCUSSION", "ACTION ITEMS", "DECISIONS", "NEXT STEPS"]
            
            for i, section in enumerate(sections):
                section_start_y = start_y + (i * section_height)
                section_end_y = section_start_y + section_height
                
                # Draw section border
                draw.rectangle(
                    [(margin_left, section_start_y), (self.DEVICE_WIDTH - margin_right, section_end_y)],
                    outline="#000000",
                    width=1
                )
                
                # Add section label
                draw.text((margin_left + 10, section_start_y + 10), section, fill="#000000", font=font)
                
                # Draw lines in section
                y = section_start_y + 30
                while y < section_end_y - 10:
                    draw.line(
                        [(margin_left + 10, y), (self.DEVICE_WIDTH - margin_right - 10, y)],
                        fill="#000000",
                        width=1
                    )
                    y += line_spacing
            
            self.logger.info("Generated meeting notes template")
            return img
            
        except Exception as e:
            self.logger.error(f"Error generating meeting notes template: {e}")
            raise
    
    def generate_mind_map_template(
        self,
        center_x: int = None,
        center_y: int = None,
        radius: int = 200,
        branches: int = 8
    ) -> Any:
        """
        Generate a mind map template with central node and branches.
        
        Args:
            center_x (int): X coordinate of center (default: center of page)
            center_y (int): Y coordinate of center (default: center of page)
            radius (int): Radius of the central circle
            branches (int): Number of main branches
            
        Returns:
            Any: Generated mind map template
        """
        try:
            # Create a white background
            img = Image.new('RGB', (self.DEVICE_WIDTH, self.DEVICE_HEIGHT), 'white')
            draw = ImageDraw.Draw(img)
            
            # Set center coordinates
            if center_x is None:
                center_x = self.DEVICE_WIDTH // 2
            if center_y is None:
                center_y = self.DEVICE_HEIGHT // 2
            
            # Draw central circle
            draw.ellipse(
                [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
                outline="#000000",
                width=3
            )
            
            # Add center label
            try:
                font = ImageFont.load_default()
            except:
                font = None
            
            draw.text((center_x - 20, center_y - 10), "TOPIC", fill="#000000", font=font)
            
            # Draw branches
            for i in range(branches):
                angle = (2 * math.pi * i) / branches
                
                # Calculate branch end point
                branch_length = 300
                end_x = center_x + int(branch_length * math.cos(angle))
                end_y = center_y + int(branch_length * math.sin(angle))
                
                # Draw branch line
                draw.line(
                    [(center_x, center_y), (end_x, end_y)],
                    fill="#000000",
                    width=2
                )
                
                # Draw branch circle
                branch_radius = 30
                draw.ellipse(
                    [end_x - branch_radius, end_y - branch_radius, 
                     end_x + branch_radius, end_y + branch_radius],
                    outline="#000000",
                    width=2
                )
                
                # Add branch label
                label_x = end_x - 15
                label_y = end_y - 10
                draw.text((label_x, label_y), f"IDEA {i+1}", fill="#000000", font=font)
                
                # Draw sub-branches
                for j in range(3):
                    sub_angle = angle + (math.pi / 6) * (j - 1)
                    sub_length = 150
                    sub_end_x = end_x + int(sub_length * math.cos(sub_angle))
                    sub_end_y = end_y + int(sub_length * math.sin(sub_angle))
                    
                    draw.line(
                        [(end_x, end_y), (sub_end_x, sub_end_y)],
                        fill="#CCCCCC",
                        width=1
                    )
                    
                    # Small circle for sub-branch
                    draw.ellipse(
                        [sub_end_x - 10, sub_end_y - 10, sub_end_x + 10, sub_end_y + 10],
                        outline="#CCCCCC",
                        width=1
                    )
            
            self.logger.info("Generated mind map template")
            return img
            
        except Exception as e:
            self.logger.error(f"Error generating mind map template: {e}")
            raise