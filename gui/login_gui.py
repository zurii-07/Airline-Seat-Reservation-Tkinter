import tkinter as tk
from tkinter import messagebox
from backend import user_manager
from PIL import Image, ImageTk
import os
import glob

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Airline Reservation Login")
        self.root.state("zoomed")
        self.root.update_idletasks()

        self.bg_images = self.load_images()
        self.bg_index = 0

        # === Canvas ===
        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.bg_label = self.canvas.create_image(0, 0, anchor="nw")
        self.update_background()  # Start slideshow

        # === Entry widgets ===
        self.username_entry = tk.Entry(root)
        self.password_entry = tk.Entry(root, show="*")

        self.canvas.create_window(700, 250, window=tk.Label(root, text="Username:", font=("Arial", 12, "bold")))
        self.canvas.create_window(850, 250, window=self.username_entry)
        self.canvas.create_window(700, 290, window=tk.Label(root, text="Password:", font=("Arial", 12, "bold")))
        self.canvas.create_window(850, 290, window=self.password_entry)

        # === Buttons ===
        self.canvas.create_window(770, 350, window=tk.Button(root, text="Login", width=10, command=self.login))
        self.canvas.create_window(870, 350, window=tk.Button(root, text="Register", width=10, command=self.open_registration))

    def load_images(self):
        assets_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
        image_files = glob.glob(os.path.join(assets_dir, '*.jpg'))
        return image_files

    def update_background(self):
        if not self.bg_images:
            return

        # Load and resize current image
        image_path = self.bg_images[self.bg_index]
        img = Image.open(image_path)

        # Get current window size for dynamic fit
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        img = img.resize((width, height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(img)

        # Update canvas background
        self.canvas.itemconfig(self.bg_label, image=self.bg_photo)
        self.canvas.tag_lower(self.bg_label)  # Ensure background is behind widgets

        # Prepare next image
        self.bg_index = (self.bg_index + 1) % len(self.bg_images)

        # Loop every 2 seconds
        self.root.after(2000, self.update_background)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if user_manager.authenticate_user(username, password):
            messagebox.showinfo("Login Successful", f"Welcome {username}!")
            self.root.destroy()
            # Launch next screen
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    def open_registration(self):
        reg_window = tk.Toplevel(self.root)
        reg_window.title("Register New User")
        reg_window.geometry("400x250")

        tk.Label(reg_window, text="Username:").grid(row=0, column=0, pady=5)
        tk.Label(reg_window, text="Password:").grid(row=1, column=0, pady=5)
        tk.Label(reg_window, text="Full Name:").grid(row=2, column=0, pady=5)
        tk.Label(reg_window, text="Email:").grid(row=3, column=0, pady=5)

        username_entry = tk.Entry(reg_window)
        password_entry = tk.Entry(reg_window, show="*")
        fullname_entry = tk.Entry(reg_window)
        email_entry = tk.Entry(reg_window)

        username_entry.grid(row=0, column=1)
        password_entry.grid(row=1, column=1)
        fullname_entry.grid(row=2, column=1)
        email_entry.grid(row=3, column=1)

        def register():
            username = username_entry.get()
            password = password_entry.get()
            fullname = fullname_entry.get()
            email = email_entry.get()
            success, message = user_manager.register_user(username, password, fullname, email)
            if success:
                messagebox.showinfo("Registration", message)
                reg_window.destroy()
            else:
                messagebox.showerror("Registration Failed", message)

        tk.Button(reg_window, text="Register", command=register).grid(row=4, column=0, columnspan=2, pady=10)
