import tkinter as tk
import tkinter.ttk as ttk
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
        # === Fonts ===
        font_title = ("Segoe UI", 24, "bold")
        font_label = ("Segoe UI", 12)
        font_button = ("Segoe UI", 10, "bold")

        # === Center Point ===
        center_x = self.root.winfo_screenwidth() // 2

        # === Title Label ===
        self.canvas.create_text(center_x, 100, text="Welcome to FlightForge Airline Seat Reservations",
                                font=font_title, fill="white")

        # === Entries & Labels Centered ===
        # === Fonts ===
        font_title = ("Segoe UI", 24, "bold")
        font_label = ("Segoe UI", 12)
        font_button = ("Segoe UI", 10, "bold")

        # === Center Position ===
        self.root.update_idletasks()
        center_x = self.root.winfo_screenwidth() // 2
        center_y = self.root.winfo_screenheight() // 2

        # === Title ===
        # self.canvas.create_text(center_x, center_y - 150,
        #                         text="✈️ Welcome to FlightForge Airline Seat Reservations",
        #                         font=font_title, fill="white")

        # === Entry Fields ===
        self.username_entry = tk.Entry(root, font=font_label, width=30)
        self.password_entry = tk.Entry(root, show="*", font=font_label, width=30)

        self.canvas.create_text(center_x - 120, center_y - 60,
                                text="Username:", font=font_label, fill="white", anchor="e")
        self.canvas.create_window(center_x + 10, center_y - 60,
                                  window=self.username_entry, anchor="w")

        self.canvas.create_text(center_x - 120, center_y - 20,
                                text="Password:", font=font_label, fill="white", anchor="e")
        self.canvas.create_window(center_x + 10, center_y - 20,
                                  window=self.password_entry, anchor="w")

        # === Buttons ===
        btn_login = tk.Button(root, text="Login", font=font_button, width=12,
                              command=self.login, bg="#2E86C1", fg="white")
        btn_register = tk.Button(root, text="Register", font=font_button, width=12,
                                 command=self.open_registration, bg="#117A65", fg="white")

        self.canvas.create_window(center_x - 50, center_y + 40, window=btn_login)
        self.canvas.create_window(center_x + 70, center_y + 40, window=btn_register)

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
        self.root.after(4000, self.update_background)

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
