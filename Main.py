'''
First - Import tkinter to py file
Second - Add functions to add & delete tasks
Third - Make the main window with size and title
Fourth - Add widgets like add/delete tasks button, listbox & display box for tasks
Fifth - Add a file saving functionality to save tasks to a file to load later
Sixth - Mark off and delete tasks once finish !
'''

# Import necessary modules from tkinter and pathlib
import tkinter as tk  # Import tkinter module for GUI
from tkinter import ttk, messagebox  # Import themed tkinter widgets and messagebox
from pathlib import Path  # Import Path for file path operations

# Define the main application class
class TodoApp:
    # Initialize the application
    def __init__(self, root):
        self.root = root  # Store the root window
        self.root.withdraw()  # Hide main window initially to show instructions first
        
        # Set up save file path on desktop
        desktop_path = Path.home() / "Desktop"  # Get user's desktop path
        self.SAVE_FILE = desktop_path / "TO-DO TASKS!.txt"  # Create save file path
        
        # Setup styles for the application
        self.setup_styles()
        
        # Show instructions window first
        self.show_instructions()

    # Function to display instructions window
    def show_instructions(self):
        # Create a new top-level window for instructions
        self.instruction_window = tk.Toplevel(self.root)
        self.instruction_window.title("How to Use!")  # Set window title
        self.instruction_window.geometry("500x400")  # Set window size
        self.instruction_window.resizable(False, False)  # Make window non-resizable
        
        # Make it modal (must be closed before continuing)
        self.instruction_window.grab_set()
        
        # Bind the close button to start the main app
        self.instruction_window.protocol("WM_DELETE_WINDOW", self.start_main_app)
        
        # Create main container frame
        container = ttk.Frame(self.instruction_window)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create header label
        header = ttk.Label(
            container,
            text="Welcome!",  # Header text
            font=("Arial", 14, "bold"),  # Font styling
            justify=tk.CENTER  # Center alignment
        )
        header.pack(pady=(0, 10))  # Add padding
        
        # Create frame for instruction text with scrollbar
        text_frame = ttk.Frame(container)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create text widget for instructions
        instructions = tk.Text(
            text_frame,
            wrap=tk.WORD,  # Word wrapping
            font=("Arial", 11),  # Font
            padx=10,  # Horizontal padding
            pady=10,  # Vertical padding
            relief=tk.FLAT,  # No border
            yscrollcommand=scrollbar.set  # Connect to scrollbar
        )
        instructions.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=instructions.yview)  # Connect scrollbar to text widget
        
        # Instruction content
        content = """Here's how to use it:

1. ADDING TASKS:
   - Type your task in the text box
   - Select a priority (High, Medium, Low)
   - Click "Add Task"

2. COMPLETING TASKS:
   - Check the box next to tasks you've completed
   - Click "Delete Selected" to remove them

3. PRIORITY COLORS:
   - High priority: Red background
   - Medium priority: Yellow background
   - Low priority: Green background

Your tasks are automatically saved to your desktop and will still be here when you reopen the app!
--Press the "X" button to start using the app!--"""
        
        # Insert content into text widget
        instructions.insert(tk.END, content)
        instructions.config(state=tk.DISABLED)  # Make it read-only

    # Function to start the main application
    def start_main_app(self):
        # Close instruction window if it exists
        if hasattr(self, 'instruction_window') and self.instruction_window:
            self.instruction_window.destroy()
        
        # Show the main window
        self.root.deiconify()
        self.root.title("To-Do List :D")  # Set window title
        self.root.geometry("600x500")  # Set window size
        
        # Create all widgets
        self.create_widgets()
        
        # Load saved tasks from file
        self.load_tasks()

    # Function to setup styles for the application
    def setup_styles(self):
        style = ttk.Style()  # Create style object
        # Configure styles for different priority levels
        style.configure("High.TFrame", background="#ffdddd")  # Reddish
        style.configure("Medium.TFrame", background="#ffffdd")  # Yellowish
        style.configure("Low.TFrame", background="#ddffdd")  # Greenish
        style.configure("High.TLabel", background="#ffdddd")
        style.configure("Medium.TLabel", background="#ffffdd")
        style.configure("Low.TLabel", background="#ddffdd")

    # Function to create all widgets in the main window
    def create_widgets(self):
        # Create frame for task entry
        entry_frame = ttk.Frame(self.root, padding="10")
        entry_frame.pack(fill=tk.X)  # Fill horizontally
        
        # Create task entry field
        self.task_entry = ttk.Entry(entry_frame, width=40, font=("Arial", 12))
        self.task_entry.pack(side=tk.LEFT, padx=5)
        
        # Create priority selection dropdown
        self.priority_var = tk.StringVar(value="Medium")  # Default value
        priorities = ["High", "Medium", "Low"]  # Priority options
        self.priority_menu = ttk.OptionMenu(entry_frame, self.priority_var, *priorities)
        self.priority_menu.pack(side=tk.LEFT, padx=5)
        
        # Create add task button
        add_btn = ttk.Button(entry_frame, text="Add Task", command=self.add_task)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Create frame for task list
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create scrollbar for task list
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create canvas for scrolling
        self.canvas = tk.Canvas(list_frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.canvas.yview)  # Connect scrollbar to canvas
        
        # Create frame inside canvas for tasks
        self.task_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.task_frame, anchor=tk.NW)
        
        # Configure canvas scrolling
        self.task_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Create delete selected button
        delete_btn = ttk.Button(self.root, text="Delete Selected", command=self.delete_selected)
        delete_btn.pack(pady=10)
        
        # Bind window close event to save tasks
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # Function to add a new task
    def add_task(self):
        task_text = self.task_entry.get().strip()  # Get task text and remove whitespace
        if task_text:  # Only proceed if there's text
            priority = self.priority_var.get()  # Get selected priority
            
            # Create frame for the task with priority-based styling
            task_frame = ttk.Frame(self.task_frame, style=f"{priority}.TFrame")
            task_frame.pack(fill=tk.X, pady=2, padx=5)
            
            # Create checkbox for task completion
            var = tk.IntVar()  # Variable to track checkbox state
            chk = ttk.Checkbutton(task_frame, variable=var)
            chk.pack(side=tk.LEFT)
            
            # Create label for task text
            task_label = ttk.Label(
                task_frame, 
                text=task_text,  # Display task text
                style=f"{priority}.TLabel",  # Priority-based styling
                font=("Arial", 11),  # Font
                padding=5  # Padding around text
            )
            task_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Create label for priority
            priority_label = ttk.Label(
                task_frame, 
                text=priority,  # Display priority
                style=f"{priority}.TLabel",  # Priority-based styling
                font=("Arial", 10, "bold"),  # Bold font
                padding=5  # Padding
            )
            priority_label.pack(side=tk.RIGHT)
            
            # Store task data as attributes of the frame
            task_frame.var = var  # Checkbox variable
            task_frame.text = task_text  # Task text
            task_frame.priority = priority  # Task priority
            
            # Clear the entry field
            self.task_entry.delete(0, tk.END)
            
            # Save tasks to file
            self.save_tasks()

    # Function to delete selected tasks
    def delete_selected(self):
        # Loop through all task widgets
        for widget in self.task_frame.winfo_children():
            # Check if widget has a checkbox and if it's checked
            if hasattr(widget, "var") and widget.var.get() == 1:
                widget.destroy()  # Remove the task
        self.save_tasks()  # Save changes

    # Function to save tasks to file
    def save_tasks(self):
        tasks = []  # List to store tasks
        # Collect all tasks from the interface
        for widget in self.task_frame.winfo_children():
            if hasattr(widget, "text"):
                # Format as "task|priority"
                tasks.append(f"{widget.text}|{widget.priority}")
        
        try:
            # Write tasks to file
            with open(self.SAVE_FILE, "w") as f:
                f.write("\n".join(tasks))  # One task per line
        except Exception as e:
            # Show error if saving fails
            messagebox.showerror("Error", f"Failed to save tasks:\n{e}")

    # Function to load tasks from file
    def load_tasks(self):
        try:
            # Check if save file exists
            if self.SAVE_FILE.exists():
                # Read tasks from file
                with open(self.SAVE_FILE, "r") as f:
                    for line in f.readlines():
                        if "|" in line:  # Check for valid format
                            # Split into text and priority
                            text, priority = line.strip().split("|")
                            # Set UI elements and add task
                            self.priority_var.set(priority)
                            self.task_entry.insert(0, text)
                            self.add_task()
                            self.task_entry.delete(0, tk.END)  # Clear entry
        except Exception as e:
            # Show error if loading fails
            messagebox.showerror("Error", f"Failed to load tasks:\n{e}")

    # Function to handle window closing
    def on_closing(self):
        self.save_tasks()  # Save tasks before closing
        self.root.destroy()  # Close the application

# Main entry point
if __name__ == "__main__":
    root = tk.Tk()  # Create root window
    app = TodoApp(root)  # Create application instance
    root.mainloop()  # Start main event loop