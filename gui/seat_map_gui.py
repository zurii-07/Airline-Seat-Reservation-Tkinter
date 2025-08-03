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
        self.seat_frame = tk.Frame(self)
        self.seat_frame.pack(pady=10)

        rows = [str(i) for i in range(1, 21)]  # Rows 1 to 20 (top to bottom)
        cols = list("ABCDEFGHI")
        groupings = [cols[0:3], cols[3:6], cols[6:9]]  # ABC, DEF, GHI

        # === Cockpit ===
        tk.Label(self.seat_frame, text="Cockpit", font=("Arial", 12, "italic")).grid(
            row=0, column=0, columnspan=20, pady=(10, 5)
        )

        # === Column Header (A to I with spacing) ===
        col_offset = 2
        for g_index, group in enumerate(groupings):
            for c_index, col in enumerate(group):
                grid_col = col_offset + g_index * 4 + c_index  # Gap after each group (3 + 1)
                tk.Label(self.seat_frame, text=col, font=("Arial", 10, "bold")).grid(
                    row=1, column=grid_col, pady=(0, 5)
                )

        # === Seat Grid ===
        for r_index, row_number in enumerate(rows, start=2):  # Starts from row 2 to leave space for column letters
            # Window left
            tk.Label(self.seat_frame, text="Window", fg="gray").grid(row=r_index, column=0, padx=(10, 5))
            # Row number
            tk.Label(self.seat_frame, text=str(row_number), font=("Arial", 10)).grid(row=r_index, column=1)

            current_col = 2  # Starting column for seat buttons

            for col_index, col in enumerate(cols):
                # Add extra spacing columns between groups
                if col in ['D', 'G']:  # after C and F (ABC | DEF | GHI)
                    tk.Label(self.seat_frame, text=" ").grid(row=r_index, column=current_col)
                    current_col += 1

                seat_id = f"{col}{row_number}"
                booked = self.bookings.get(seat_id)

                if booked:
                    gender = booked["gender"].strip().upper()
                    text = gender
                    bg = "#e80cdd" if gender == "F" else "red"
                else:
                    text = ""
                    bg = "#a6f20f"  # Available

                btn = tk.Button(self.seat_frame, text=text, width=3, bg=bg,
                                command=lambda s=seat_id: self.book_seat(s))
                btn.grid(row=r_index, column=current_col, padx=1, pady=2)

                current_col += 1

            # Window right
            tk.Label(self.seat_frame, text="Window", fg="gray").grid(row=r_index, column=current_col, padx=(5, 10))

        # === Lavatory ===
        tk.Label(self.seat_frame, text="Lavatory", font=("Arial", 12, "italic")).grid(
            row=r_index + 1, column=0, columnspan=20, pady=(15, 5)
        )

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


