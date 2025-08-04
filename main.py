import tkinter as tk
from gui.login_gui import LoginWindow
from gui.flight_selection_gui import App

def launch_main_app(username):
    app = App(current_user=username)
    app.mainloop()

def run_login_again():
    root = tk.Tk()
    user_data = {}

    def on_login_success(username):
        user_data['username'] = username
        root.quit()  # ✅ ONLY quit the loop, no destroy

    login = LoginWindow(root, on_login_success)
    root.mainloop()

    # DO NOT destroy again — already destroyed inside login_gui
    if 'username' in user_data:
        launch_main_app(user_data['username'])


if __name__ == '__main__':
    run_login_again()
