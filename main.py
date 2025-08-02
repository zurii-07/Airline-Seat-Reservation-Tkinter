# import tkinter as tk
# from gui.login_gui import LoginWindow
#
# #Launcher for Login GUI;
# if __name__ == '__main__':
#     root = tk.Tk()
#     app = LoginWindow(root)
#     root.mainloop()

import tkinter as tk
from gui.login_gui import LoginWindow
from gui.flight_selection_gui import App  # This manages both selection + seat map

def launch_main_app():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    root = tk.Tk()

    def on_login_success():
        root.destroy()           # Close login window
        launch_main_app()        # Launch flight selection app

    login = LoginWindow(root, on_login_success)
    root.mainloop()
