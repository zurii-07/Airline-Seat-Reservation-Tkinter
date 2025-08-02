import tkinter as tk
from tkinter import ttk, messagebox
from backend.flight_data import generate_flights

class FlightSelectionFrame(tk.Frame):
    def __init__(self, master, on_continue):
        super().__init__(master)
        self.on_continue = on_continue
        self.flights = generate_flights(days_ahead=7)
        self.pack(fill='both', expand=True)

        ttk.Label(self, text="Select Your Flight", font=("Segoe UI",18,"bold")).pack(pady=10)
        ttk.Label(self, text="Origin Country:").pack()
        self.origin_var = tk.StringVar()
        self.origin_combo = ttk.Combobox(self, textvariable=self.origin_var, width=50)
        self.origin_combo['values'] = sorted({f['origin_country'] for f in self.flights})
        self.origin_combo.pack()

        ttk.Label(self, text="Destination Country:").pack(pady=(10,0))
        self.dest_var = tk.StringVar()
        self.dest_combo = ttk.Combobox(self, textvariable=self.dest_var, width=50)
        self.dest_combo.pack()

        self.listbox = tk.Listbox(self, width=100, height=10)
        self.listbox.pack(pady=20)

        ttk.Button(self, text="Continue", command=self.continue_pressed).pack()
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
                self.listbox.insert(tk.END, f"{f['flight_id']} | {f['date']} {f['time']} | {f['origin_airport']} → {f['dest_airport']}")

    def continue_pressed(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("No flight", "Select a flight first")
            return
        chosen = self.listbox.get(sel[0])
        fid = chosen.split(" | ")[0]
        flight = next(f for f in self.flights if f['flight_id']==fid)
        self.on_continue(flight)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flight Booking")
        self.geometry("800x600")
        self.current_frame = None
        self.show_selection()

    def show_selection(self):
        self.clear_frame()
        self.current_frame = FlightSelectionFrame(self, on_continue=self.show_seatmap)

    def show_seatmap(self, flight):
        from gui.seat_map_gui import SeatMapFrame
        self.clear_frame()
        self.current_frame = SeatMapFrame(self, flight, on_back=self.show_selection)

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

if __name__=="__main__":
    App().mainloop()

