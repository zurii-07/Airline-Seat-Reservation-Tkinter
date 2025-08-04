import tkinter as tk
from tkinter import messagebox
from backend import user_manager
from PIL import Image, ImageTk
import os
import glob

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Airline Reservation Login")
        self.root.state("zoomed")
        self.root.update_idletasks()

        self.bg_images = self.load_images()
        self.bg_index = 0
        self.bg_callback_id = None

        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.bg_label = self.canvas.create_image(0, 0, anchor="nw")
        self.update_background()

        font_title = ("Segoe UI", 24, "bold")
        font_label = ("Segoe UI", 13, "bold")
        font_button = ("Segoe UI", 11, "bold")

        center_x = self.root.winfo_screenwidth() // 2
        center_y = self.root.winfo_screenheight() // 2

        self.canvas.create_text(center_x, center_y - 150,
                                text="Welcome to FlightForge Airline Seat Reservations",
                                font=font_title, fill="white")

        # === Username Field with Label Background ===
        self.canvas.create_rectangle(center_x - 200, center_y - 65,
                                     center_x - 50, center_y - 35,
                                     fill="white", outline="")
        self.username_entry = tk.Entry(root, font=font_label, width=28)
        self.canvas.create_text(center_x - 120, center_y - 50,
                                text="Username:", font=font_label, fill="#000000", anchor="e")
        self.canvas.create_window(center_x + 10, center_y - 50,
                                  window=self.username_entry, anchor="w")

        # === Password Field with Label Background ===
        self.canvas.create_rectangle(center_x - 200, center_y - 25,
                                     center_x - 50, center_y + 5,
                                     fill="white", outline="")
        self.password_entry = tk.Entry(root, show="*", font=font_label, width=28)
        self.canvas.create_text(center_x - 120, center_y - 10,
                                text="Password:", font=font_label, fill="#000000", anchor="e")
        self.canvas.create_window(center_x + 10, center_y - 10,
                                  window=self.password_entry, anchor="w")

        # === Buttons ===
        btn_login = tk.Button(root, text="Login", font=font_button, width=12,
                              command=self.login, bg="#2E86C1", fg="white")
        btn_register = tk.Button(root, text="Register", font=font_button, width=12,
                                 command=self.open_registration, bg="#117A65", fg="white")
        self.canvas.create_window(center_x - 60, center_y + 40, window=btn_login)
        self.canvas.create_window(center_x + 60, center_y + 40, window=btn_register)

    def load_images(self):
        assets_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
        return glob.glob(os.path.join(assets_dir, '*.jpg'))

    def update_background(self):
        if not self.bg_images:
            return
        image_path = self.bg_images[self.bg_index]
        img = Image.open(image_path)
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(img)
        self.canvas.itemconfig(self.bg_label, image=self.bg_photo)
        self.canvas.tag_lower(self.bg_label)

        self.bg_index = (self.bg_index + 1) % len(self.bg_images)
        self.bg_callback_id = self.canvas.after(4000, self.update_background)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Missing Fields", "Please enter both username and password.")
            return

        if user_manager.authenticate_user(username, password):
            messagebox.showinfo("Login Successful", f"Welcome {username}!")

            try:
                if self.bg_callback_id:
                    self.canvas.after_cancel(self.bg_callback_id)
            except Exception:
                pass

            self.root.quit()
            self.root.destroy()
            self.on_login_success(username)
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    def open_registration(self):
        reg_window = tk.Toplevel(self.root)
        reg_window.title("Register New User")
        reg_window.geometry("900x500")
        reg_window.resizable(False, False)

        bg_image_path = os.path.join(os.path.dirname(__file__), '..', 'assets 2', 'Shield.jpg')
        bg_img = Image.open(bg_image_path)
        bg_img = bg_img.resize((900, 500), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_img)

        bg_canvas = tk.Canvas(reg_window, width=900, height=500, highlightthickness=0)
        bg_canvas.pack(fill="both", expand=True)
        bg_canvas.create_image(0, 0, anchor="nw", image=bg_photo)
        reg_window.bg_photo = bg_photo

        font_label = ("Segoe UI", 13, "bold")
        font_entry = ("Segoe UI", 12)
        font_button = ("Segoe UI", 11, "bold")

        entry_width = 30
        label_color = "#ffffff"
        field_y_start = 120
        field_spacing = 50
        x_label = 240
        x_entry = 400

        def create_label(text, y):
            return bg_canvas.create_text(x_label, y, text=text, font=font_label, fill=label_color, anchor="e")

        def create_entry(y):
            entry = tk.Entry(reg_window, font=font_entry, width=entry_width, bd=2, relief="groove")
            bg_canvas.create_window(x_entry, y, window=entry, anchor="w")
            return entry

        create_label("Username:", field_y_start)
        username_entry = create_entry(field_y_start)

        create_label("Password:", field_y_start + field_spacing)
        password_entry = tk.Entry(reg_window, font=font_entry, show="*", width=entry_width, bd=2, relief="groove")
        bg_canvas.create_window(x_entry, field_y_start + field_spacing, window=password_entry, anchor="w")

        create_label("Full Name:", field_y_start + 2 * field_spacing)
        fullname_entry = create_entry(field_y_start + 2 * field_spacing)

        create_label("Email:", field_y_start + 3 * field_spacing)
        email_entry = create_entry(field_y_start + 3 * field_spacing)

        def register():
            username = username_entry.get()
            password = password_entry.get()
            fullname = fullname_entry.get()
            email = email_entry.get()

            if not all([username, password, fullname, email]):
                messagebox.showwarning("Missing Info", "All fields are required.")
                return

            success, message = user_manager.register_user(username, password, fullname, email)
            if success:
                messagebox.showinfo("Registration", message)
                reg_window.destroy()
            else:
                messagebox.showerror("Registration Failed", message)

        register_btn = tk.Button(reg_window, text="Register", font=font_button, width=15,
                                 command=register, bg="#28a745", fg="white", relief="flat", bd=0,
                                 highlightthickness=1, highlightbackground="#1e7e34", cursor="hand2")
        bg_canvas.create_window(x_entry + 60, field_y_start + 4 * field_spacing + 20,
                                window=register_btn, anchor="w")
