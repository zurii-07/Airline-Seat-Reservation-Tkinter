import tkinter as tk
from tkinter import messagebox
from backend.seat_manager import load_bookings, save_booking, user_bookings

class SeatMapFrame(tk.Frame):
    def __init__(self, master, flight, on_back, current_user):
        super().__init__(master)
        self.master = master
        self.master.state("zoomed")
        self.flight = flight
        self.on_back = on_back
        self.current_user = current_user
        self.pack(fill='both', expand=True)

        self.bookings = load_bookings(flight['flight_id'])

        tk.Button(self, text="← Back", command=self.on_back).pack(anchor='nw', pady=5, padx=5)
        title = (f"Flight {flight['flight_id']}  | {flight['date']} {flight['time']}  | "
                 f"{flight['origin_airport']} → {flight['dest_airport']}")
        tk.Label(self, text=title, font=("Segoe UI", 16, "bold")).pack(pady=10)

        from gui.flight_selection_gui import App
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

        # layout wrapper
        self.center_frame = tk.Frame(self.container)
        self.center_frame.pack(pady=10)
        self.grid_frame = tk.Frame(self.center_frame)
        self.grid_frame.pack(anchor="center")
        self.seat_frame = tk.Frame(self.grid_frame)
        self.seat_frame.pack(side="left", anchor="n", padx=(0, 30))
        self.form_frame = None

        # After scrollable area setup:
        self.draw_seats()

        # === Now add bookings panel anchored on right of master ===
        panel = tk.Frame(self, bg="#f9f9f9", bd=1, relief="solid")
        panel.place(relx=0.85, rely=0.2, width=260, height=300, anchor="n")
        tk.Label(panel, text="Your Bookings", font=("Segoe UI", 12, "bold"), bg=panel["bg"]).pack(pady=5)
        self.booking_list = tk.Listbox(panel, width=30, height=12)
        self.booking_list.pack(padx=10, pady=5)
        for bk in user_bookings(self.current_user):
            entry = f"{bk['flight_id']} | Seat:{bk['seat']} | {bk['name']}"
            self.booking_list.insert(tk.END, entry)

        exit_btn = tk.Button(self, text="Exit", bg="#d9534f", fg="white", font=("Segoe UI", 10, "bold"),
                             command=self.master.quit)
        exit_btn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

    def draw_seats(self):
        self.seat_frame.destroy()
        self.seat_frame = tk.Frame(self.grid_frame)
        self.seat_frame.pack(side="left", anchor="n", padx=(0, 30))

        rows = [str(i) for i in range(1, 21)]
        cols = list("ABCDEFGHI")
        groupings = [cols[0:3], cols[3:6], cols[6:9]]

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

        self.form_frame = tk.Frame(self.grid_frame, bd=2, relief="groove", padx=10, pady=10, bg="white")
        self.form_frame.pack(side="right", anchor="n", padx=10)

        tk.Label(self.form_frame, text=f"Booking Seat: {seat_id}", font=("Segoe UI", 12, "bold"), bg="white").grid(
            row=0, column=0, columnspan=2, pady=(0, 10)
        )

        # === Form Fields ===
        def label(text, row):
            return tk.Label(self.form_frame, text=text, bg="white").grid(row=row, column=0, sticky='e', padx=5, pady=2)

        def entry(row, width=30):
            e = tk.Entry(self.form_frame, width=width)
            e.grid(row=row, column=1)
            return e

        label("Full Name:", 1)
        name_entry = entry(1)

        label("Gender (M/F):", 2)
        gender_entry = entry(2, width=10)

        label("Passport No:", 3)
        passport_entry = entry(3)

        label("Visa No:", 4)
        visa_entry = entry(4)

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
                "booked_by": self.current_user
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


