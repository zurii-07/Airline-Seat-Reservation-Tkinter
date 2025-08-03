import tkinter as tk
from gui.login_gui import LoginWindow
from gui.flight_selection_gui import App

def launch_main_app():
    app = App()
    app.mainloop()

def run_login_again():
    root = tk.Tk()

    def on_login_success():
        launch_main_app()

    login = LoginWindow(root, on_login_success)
    root.mainloop()

if __name__ == '__main__':
    run_login_again()
