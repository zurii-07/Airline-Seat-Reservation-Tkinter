# ✈️ FlightForge: Airline Seat Reservation System

A Python-based GUI system for airline seat reservations across **193 countries** and **386+ global flight routes** — built with **Tkinter**, **CSV** data handling, and dynamic seat visualization.

---

## 🚀 Overview

This project simulates a real-world airline booking system, allowing users to:

- 🔐 Register & log in as passengers  
- 🌍 Select flights by origin/destination country  
- 🎫 View upcoming flights within 7 days  
- 💺 Book available seats from a visual seat map  
- 📄 Fill in passenger details (Name, Gender, Passport, Visa)  
- 🧾 Track booking history by user  

---

## 🧠 Features

1. 🎨 Tkinter GUI with slideshow backgrounds & blurred form effects  
2. 👥 Multi-user authentication with CSV-based login/register system  
3. 🌐 193×2 = **386+ flights** generated weekly using airport data  
4. 🪑 Seat Map Layout: 9×20 grid with cockpit, windows, lavatory  
5. 🎨 Gender-based seat indicators:
   - 🔴 Male
   - 🩷 Female
   - 🟢 Available  
6. 📝 Booking form integration (below seat map or side panel)  
7. 🧾 Real-time booking updates & no double-booking  
8. 🧳 User-specific booking history side panel  
9. 🔄 Scroll-enabled seat layout (optional for future enhancements)  

---

## 🧰 Tech Stack

| Tool      | Description               |
|-----------|---------------------------|
| **Python 3.13** | Core Programming Language |
| **Tkinter**     | GUI Framework              |
| **CSV**         | Persistent storage backend |
| **Pillow**      | Background image slideshow |

---

## 🗂️ Project Structure

```bash
airline_seat_reservation/
├── main.py                  # Launcher
├── gui/
│   ├── login_gui.py
│   ├── flight_selection_gui.py
│   └── seat_map_gui.py
├── backend/
│   ├── user_manager.py
│   ├── flight_data.py
│   └── seat_manager.py
├── data/
│   ├── users.csv
│   ├── airports.csv
│   └── bookings_*.csv
├── assets/
│   └── 4K2.jpg, SriLankan-Airlines-Airbus.jpg, Window.jpg, Wing-1.jpg
├── assets 2/
│   └── NewUser.jpg, FlightSelection.jpg, seat_bg.jpg
```


---

## 📸 Screenshots

### 🔐 Login Page
![Login](screenshots/Login%20Page.png)

### 🛫 Flight Selection
![Flights](screenshots/Flight%20Selection.png)

### 🪑 Seat Map Interface
![Seat Map](screenshots/Seat%20Map%20GUI.png)

---

## 📦 Installation & Run

### 1. ✅ Clone the repo

```bash
git clone https://github.com/zurii-07/Airline-Seat-Reservation-Tkinter.git
cd Airline-Seat-Reservation-Tkinter
```

### 2.📦 Create Virtual Env (optional)

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate
```

### 3.💡 Install dependencies

```bash
pip install -r requirements.txt
```

### 4.🧨 Run the App

```bash
python main.py
```

### 🧑‍🎓 Author

Surakkitha Galappaththi – [LinkedIn](https://www.linkedin.com/in/surakkitha-galappaththi-001588290)
Data Science | AI Engineer | Python Enthusiast
Email: surakkithag@gmail.com

### 📄 License

MIT License
