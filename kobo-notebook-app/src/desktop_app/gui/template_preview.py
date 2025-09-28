"""
Template preview functionality for the Kobo Notebook App.

This module provides template preview capabilities including zoom, pan,
and real-time preview of template generation.
"""

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    TKINTER_AVAILABLE = True
except ImportError:
    # Use mock tkinter for testing
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
    from mock_tkinter import *
    import mock_tkinter as tk
    TKINTER_AVAILABLE = False
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from utils.logger import setup_logger


class TemplatePreview:
    """Template preview window with zoom and pan capabilities."""
    
    def __init__(self, parent):
        """Initialize the template preview."""
        self.parent = parent
        self.logger = setup_logger()
        self.current_template = None
        self.zoom_factor = 1.0
        self.pan_x = 0
        self.pan_y = 0
        
        # Create preview window
        self.window = tk.Toplevel(parent)
        self.window.title("Template Preview")
        self.window.geometry("800x600")
        self.window.minsize(400, 300)
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create the preview window widgets."""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Zoom controls
        ttk.Label(toolbar, text="Zoom:").grid(row=0, column=0, padx=(0, 5))
        
        self.zoom_var = tk.StringVar(value="100%")
        zoom_combo = ttk.Combobox(
            toolbar,
            textvariable=self.zoom_var,
            values=["25%", "50%", "75%", "100%", "125%", "150%", "200%"],
            state="readonly",
            width=8
        )
        zoom_combo.grid(row=0, column=1, padx=(0, 10))
        zoom_combo.bind("<<ComboboxSelected>>", self.on_zoom_change)
        
        # Zoom buttons
        ttk.Button(toolbar, text="+", command=self.zoom_in, width=3).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(toolbar, text="-", command=self.zoom_out, width=3).grid(row=0, column=3, padx=(0, 10))
        ttk.Button(toolbar, text="Fit", command=self.zoom_fit, width=4).grid(row=0, column=4, padx=(0, 10))
        
        # Pan controls
        ttk.Label(toolbar, text="Pan:").grid(row=0, column=5, padx=(0, 5))
        ttk.Button(toolbar, text="↑", command=self.pan_up, width=3).grid(row=0, column=6, padx=(0, 2))
        ttk.Button(toolbar, text="↓", command=self.pan_down, width=3).grid(row=0, column=7, padx=(0, 2))
        ttk.Button(toolbar, text="←", command=self.pan_left, width=3).grid(row=0, column=8, padx=(0, 2))
        ttk.Button(toolbar, text="→", command=self.pan_right, width=3).grid(row=0, column=9, padx=(0, 10))
        
        # Center button
        ttk.Button(toolbar, text="Center", command=self.center_view, width=6).grid(row=0, column=10, padx=(0, 10))
        
        # Info panel
        info_frame = ttk.LabelFrame(main_frame, text="Template Information", padding="5")
        info_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        info_frame.columnconfigure(0, weight=1)
        
        # Template info
        self.info_text = tk.Text(info_frame, height=15, width=30, wrap=tk.WORD)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for info text
        info_scroll = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=info_scroll.set)
        info_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Preview canvas
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)
        
        # Create canvas with scrollbars
        self.canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=1, highlightbackground="gray")
        
        # Scrollbars
        h_scroll = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        
        # Grid layout
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        h_scroll.grid(row=1, column=0, sticky=(tk.W, tk.E))
        v_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind mouse events for panning
        self.canvas.bind("<Button-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.pan)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def show_template(self, template: Any, template_info: Dict[str, Any] = None):
        """Display a template in the preview window."""
        try:
            self.current_template = template
            self.update_template_info(template_info or {})
            self.render_template()
            self.status_var.set("Template loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Error showing template: {e}")
            messagebox.showerror("Error", f"Failed to display template: {e}")
            self.status_var.set(f"Error: {e}")
    
    def update_template_info(self, info: Dict[str, Any]):
        """Update the template information panel."""
        self.info_text.delete(1.0, tk.END)
        
        info_text = "Template Information\n" + "=" * 20 + "\n\n"
        
        if info:
            for key, value in info.items():
                info_text += f"{key}: {value}\n"
        else:
            info_text += "Type: Generated Template\n"
            info_text += "Size: 1404 x 1872 pixels\n"
            info_text += "Format: PNG\n"
            info_text += "DPI: 300\n"
            info_text += "Color: Black & White\n"
        
        info_text += f"\nZoom: {self.zoom_var.get()}\n"
        info_text += f"Pan: ({self.pan_x}, {self.pan_y})\n"
        
        self.info_text.insert(1.0, info_text)
    
    def render_template(self):
        """Render the current template on the canvas."""
        if not self.current_template:
            return
        
        # Clear canvas
        self.canvas.delete("all")
        
        # For now, show a placeholder since we don't have PIL available
        # In a real implementation, this would render the actual template image
        
        # Create a placeholder representation
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            # Canvas not yet sized, schedule for later
            self.window.after(100, self.render_template)
            return
        
        # Draw template outline
        template_width = 1404 * self.zoom_factor
        template_height = 1872 * self.zoom_factor
        
        # Center the template
        x = (canvas_width - template_width) / 2 + self.pan_x
        y = (canvas_height - template_height) / 2 + self.pan_y
        
        # Draw template border
        self.canvas.create_rectangle(
            x, y, x + template_width, y + template_height,
            outline="black", width=2, tags="template"
        )
        
        # Draw template content (simplified representation)
        if hasattr(self.current_template, '__class__') and 'Lined' in str(self.current_template.__class__):
            # Draw lines for lined template
            for i in range(0, int(template_height), int(10 * self.zoom_factor)):
                self.canvas.create_line(
                    x, y + i, x + template_width, y + i,
                    fill="lightgray", width=1, tags="template"
                )
        elif hasattr(self.current_template, '__class__') and 'Grid' in str(self.current_template.__class__):
            # Draw grid for grid template
            for i in range(0, int(template_width), int(14 * self.zoom_factor)):
                self.canvas.create_line(
                    x + i, y, x + i, y + template_height,
                    fill="lightgray", width=1, tags="template"
                )
            for i in range(0, int(template_height), int(14 * self.zoom_factor)):
                self.canvas.create_line(
                    x, y + i, x + template_width, y + i,
                    fill="lightgray", width=1, tags="template"
                )
        
        # Add template label
        self.canvas.create_text(
            x + template_width/2, y - 20,
            text="Template Preview (1404 x 1872 px)",
            fill="black", font=("Arial", 10), tags="template"
        )
        
        # Update scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_zoom_change(self, event=None):
        """Handle zoom level change."""
        zoom_text = self.zoom_var.get()
        zoom_value = float(zoom_text.rstrip('%')) / 100.0
        self.zoom_factor = zoom_value
        self.render_template()
        self.update_template_info({})
    
    def zoom_in(self):
        """Zoom in on the template."""
        current_zoom = float(self.zoom_var.get().rstrip('%'))
        new_zoom = min(current_zoom * 1.25, 400)
        self.zoom_var.set(f"{new_zoom:.0f}%")
        self.on_zoom_change()
    
    def zoom_out(self):
        """Zoom out on the template."""
        current_zoom = float(self.zoom_var.get().rstrip('%'))
        new_zoom = max(current_zoom / 1.25, 25)
        self.zoom_var.set(f"{new_zoom:.0f}%")
        self.on_zoom_change()
    
    def zoom_fit(self):
        """Fit template to window."""
        self.zoom_var.set("100%")
        self.pan_x = 0
        self.pan_y = 0
        self.on_zoom_change()
    
    def pan_up(self):
        """Pan up."""
        self.pan_y += 50
        self.render_template()
        self.update_template_info({})
    
    def pan_down(self):
        """Pan down."""
        self.pan_y -= 50
        self.render_template()
        self.update_template_info({})
    
    def pan_left(self):
        """Pan left."""
        self.pan_x += 50
        self.render_template()
        self.update_template_info({})
    
    def pan_right(self):
        """Pan right."""
        self.pan_x -= 50
        self.render_template()
        self.update_template_info({})
    
    def center_view(self):
        """Center the view."""
        self.pan_x = 0
        self.pan_y = 0
        self.render_template()
        self.update_template_info({})
    
    def start_pan(self, event):
        """Start panning operation."""
        self.last_x = event.x
        self.last_y = event.y
    
    def pan(self, event):
        """Pan the view."""
        if hasattr(self, 'last_x'):
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            self.pan_x += dx
            self.pan_y += dy
            self.last_x = event.x
            self.last_y = event.y
            self.render_template()
            self.update_template_info({})
    
    def on_mousewheel(self, event):
        """Handle mouse wheel zoom."""
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()
    
    def close(self):
        """Close the preview window."""
        self.window.destroy()


class TemplatePreviewDialog:
    """Dialog for template preview with generation options."""
    
    def __init__(self, parent):
        """Initialize the preview dialog."""
        self.parent = parent
        self.logger = setup_logger()
        self.preview_window = None
        
    def show_preview_dialog(self, template_type: str, parameters: Dict[str, Any]):
        """Show template preview dialog."""
        try:
            # Create preview window
            self.preview_window = TemplatePreview(self.parent)
            
            # Generate template for preview
            from template_tools.template_generator import TemplateGenerator
            generator = TemplateGenerator()
            
            template = None
            if template_type == "Lined":
                template = generator.generate_lined_template(
                    line_spacing=parameters.get('line_spacing', 7)
                )
            elif template_type == "Grid":
                template = generator.generate_grid_template(
                    grid_size=parameters.get('grid_size', 5)
                )
            elif template_type == "Dot Grid":
                template = generator.generate_dot_grid_template(
                    dot_spacing=parameters.get('dot_spacing', 5)
                )
            elif template_type == "Cornell Notes":
                template = generator.generate_cornell_template()
            elif template_type == "Blank":
                template = generator.generate_blank_template()
            
            if template:
                template_info = {
                    "Type": template_type,
                    "Parameters": str(parameters),
                    "Generated": "Just now"
                }
                self.preview_window.show_template(template, template_info)
            
        except Exception as e:
            self.logger.error(f"Error showing preview dialog: {e}")
            messagebox.showerror("Error", f"Failed to show preview: {e}")
    
    def close_preview(self):
        """Close the preview dialog."""
        if self.preview_window:
            self.preview_window.close()
            self.preview_window = None