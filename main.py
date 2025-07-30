import tkinter as tk
from gui.login_gui import LoginWindow

#Launcher for Login GUI;
if __name__ == '__main__':
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()