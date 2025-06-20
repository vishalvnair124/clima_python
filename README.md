# ☁️ clima_backend – Weather Forecasting Backend with Python

**clima_backend** is the Python backend for the Clima weather forecasting app. It handles user authentication, weather data retrieval, time-series forecasting (ARIMA), and email-based features, making it the core engine of the Clima system.

---

## ✨ Features

- 🔐 User authentication with email and password handling  
- ⛅ Real-time weather data fetching (daily & hourly)  
- 📈 Forecasting using ARIMA models (stored as `.pkl`)  
- 📬 Email notifications and password generation  
- ⚙️ Modular Python files for user and data handling

---

## 🚀 How to Run

1. **Clone the repository:**

```bash
git clone https://github.com/vishalvnair124/clima_backend.git
```

2. **Navigate into the project and set up the virtual environment:**

```bash
cd clima_backend
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

3. **Run the main backend app:**

```bash
python app.py
```

---

## 🗂 Project Structure

```plaintext
clima_backend/
│
├── app.py               # Entry point of the backend server
├── auth_utils.py        # Utilities for authentication
├── forecast.py          # Weather forecast logic
├── weatherfetch.py      # Fetches live weather data
├── get_daily.py         # Fetch daily weather data
├── get_hourly.py        # Fetch hourly weather data
├── arima_models.pkl     # Serialized ARIMA models
├── user.py              # User creation/login handler
├── login.py             # Login email verification
├── mail.py              # Email sending functionality
├── random_password.py   # Random password generator
├── userfetch.py         # Fetches user data
├── check.py             # Input validation
├── thisweektemp.py      # Weekly forecast logic
├── gen.py               # Additional generation logic
├── mytest.py            # UI test scripts
├── env/                 # Python virtual environment
└── README.md            # Project documentation
```

---

## 🛠 Requirements

- Python 3.8+  
- Flask or FastAPI (as backend framework)  
- Pandas, NumPy, scikit-learn, and other data libraries  
- A weather API (like OpenWeatherMap or similar)

---

## 👨‍💻 Author

**Vishal V Nair**  
🚀 Python & API Developer  
📫 GitHub: [@vishalvnair124](https://github.com/vishalvnair124)
