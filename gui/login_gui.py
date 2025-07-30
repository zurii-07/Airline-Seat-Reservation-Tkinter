import tkinter as tk #Importing python GUI toolkit
from tkinter import messagebox #for pop-up dialogs
from backend import user_manager #connecting to functions from the backend

class LoginWindow: #When launched, passed to the Tk window.
    def __init__(self, root):
        self.root = root
        self.root.title("Airline Reservation Login") #window title

        #Labels & entry fields
        tk.Label(root, text="Username:").grid(row=0, column=0, pady=5)
        tk.Label(root, text="Password:").grid(row=1, column=0, pady=5)

        self.username_entry = tk.Entry(root)
        self.password_entry = tk.Entry(root, show="*")

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

        #Buttons to perform tasks
        tk.Button(root, text="Login", command=self.login).grid(row=2, column=0, pady=10)
        tk.Button(root, text="Register", command=self.open_registration).grid(row=2, column=1, pady=10)

    #Method for login
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if user_manager.authenticate_user(username, password):
            messagebox.showinfo("Login Successful", f"Welcome {username}!")
            self.root.destroy()  # Closes login window
            # Here load the next window (flight selection)
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    #Method for registration
    def open_registration(self):
        reg_window = tk.Toplevel(self.root)
        reg_window.title("Register New User")

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

        #Inner function for registration
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

