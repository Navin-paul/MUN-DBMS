import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import webbrowser
import os
import sys
from pathlib import Path

def ensure_pil_installed():
    try:
        import PIL
    except ImportError:
        print("PIL not found. Installing Pillow...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
            print("Pillow installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error installing Pillow: {e}")
            messagebox.showerror("Error", "Failed to install required package (Pillow). Please install it manually using: pip install Pillow")
            sys.exit(1)

# Ensure PIL is installed before importing
ensure_pil_installed()

# Now we can safely import PIL
try:
    from PIL import Image, ImageTk
except ImportError:
    messagebox.showerror("Error", "Failed to import PIL module even after installation.")
    sys.exit(1)
from PIL import Image, ImageTk  # Add PIL imports

class AdminInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("MUN-DBMS Admin Interface")
        self.root.geometry("1024x768")  # Increased size for better layout
        self.root.configure(bg="#2C3E50")

        # Load and display the background image
        try:
            # Create a canvas for the background
            self.canvas = tk.Canvas(root, width=1024, height=768, highlightthickness=0)
            self.canvas.pack(fill="both", expand=True)
            
            # Get current script directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            print(f"Current directory: {current_dir}")
            
            # Check static folder
            static_dir = os.path.join(current_dir, "static")
            print(f"Static directory: {static_dir}")
            print(f"Static directory exists: {os.path.exists(static_dir)}")
            
            # Try to load the image
            image_path = os.path.join(static_dir, "un_logo.png")
            print(f"Looking for image at: {image_path}")
            print(f"Image file exists: {os.path.exists(image_path)}")
            
            if os.path.exists(image_path):
                try:
                    print("Attempting to load image...")
                    # Use PIL to open and convert the image
                    image = Image.open(image_path)
                    self.bg_image = ImageTk.PhotoImage(image)
                    self.canvas.create_image(512, 384, image=self.bg_image, anchor="center")
                    print("Image loaded successfully!")
                except Exception as img_error:
                    print(f"Error loading image: {img_error}")
                    self.draw_default_symbol()
            else:
                print("Image not found, drawing default symbol")
                self.draw_default_symbol()
            
            # No overlay needed
                                      
            # Create and add buttons
            self.create_buttons()
        except Exception as e:
            print(f"Error setting up canvas: {e}")
            self.root.configure(bg="#2C3E50")  # Fallback to solid color

    def draw_default_symbol(self):
        """Draw a default UN-like symbol on the canvas"""
        # Main circles (UN emblem)
        self.canvas.create_oval(412, 284, 612, 484, outline="#ECF0F1", width=3)
        self.canvas.create_oval(437, 309, 587, 459, outline="#ECF0F1", width=3)
        
        # World map suggestion (simplified)
        self.canvas.create_arc(462, 334, 562, 434, 
                             start=0, extent=180, 
                             outline="#ECF0F1", width=2,
                             style=tk.ARC)
        
        # Olive branches (simplified)
        branch_color = "#2ECC71"  # Green color for branches
        # Left branch
        self.canvas.create_arc(362, 334, 462, 434, 
                             start=45, extent=180, 
                             outline=branch_color, width=2)
        # Right branch
        self.canvas.create_arc(562, 334, 662, 434, 
                             start=-45, extent=180, 
                             outline=branch_color, width=2)
        
        # Create and add buttons after drawing the symbol
        self.create_buttons()

    def create_buttons(self):
        """Create and set up all buttons"""
        # Create title directly on canvas
        self.canvas.create_text(512, 70,  # Moved higher up
                              text="MUN-DBMS Admin Dashboard",
                              font=("Helvetica", 24, "bold"),
                              fill="#FFFFFF")

        # Create buttons container (fully transparent)
        button_frame = tk.Frame(self.canvas, bg='', highlightthickness=0)
        self.canvas.create_window(512, 384, window=button_frame, anchor="center")

        # Button configurations with the blue color scheme
        buttons = [
            ("Update Delegates", self.update_delegates, "#00FFC8"),
            ("Calculate Points", self.calculate_points, "#00EEFF"),
            ("Allot Delegates", self.allot_delegates, "#00A2FF"),
            ("Registration Page", self.open_registration, "#0059FF")
        ]

        for text, command, color in buttons:
            # Create button directly in the button frame
            btn_frame = tk.Frame(button_frame, bg='', highlightthickness=0)
            btn_frame.pack(pady=2)  # Reduced padding between buttons
            
            # Create glass effect background (transparent)
            glass = tk.Frame(btn_frame, 
                           bg=self.adjust_color(color, -20),
                           width=240,
                           height=60)
            glass.place(x=2, y=2)
            
            # Create button
            btn = tk.Button(btn_frame,
                          text=text,
                          command=command,
                          font=("Helvetica", 14, "bold"),
                          fg="white",
                          bg=color,
                          activebackground=self.adjust_color(color, -20),
                          activeforeground="white",
                          width=20,
                          height=2,
                          relief=tk.RAISED,
                          bd=3)
            btn.pack()
            
            # Enhanced hover effects
            btn.bind("<Enter>", lambda e, b=btn, c=color, g=glass: self.on_hover(b, c, g))
            btn.bind("<Leave>", lambda e, b=btn, c=color, g=glass: self.on_leave(b, c, g))

    def adjust_color(self, color, amount):
        """Adjust color brightness"""
        import colorsys
        # Convert hex to RGB
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        # Convert RGB to HSV
        hsv = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        # Adjust brightness
        rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], max(0, min(1, hsv[2] + amount/100)))
        # Convert back to hex
        return f"#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}"

    def on_hover(self, button, color, glass):
        """Enhanced mouse hover effect"""
        hover_color = self.adjust_color(color, 10)
        button.configure(bg=hover_color)
        glass.configure(bg=hover_color)

    def on_leave(self, button, color, glass):
        """Enhanced mouse leave effect"""
        button.configure(bg=color)
        glass.configure(bg=color)

    def show_success(self, message):
        """Show success popup"""
        messagebox.showinfo("Success", message)

    def show_error(self, message):
        """Show error popup"""
        messagebox.showerror("Error", message)

    def run_python_script(self, script_path):
        """Run a Python script and handle errors"""
        try:
            # Get the directory of the script to run
            script_dir = os.path.dirname(script_path)
            
            # Get Python executable path
            python_exe = sys.executable if hasattr(sys, 'executable') else 'python'
            
            # Set environment variables for proper encoding
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            env['PYTHONLEGACYWINDOWSSTDIO'] = '1'  # Fix for Windows encoding
            
            startupinfo = None
            if os.name == 'nt':  # If on Windows
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            # Run the script with proper working directory and encoding
            cmd = [python_exe, '-X', 'utf8', str(script_path)]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                cwd=script_dir,
                env=env,
                encoding='utf-8',
                errors='replace',  # Handle any encoding errors by replacing invalid characters
                startupinfo=startupinfo
            )
            
            if result.stderr:
                print(f"Script warnings/errors: {result.stderr}")
            if result.stdout:
                print(f"Script output: {result.stdout}")
                
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else str(e)
            print(f"Script error output: {error_msg}")
            return False, error_msg
        except Exception as e:
            print(f"Exception running script: {str(e)}")
            return False, str(e)

    def get_absolute_path(self, relative_path):
        """Get absolute path from relative path"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, relative_path)

    def update_delegates(self):
        """Handle Update Delegates button click"""
        script_path = Path(self.get_absolute_path("del_transfer/insert_data.py"))
        print(f"Attempting to run: {script_path}")
        if script_path.exists():
            print(f"Running with cwd: {script_path.parent}")
            success, output = self.run_python_script(str(script_path))
            if success:
                self.show_success("Successfully updated delegates data!")
            else:
                self.show_error(f"Error updating delegates: {output}")
        else:
            self.show_error(f"File not found: {script_path}")

    def calculate_points(self):
        """Handle Calculate Points button click"""
        try:
            # Handle paths with spaces using Path objects
            script1_path = Path(self.get_absolute_path("Point system/point_sort.py"))
            script2_path = Path(self.get_absolute_path("Point system/Point_sys.py"))
            
            print(f"Attempting to run: {script1_path}")
            print(f"Attempting to run: {script2_path}")
            
            if not script1_path.exists():
                self.show_error(f"File not found: {script1_path}")
                return
            if not script2_path.exists():
                self.show_error(f"File not found: {script2_path}")
                return
                
            success1, output1 = self.run_python_script(str(script1_path))
            if success1:
                success2, output2 = self.run_python_script(str(script2_path))
                if success1 and success2:
                    self.show_success("Successfully calculated points!")
                else:
                    error_msg = output2
                    self.show_error(f"Error calculating points: {error_msg}")
            else:
                self.show_error(f"Error calculating points: {output1}")
        except Exception as e:
            self.show_error(f"Error: {str(e)}")

    def allot_delegates(self):
        """Handle Allot Delegates button click"""
        script_path = Path(self.get_absolute_path("allotment_alg.py"))
        print(f"Attempting to run: {script_path}")
        if script_path.exists():
            success, output = self.run_python_script(str(script_path))
            if success:
                self.show_success("Successfully allotted delegates!")
            else:
                self.show_error(f"Error allotting delegates: {output}")
        else:
            self.show_error(f"File not found: {script_path}")

    def open_registration(self):
        """Handle Registration Page button click"""
        try:
            file_path = Path(self.get_absolute_path("templates/MAIN(1).html"))
            print(f"Attempting to open: {file_path}")
            if file_path.exists():
                webbrowser.open(f'file://{file_path}')
                self.show_success("Registration page opened successfully!")
            else:
                self.show_error(f"File not found: {file_path}")
        except Exception as e:
            self.show_error(f"Error opening registration page: {str(e)}")

def main():
    root = tk.Tk()
    app = AdminInterface(root)
    # Center the window on the screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'+{x}+{y}')
    root.mainloop()

if __name__ == "__main__":
    main()