"""
Mock tkinter module for testing environments where tkinter is not available.
"""

# Mock tkinter classes for testing
class Tk:
    def __init__(self):
        self.title = lambda x: None
        self.geometry = lambda x: None
        self.minsize = lambda x, y: None
        self.mainloop = lambda: None
        self.columnconfigure = lambda x, **kwargs: None
        self.rowconfigure = lambda x, **kwargs: None
        self.after = lambda x, y: None
        self.update = lambda: None

class Toplevel(Tk):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

class Frame:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.grid = lambda **kwargs: None
        self.columnconfigure = lambda x, **kwargs: None
        self.rowconfigure = lambda x, **kwargs: None

class LabelFrame(Frame):
    def __init__(self, parent, text=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.text = text

class Label:
    def __init__(self, parent, text=None, textvariable=None, **kwargs):
        self.parent = parent
        self.text = text
        self.textvariable = textvariable
        self.grid = lambda **kwargs: None

class Button:
    def __init__(self, parent, text=None, command=None, **kwargs):
        self.parent = parent
        self.text = text
        self.command = command
        self.grid = lambda **kwargs: None

class Entry:
    def __init__(self, parent, textvariable=None, **kwargs):
        self.parent = parent
        self.textvariable = textvariable
        self.grid = lambda **kwargs: None

class Combobox:
    def __init__(self, parent, textvariable=None, values=None, state=None, **kwargs):
        self.parent = parent
        self.textvariable = textvariable
        self.values = values or []
        self.state = state
        self.grid = lambda **kwargs: None
        self.bind = lambda event, func: None

class Treeview:
    def __init__(self, parent, columns=None, show=None, **kwargs):
        self.parent = parent
        self.columns = columns or []
        self.show = show
        self.grid = lambda **kwargs: None
        self.heading = lambda col, text=None: None
        self.column = lambda col, **kwargs: None
        self.selection = lambda: []
        self.configure = lambda **kwargs: None

class Scrollbar:
    def __init__(self, parent, orient=None, command=None, **kwargs):
        self.parent = parent
        self.orient = orient
        self.command = command
        self.grid = lambda **kwargs: None

class Notebook:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.grid = lambda **kwargs: None
        self.add = lambda child, text=None: None

class Text:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.grid = lambda **kwargs: None
        self.delete = lambda start, end: None
        self.insert = lambda pos, text: None
        self.configure = lambda **kwargs: None

class Canvas:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.grid = lambda **kwargs: None
        self.delete = lambda tag: None
        self.create_rectangle = lambda *args, **kwargs: None
        self.create_line = lambda *args, **kwargs: None
        self.create_text = lambda *args, **kwargs: None
        self.create_oval = lambda *args, **kwargs: None
        self.configure = lambda **kwargs: None
        self.bind = lambda event, func: None
        self.bbox = lambda tag: (0, 0, 100, 100)
        self.winfo_width = lambda: 400
        self.winfo_height = lambda: 300

# StringVar and other variables
class StringVar:
    def __init__(self, value=""):
        self._value = value
    
    def get(self):
        return self._value
    
    def set(self, value):
        self._value = value

class BooleanVar:
    def __init__(self, value=False):
        self._value = value
    
    def get(self):
        return self._value
    
    def set(self, value):
        self._value = value

# Constants
W = "w"
E = "e"
N = "n"
S = "s"
WEST = "w"
EAST = "e"
NORTH = "n"
SOUTH = "s"
SUNKEN = "sunken"
RAISED = "raised"
VERTICAL = "vertical"
HORIZONTAL = "horizontal"
WORD = "word"
CHAR = "char"
END = "end"
LEFT = "left"
RIGHT = "right"
TOP = "top"
BOTTOM = "bottom"

# Style
class Style:
    def __init__(self):
        pass
    
    def theme_use(self, theme):
        pass
    
    def configure(self, style, **kwargs):
        pass

# ttk module
class ttk:
    Frame = Frame
    LabelFrame = LabelFrame
    Label = Label
    Button = Button
    Entry = Entry
    Combobox = Combobox
    Treeview = Treeview
    Scrollbar = Scrollbar
    Notebook = Notebook
    Style = Style

# messagebox
class messagebox:
    @staticmethod
    def showinfo(title, message):
        print(f"INFO: {title} - {message}")
    
    @staticmethod
    def showwarning(title, message):
        print(f"WARNING: {title} - {message}")
    
    @staticmethod
    def showerror(title, message):
        print(f"ERROR: {title} - {message}")
    
    @staticmethod
    def askyesno(title, message):
        print(f"YES/NO: {title} - {message}")
        return True

# filedialog
class filedialog:
    @staticmethod
    def askopenfilename(**kwargs):
        print(f"OPEN FILE: {kwargs}")
        return ""
    
    @staticmethod
    def asksaveasfilename(**kwargs):
        print(f"SAVE FILE: {kwargs}")
        return ""
    
    @staticmethod
    def askdirectory(**kwargs):
        print(f"SELECT DIRECTORY: {kwargs}")
        return ""