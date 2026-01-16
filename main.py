import tkinter as tk
from gui.login_gui import LoginWindow #Import the custom login GUI
from gui.flight_selection_gui import App #Main app GUI after login

#Function: launch_main_app
#Launches the main App window with the logged-in user.
def launch_main_app(username):
    app = App(current_user=username) #Pass username to main App
    app.mainloop() #Start the main event loop

#Function: run_login_again
#Launches the login window first.
#If login succeeds, it launches the main app.
def run_login_again():
    root = tk.Tk() #Initialize root window for login
    user_data = {} #Placeholder to store logged-in username

    #Callback passed to login window to handle success
    def on_login_success(username):
        user_data['username'] = username
        root.quit()  #only to quit the loop, no destroy

    login = LoginWindow(root, on_login_success) #Launch login UI
    root.mainloop() #Wait for login action

    if 'username' in user_data:
        launch_main_app(user_data['username'])

#Entry Point
if __name__ == '__main__':
    run_login_again() #Start the login process when the script runs
