import tkinter as tk
from tkinter import messagebox
from backend.seat_manager import load_bookings, save_booking

class SeatMapFrame(tk.Frame):
    def __init__(self, master, flight, on_back):
        super().__init__(master)
        self.master = master
        self.master.state("zoomed")
        self.flight = flight
        self.on_back = on_back
        self.pack(fill='both', expand=True)

        self.bookings = load_bookings(flight['flight_id'])

        # === Top Navigation ===
        tk.Button(self, text="← Back", command=self.on_back).pack(anchor='nw', pady=5, padx=5)

        title = (f"Flight {flight['flight_id']}  | "
                 f"{flight['date']} {flight['time']}  | "
                 f"{flight['origin_airport']} → {flight['dest_airport']}")
        tk.Label(self, text=title, font=("Segoe UI", 16, "bold")).pack(pady=10)

        # === Scrollable Canvas ===
        canvas_frame = tk.Frame(self)
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        self.container = tk.Frame(canvas)
        self.container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.container, anchor="nw")

        # === Main UI Blocks Inside Scrollable Area ===
        self.seat_frame = tk.Frame(self.container)
        self.seat_frame.pack(pady=(10, 0))

        self.form_frame = None

        self.draw_seats()

    def draw_seats(self):
        self.seat_frame.destroy()
        self.seat_frame = tk.Frame(self.container)
        self.seat_frame.pack(pady=10)

        rows = [str(i) for i in range(1, 21)]
        cols = list("ABCDEFGHI")
        groupings = [cols[0:3], cols[3:6], cols[6:9]]  # ABC DEF GHI

        # === Cockpit ===
        tk.Label(self.seat_frame, text="Cockpit", font=("Arial", 12, "italic")).grid(
            row=0, column=0, columnspan=20, pady=(10, 5)
        )

        # === Column Labels ===
        col_offset = 2
        for g_index, group in enumerate(groupings):
            for c_index, col in enumerate(group):
                grid_col = col_offset + g_index * 4 + c_index
                tk.Label(self.seat_frame, text=col, font=("Arial", 10, "bold")).grid(
                    row=1, column=grid_col, pady=(0, 5)
                )

        # === Seat Grid ===
        for r_index, row_number in enumerate(rows, start=2):
            tk.Label(self.seat_frame, text="Window", fg="gray").grid(row=r_index, column=0, padx=(10, 5))
            tk.Label(self.seat_frame, text=str(row_number), font=("Arial", 10)).grid(row=r_index, column=1)

            current_col = 2
            for col_index, col in enumerate(cols):
                if col in ['D', 'G']:
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
                    bg = "#a6f20f"

                btn = tk.Button(self.seat_frame, text=text, width=3, bg=bg,
                                command=lambda sid=seat_id: self.book_seat(sid))
                btn.grid(row=r_index, column=current_col, padx=1, pady=2)
                current_col += 1

            tk.Label(self.seat_frame, text="Window", fg="gray").grid(
                row=r_index, column=current_col, padx=(5, 10)
            )

        # === Lavatory ===
        tk.Label(self.seat_frame, text="Lavatory", font=("Arial", 12, "italic")).grid(
            row=r_index + 1, column=0, columnspan=20, pady=(15, 5)
        )

    def book_seat(self, seat_id):
        if seat_id in self.bookings:
            messagebox.showinfo("Booked", f"Seat {seat_id} is already booked.")
            return

        if self.form_frame:
            self.form_frame.destroy()

        self.form_frame = tk.Frame(self.container)
        self.form_frame.pack(pady=20)

        tk.Label(self.form_frame, text=f"Booking Seat: {seat_id}", font=("Segoe UI", 12, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 10)
        )

        # === Form Fields ===
        tk.Label(self.form_frame, text="Full Name:").grid(row=1, column=0, sticky='e', padx=5, pady=2)
        name_entry = tk.Entry(self.form_frame, width=30)
        name_entry.grid(row=1, column=1)

        tk.Label(self.form_frame, text="Gender (M/F):").grid(row=2, column=0, sticky='e', padx=5, pady=2)
        gender_entry = tk.Entry(self.form_frame, width=10)
        gender_entry.grid(row=2, column=1, sticky='w')

        tk.Label(self.form_frame, text="Passport No:").grid(row=3, column=0, sticky='e', padx=5, pady=2)
        passport_entry = tk.Entry(self.form_frame, width=30)
        passport_entry.grid(row=3, column=1)

        tk.Label(self.form_frame, text="Visa No:").grid(row=4, column=0, sticky='e', padx=5, pady=2)
        visa_entry = tk.Entry(self.form_frame, width=30)
        visa_entry.grid(row=4, column=1)

        def confirm():
            name = name_entry.get().strip()
            gender = gender_entry.get().strip().upper()
            passport = passport_entry.get().strip()
            visa = visa_entry.get().strip()

            if not all([name, gender, passport, visa]) or gender not in ("M", "F"):
                messagebox.showwarning("Incomplete", "Please fill all fields correctly.")
                return

            passenger = {
                "name": name,
                "gender": gender,
                "passport": passport,
                "visa": visa,
                "booked_by": "current_user"
            }

            save_booking(self.flight['flight_id'], seat_id, passenger)
            self.bookings[seat_id] = passenger

            self.form_frame.destroy()
            self.form_frame = None

            self.draw_seats()

        tk.Button(self.form_frame, text="Confirm Booking", command=confirm,
                  bg="#28a745", fg="white", width=20).grid(
            row=5, column=0, columnspan=2, pady=10
        )
