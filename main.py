import tkinter as tk
from gui.login_gui import LoginWindow
from gui.flight_selection_gui import App # This manages both selection + seat map

def launch_main_app():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    root = tk.Tk()

    def on_login_success():
        launch_main_app()  # ✅ Clean hand-off

    login = LoginWindow(root, on_login_success)
    root.mainloop()

def run_login_again():
    root = tk.Tk()
    login = LoginWindow(root, on_login_success)
    root.mainloop()

