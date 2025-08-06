import tkinter as tk
from tkinter import ttk, messagebox
from backend.flight_data import generate_flights
from PIL import Image, ImageTk
import os
from backend.seat_manager import user_bookings

# GUI Frame for flight selection, with background image,
# origin/destination selection, available flights list,
# and a side panel showing user's bookings.

class FlightSelectionFrame(tk.Frame):
    def __init__(self, master, on_continue, on_back, current_user):
        super().__init__(master)
        self.master = master
        self.on_continue = on_continue # Callback to move to seat map
        self.on_back = on_back # Callback to return to login or previous page
        self.current_user = current_user
        self.pack(fill='both', expand=True)
        self.master.state("zoomed") # Start the window maximized

        self.flights = generate_flights(days_ahead=7) # Load upcoming 7 days of flights

        # Background image
        bg_path = os.path.join(os.path.dirname(__file__), '..', 'assets 2', 'FlightSelection.jpg')
        img = Image.open(bg_path)
        img = img.resize((self.master.winfo_screenwidth(), self.master.winfo_screenheight()), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(img)
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Main content container
        container = tk.Frame(self, bg="#ffffff", bd=2, relief="ridge")
        container.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(container, text="Select Your Flight", font=("Segoe UI", 18, "bold")).pack(pady=(20, 10))

        # Origin Country Selection
        ttk.Label(container, text="Origin Country:").pack(pady=(10, 0))
        self.origin_var = tk.StringVar()
        self.origin_combo = ttk.Combobox(container, textvariable=self.origin_var, width=50, state="readonly")
        self.origin_combo['values'] = sorted({f['origin_country'] for f in self.flights})
        self.origin_combo.pack()

        # Destination Country Selection
        ttk.Label(container, text="Destination Country:").pack(pady=(10, 0))
        self.dest_var = tk.StringVar()
        self.dest_combo = ttk.Combobox(container, textvariable=self.dest_var, width=50, state="readonly")
        self.dest_combo.pack()

        # Listbox to display available flights based on origin & destination
        self.listbox = tk.Listbox(container, width=80, height=10)
        self.listbox.pack(pady=20)

        #Continue button to proceed to seat selection
        ttk.Button(container, text="Continue", command=self.continue_pressed).pack(pady=(0, 10))

        #Back button in top-left
        ttk.Button(self, text="<--Back", command=self.on_back).place(x=10, y=10)

        #Bind dropdown selection changes to update destination and flights
        self.origin_combo.bind("<<ComboboxSelected>>", self.update_destinations)
        self.dest_combo.bind("<<ComboboxSelected>>", self.update_flights)

        #Side panel for user bookings
        panel = tk.Frame(self, bg="#f9f9f9", bd=1, relief="solid")
        panel.place(relx=0.85, rely=0.3, width=260, height=300, anchor="center")
        tk.Label(panel, text="Your Bookings", font=("Segoe UI", 12, "bold"), bg=panel["bg"]).pack(pady=5)
        self.booking_list = tk.Listbox(panel, width=30, height=12)
        self.booking_list.pack(padx=10, pady=5)

        #Load and display bookings made by the current user
        for bk in user_bookings(self.current_user):
            entry = f"{bk['flight_id']} Seat:{bk['seat']} {bk['name']}"
            self.booking_list.insert(tk.END, f"{bk['flight_id']} | Seat:{bk['seat']} | {bk['name']}")

        #Exit button
        exit_btn = tk.Button(self, text="Exit", bg="#d9534f", fg="white", font=("Segoe UI", 10, "bold"),
                             command=self.master.quit)
        exit_btn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

    #Update destination dropdown based on selected origin
    def update_destinations(self, event=None):
        origin = self.origin_var.get()
        dests = sorted({f['dest_country'] for f in self.flights if f['origin_country'] == origin})
        self.dest_combo['values'] = dests
        self.dest_var.set('')
        self.listbox.delete(0, tk.END)

    #Update list of available flights based on selected origin and destination
    def update_flights(self, event=None):
        origin = self.origin_var.get()
        dest = self.dest_var.get()
        self.listbox.delete(0, tk.END)
        for f in self.flights:
            if f['origin_country'] == origin and f['dest_country'] == dest:
                info = f"{f['flight_id']} | {f['date']} {f['time']} | {f['origin_airport']} → {f['dest_airport']}"
                self.listbox.insert(tk.END, info)

    #Handle the continue button click
    def continue_pressed(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a flight.")
            return
        selected_line = self.listbox.get(sel[0])

        #Find the full flight object from the flight list
        flight_id = selected_line.split(" | ")[0]
        flight = next(f for f in self.flights if f['flight_id'] == flight_id)
        self.on_continue(flight, self.current_user)


# Main Application Class (Window Manager)
# Controls switching between frames (flight selection --> seat map)
class App(tk.Tk):
    def __init__(self, current_user):
        super().__init__()
        self.title("Flight Booking System")
        self.geometry("1200x800")
        self.resizable(False, False)
        self.current_user = current_user
        self.current_frame = None
        self.show_selection() #Start with flight selection

    #Show the flight selection frame
    def show_selection(self):
        self.clear_frame()
        self.current_frame = FlightSelectionFrame(self, on_continue=self.show_seatmap,
                                                  on_back=self.restart_login,
                                                  current_user=self.current_user)

    #Show the seat map frame for a selected flight
    def show_seatmap(self, flight, current_user):
        from gui.seat_map_gui import SeatMapFrame #Import here to avoid circular imports
        self.clear_frame()
        self.current_frame = SeatMapFrame(self, flight, on_back=self.show_selection, current_user=current_user)

    #Destroy the current frame before switching to another
    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    #Restart login window (go back to login GUI)
    def restart_login(self):
        self.destroy() #Close current window
        import main
        main.run_login_again() #Relaunch the login window


