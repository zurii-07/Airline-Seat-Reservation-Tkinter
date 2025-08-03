import tkinter as tk
from tkinter import ttk, messagebox
from backend.flight_data import generate_flights
from PIL import Image, ImageTk
import os

class FlightSelectionFrame(tk.Frame):
    def __init__(self, master, on_continue, on_back):
        super().__init__(master)
        self.master = master
        self.on_continue = on_continue
        self.on_back = on_back
        self.pack(fill='both', expand=True)
        self.master.state("zoomed")

        self.flights = generate_flights(days_ahead=7)

        # === Load and set background image ===
        bg_path = os.path.join(os.path.dirname(__file__), '..', 'assets 2', 'FlightSelection.jpg')
        img = Image.open(bg_path)
        img = img.resize((self.master.winfo_screenwidth(), self.master.winfo_screenheight()), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(img)

        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # === Container Frame (Center Aligned) ===
        container = tk.Frame(self, bg="#ffffff", bd=2, relief="ridge")
        container.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(container, text="Select Your Flight", font=("Segoe UI", 18, "bold")).pack(pady=(20, 10))

        ttk.Label(container, text="Origin Country:").pack(pady=(10, 0))
        self.origin_var = tk.StringVar()
        self.origin_combo = ttk.Combobox(container, textvariable=self.origin_var, width=50, state="readonly")
        self.origin_combo['values'] = sorted({f['origin_country'] for f in self.flights})
        self.origin_combo.pack()

        ttk.Label(container, text="Destination Country:").pack(pady=(10, 0))
        self.dest_var = tk.StringVar()
        self.dest_combo = ttk.Combobox(container, textvariable=self.dest_var, width=50, state="readonly")
        self.dest_combo.pack()

        self.listbox = tk.Listbox(container, width=100, height=10)
        self.listbox.pack(pady=20)

        ttk.Button(container, text="Continue", command=self.continue_pressed).pack(pady=(0, 10))

        # === Back Button ===
        ttk.Button(self, text="← Back", command=self.on_back).place(x=10, y=10)

        # === Event Bindings ===
        self.origin_combo.bind("<<ComboboxSelected>>", self.update_destinations)
        self.dest_combo.bind("<<ComboboxSelected>>", self.update_flights)

    def update_destinations(self, event=None):
        origin = self.origin_var.get()
        dests = sorted({f['dest_country'] for f in self.flights if f['origin_country'] == origin})
        self.dest_combo['values'] = dests
        self.dest_var.set('')
        self.listbox.delete(0, tk.END)

    def update_flights(self, event=None):
        origin = self.origin_var.get()
        dest = self.dest_var.get()
        self.listbox.delete(0, tk.END)
        for f in self.flights:
            if f['origin_country'] == origin and f['dest_country'] == dest:
                info = f"{f['flight_id']} | {f['date']} {f['time']} | {f['origin_airport']} → {f['dest_airport']}"
                self.listbox.insert(tk.END, info)

    def continue_pressed(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a flight.")
            return
        selected_line = self.listbox.get(selection[0])
        flight_id = selected_line.split(" | ")[0]
        flight = next(f for f in self.flights if f['flight_id'] == flight_id)
        self.on_continue(flight)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flight Booking System")
        self.geometry("900x600")
        self.resizable(False, False)
        self.current_frame = None
        self.show_selection()

    def show_selection(self):
        self.clear_frame()
        self.current_frame = FlightSelectionFrame(self, on_continue=self.show_seatmap, on_back=self.restart_login)

    def show_seatmap(self, flight):
        from gui.seat_map_gui import SeatMapFrame
        self.clear_frame()
        self.current_frame = SeatMapFrame(self, flight, on_back=self.show_selection)

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def restart_login(self):
        self.destroy()  # Kill this window
        import main
        main.run_login_again()  # 🔁 You'll define this next


