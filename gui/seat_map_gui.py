import tkinter as tk
from tkinter import simpledialog, messagebox
from backend.seat_manager import load_bookings, save_booking

class SeatMapFrame(tk.Frame):
    def __init__(self, master, flight, on_back):
        super().__init__(master)
        self.master = master
        self.master.state("zoomed")
        self.flight = flight
        self.on_back = on_back
        self.pack(fill='both', expand=True)

        tk.Button(self, text="← Back", command=self.on_back).pack(anchor='nw', pady=5, padx=5)

        title = (f"Flight {flight['flight_id']}  | "
                 f"{flight['date']} {flight['time']}  | "
                 f"{flight['origin_airport']} → {flight['dest_airport']}")
        tk.Label(self, text=title, font=("Segoe UI", 16, "bold")).pack(pady=10)

        self.seat_frame = tk.Frame(self)
        self.seat_frame.pack()

        self.bookings = load_bookings(flight['flight_id'])
        self.draw_seats()

    def draw_seats(self):
        header = tk.Frame(self.seat_frame)
        header.grid(row=0, column=0, columnspan=21)
        tk.Label(header, text="Cockpit", font=("Arial",12,"italic")).grid(row=0, column=0, columnspan=21)

        rows = "ABCDEFGHI"
        for r_index, row in enumerate(rows, start=1):
            lbl = tk.Label(self.seat_frame, text=row, width=2)
            lbl.grid(row=r_index, column=0)
            for c in range(1, 21):
                seat_id = f"{row}{c}"
                booked = self.bookings.get(seat_id)
                if booked:
                    txt = booked['gender']
                    bg = "red"
                else:
                    txt = ""
                    bg = "green"

                btn = tk.Button(self.seat_frame, text=txt, width=3, bg=bg,
                                command=lambda s=seat_id: self.book_seat(s))
                btn.grid(row=r_index, column=c, padx=2, pady=2)

        # side windows as blank column at left/right
        for i in range(1, 10):
            tk.Label(self.seat_frame, text=" ", width=1,
                     bg="lightblue").grid(row=i, column=21)
        for i in range(1, 10):
            tk.Label(self.seat_frame, text=" ", width=1,
                     bg="lightblue").grid(row=i, column=22)

    def book_seat(self, seat_id):
        if seat_id in self.bookings:
            messagebox.showinfo("Booked", f"Seat {seat_id} is already booked.")
            return
        info = {}
        info['name'] = simpledialog.askstring("Name", "Passenger Name:")
        if not info['name']:
            return
        info['gender'] = simpledialog.askstring("Gender (M/F)", "Gender (M/F):")
        if info['gender'] not in ('M','F'):
            messagebox.showwarning("Invalid", "Enter M or F")
            return
        info['passport'] = simpledialog.askstring("Passport", "Passport Number:")
        info['visa'] = simpledialog.askstring("Visa", "Visa Number:")
        info['booked_by'] = "current_user"  # Replace or pass real username

        save_booking(self.flight['flight_id'], seat_id, info)
        self.bookings[seat_id] = info
        self.seat_frame.destroy()
        self.seat_frame = tk.Frame(self)
        self.seat_frame.pack()
        self.draw_seats()


