"""
Main window GUI for the Kobo Notebook App.

This module provides the main application window with tabs for different
functionality: device management, template creation, template library, and settings.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from utils.device_manager import DeviceManager
from utils.logger import setup_logger
from desktop_app.gui.template_preview import TemplatePreviewDialog


class MainWindow:
    """Main application window with tabbed interface."""
    
    def __init__(self, root):
        """Initialize the main window."""
        self.root = root
        self.logger = setup_logger()
        self.device_manager = DeviceManager()
        self.preview_dialog = TemplatePreviewDialog(root)
        
        # Window configuration
        self.root.title("Kobo Notebook App - Custom Template Manager")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Configure style
        self.setup_styles()
        
        # Create the main interface
        self.create_widgets()
        
        # Initialize device detection
        self.detect_devices()
        
        self.logger.info("Main window initialized successfully")
    
    def setup_styles(self):
        """Configure the application styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Status.TLabel', font=('Arial', 10))
        
    def create_widgets(self):
        """Create the main widgets for the application."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Kobo Notebook App", 
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs
        self.create_device_tab()
        self.create_template_tab()
        self.create_library_tab()
        self.create_settings_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            main_frame, 
            textvariable=self.status_var, 
            style='Status.TLabel',
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_device_tab(self):
        """Create the device management tab."""
        device_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(device_frame, text="Device")
        
        # Device detection section
        device_section = ttk.LabelFrame(device_frame, text="Device Detection", padding="10")
        device_section.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        device_section.columnconfigure(1, weight=1)
        
        ttk.Label(device_section, text="Status:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.device_status_var = tk.StringVar(value="No device detected")
        self.device_status_label = ttk.Label(device_section, textvariable=self.device_status_var)
        self.device_status_label.grid(row=0, column=1, sticky=tk.W)
        
        self.refresh_button = ttk.Button(
            device_section, 
            text="Refresh", 
            command=self.detect_devices
        )
        self.refresh_button.grid(row=0, column=2, padx=(10, 0))
        
        # Device information section
        info_section = ttk.LabelFrame(device_frame, text="Device Information", padding="10")
        info_section.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        info_section.columnconfigure(1, weight=1)
        info_section.rowconfigure(4, weight=1)
        
        # Device details
        self.device_details = {}
        labels = ["Model:", "Firmware:", "Storage:", "Templates:"]
        self.detail_vars = {}
        
        for i, label in enumerate(labels):
            ttk.Label(info_section, text=label).grid(row=i, column=0, sticky=tk.W, pady=2)
            var = tk.StringVar(value="Unknown")
            self.detail_vars[label.rstrip(':')] = var
            ttk.Label(info_section, textvariable=var).grid(row=i, column=1, sticky=tk.W, padx=(10, 0))
        
        # Backup section
        backup_section = ttk.LabelFrame(device_frame, text="Backup & Restore", padding="10")
        backup_section.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Button(
            backup_section, 
            text="Create Backup", 
            command=self.create_backup
        ).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(
            backup_section, 
            text="Restore Backup", 
            command=self.restore_backup
        ).grid(row=0, column=1)
    
    def create_template_tab(self):
        """Create the template creation tab."""
        template_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(template_frame, text="Create Template")
        
        # Template creation section
        create_section = ttk.LabelFrame(template_frame, text="Template Creation", padding="10")
        create_section.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        create_section.columnconfigure(1, weight=1)
        
        # Template type selection
        ttk.Label(create_section, text="Template Type:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.template_type_var = tk.StringVar(value="Lined")
        template_types = ["Lined", "Grid", "Dot Grid", "Cornell Notes", "Blank", "Custom"]
        template_combo = ttk.Combobox(
            create_section, 
            textvariable=self.template_type_var, 
            values=template_types,
            state="readonly"
        )
        template_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # Template parameters
        params_section = ttk.LabelFrame(template_frame, text="Template Parameters", padding="10")
        params_section.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        params_section.columnconfigure(1, weight=1)
        
        # Line spacing (for lined templates)
        ttk.Label(params_section, text="Line Spacing:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.line_spacing_var = tk.StringVar(value="7")
        ttk.Entry(params_section, textvariable=self.line_spacing_var, width=10).grid(
            row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2
        )
        
        # Grid size (for grid templates)
        ttk.Label(params_section, text="Grid Size:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.grid_size_var = tk.StringVar(value="5")
        ttk.Entry(params_section, textvariable=self.grid_size_var, width=10).grid(
            row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2
        )
        
        # Action buttons
        action_frame = ttk.Frame(template_frame)
        action_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Button(
            action_frame, 
            text="Preview Template", 
            command=self.preview_template
        ).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(
            action_frame, 
            text="Create Template", 
            command=self.create_template
        ).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(
            action_frame, 
            text="Import Template", 
            command=self.import_template
        ).grid(row=0, column=2)
    
    def create_library_tab(self):
        """Create the template library tab."""
        library_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(library_frame, text="Template Library")
        
        # Library list section
        list_section = ttk.LabelFrame(library_frame, text="Available Templates", padding="10")
        list_section.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_section.columnconfigure(0, weight=1)
        list_section.rowconfigure(1, weight=1)
        
        # Search/filter
        search_frame = ttk.Frame(list_section)
        search_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        search_frame.columnconfigure(0, weight=1)
        
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, sticky=tk.W)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # Template list
        columns = ("Name", "Type", "Size", "Created")
        self.template_tree = ttk.Treeview(list_section, columns=columns, show="headings")
        
        for col in columns:
            self.template_tree.heading(col, text=col)
            self.template_tree.column(col, width=150)
        
        # Scrollbar for treeview
        tree_scroll = ttk.Scrollbar(list_section, orient=tk.VERTICAL, command=self.template_tree.yview)
        self.template_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.template_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_scroll.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Library actions
        library_actions = ttk.Frame(library_frame)
        library_actions.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(
            library_actions, 
            text="Install Selected", 
            command=self.install_selected_template
        ).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(
            library_actions, 
            text="Export Template", 
            command=self.export_template
        ).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(
            library_actions, 
            text="Delete Template", 
            command=self.delete_template
        ).grid(row=0, column=2)
    
    def create_settings_tab(self):
        """Create the settings tab."""
        settings_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(settings_frame, text="Settings")
        
        # General settings
        general_section = ttk.LabelFrame(settings_frame, text="General Settings", padding="10")
        general_section.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        general_section.columnconfigure(1, weight=1)
        
        # Auto-detect devices
        self.auto_detect_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            general_section, 
            text="Auto-detect connected devices", 
            variable=self.auto_detect_var
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Backup directory
        ttk.Label(general_section, text="Backup Directory:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.backup_dir_var = tk.StringVar(value=str(Path.home() / "kobo_backups"))
        ttk.Entry(general_section, textvariable=self.backup_dir_var).grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2
        )
        ttk.Button(
            general_section, 
            text="Browse", 
            command=self.browse_backup_dir
        ).grid(row=1, column=2, padx=(10, 0), pady=2)
        
        # About section
        about_section = ttk.LabelFrame(settings_frame, text="About", padding="10")
        about_section.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        about_text = """Kobo Notebook App v0.1.0

A desktop application for creating and installing custom notebook templates 
on Kobo Elipsa 2e devices.

⚠️ WARNING: This application modifies your device's firmware. 
Use at your own risk and always backup your device first.

For support and updates, visit the project repository."""
        
        about_label = ttk.Label(about_section, text=about_text, justify=tk.LEFT)
        about_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
    
    def detect_devices(self):
        """Detect connected Kobo devices."""
        self.status_var.set("Detecting devices...")
        self.root.update()
        
        try:
            devices = self.device_manager.detect_devices()
            if devices:
                device = devices[0]  # Use first detected device
                self.device_status_var.set(f"Connected: {device['model']}")
                self.detail_vars['Model'].set(device['model'])
                self.detail_vars['Firmware'].set(device['firmware'])
                self.detail_vars['Storage'].set(device['storage'])
                self.detail_vars['Templates'].set(str(device['template_count']))
                self.status_var.set("Device detected successfully")
            else:
                self.device_status_var.set("No device detected")
                self.status_var.set("No Kobo device found")
        except Exception as e:
            self.device_status_var.set("Error detecting device")
            self.status_var.set(f"Error: {e}")
            self.logger.error(f"Device detection error: {e}")
    
    def create_backup(self):
        """Create a backup of the device."""
        if not self.device_manager.has_connected_device():
            messagebox.showwarning("No Device", "Please connect a Kobo device first.")
            return
        
        backup_dir = filedialog.askdirectory(
            title="Select Backup Directory",
            initialdir=self.backup_dir_var.get()
        )
        
        if backup_dir:
            try:
                self.status_var.set("Creating backup...")
                self.device_manager.create_backup(backup_dir)
                self.status_var.set("Backup created successfully")
                messagebox.showinfo("Success", f"Backup created in {backup_dir}")
            except Exception as e:
                self.status_var.set(f"Backup failed: {e}")
                messagebox.showerror("Backup Failed", str(e))
    
    def restore_backup(self):
        """Restore a backup to the device."""
        if not self.device_manager.has_connected_device():
            messagebox.showwarning("No Device", "Please connect a Kobo device first.")
            return
        
        backup_file = filedialog.askopenfilename(
            title="Select Backup File",
            filetypes=[("Backup files", "*.kobo_backup"), ("All files", "*.*")]
        )
        
        if backup_file:
            if messagebox.askyesno("Confirm Restore", 
                                 "This will restore your device from backup. Continue?"):
                try:
                    self.status_var.set("Restoring backup...")
                    self.device_manager.restore_backup(backup_file)
                    self.status_var.set("Backup restored successfully")
                    messagebox.showinfo("Success", "Backup restored successfully")
                except Exception as e:
                    self.status_var.set(f"Restore failed: {e}")
                    messagebox.showerror("Restore Failed", str(e))
    
    def preview_template(self):
        """Preview the selected template."""
        try:
            # Get current template parameters
            template_type = self.template_type_var.get()
            parameters = {}
            
            if template_type == "Lined":
                parameters['line_spacing'] = int(self.line_spacing_var.get())
            elif template_type == "Grid":
                parameters['grid_size'] = int(self.grid_size_var.get())
            elif template_type == "Dot Grid":
                parameters['dot_spacing'] = int(self.grid_size_var.get())  # Reuse grid_size for dot spacing
            
            # Show preview dialog
            self.preview_dialog.show_preview_dialog(template_type, parameters)
            
        except ValueError as e:
            messagebox.showerror("Invalid Parameters", f"Please enter valid numeric values: {e}")
        except Exception as e:
            self.logger.error(f"Error previewing template: {e}")
            messagebox.showerror("Error", f"Failed to preview template: {e}")
    
    def create_template(self):
        """Create a new template."""
        messagebox.showinfo("Create Template", "Template creation functionality coming soon!")
    
    def import_template(self):
        """Import a template from file."""
        file_path = filedialog.askopenfilename(
            title="Import Template",
            filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*")]
        )
        if file_path:
            messagebox.showinfo("Import", f"Importing template from {file_path}")
    
    def install_selected_template(self):
        """Install the selected template to the device."""
        selection = self.template_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a template to install.")
            return
        messagebox.showinfo("Install", "Template installation functionality coming soon!")
    
    def export_template(self):
        """Export the selected template."""
        selection = self.template_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a template to export.")
            return
        messagebox.showinfo("Export", "Template export functionality coming soon!")
    
    def delete_template(self):
        """Delete the selected template."""
        selection = self.template_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a template to delete.")
            return
        messagebox.showinfo("Delete", "Template deletion functionality coming soon!")
    
    def browse_backup_dir(self):
        """Browse for backup directory."""
        directory = filedialog.askdirectory(
            title="Select Backup Directory",
            initialdir=self.backup_dir_var.get()
        )
        if directory:
            self.backup_dir_var.set(directory)