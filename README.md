# Cinema Booking System

A simple command-line cinema seat booking system in Python. This project allows users to:

- Set up a cinema with a custom movie title, number of rows, and seats per row
- Book tickets (with default or custom seat selection)
- Check bookings by booking ID
- Cancel bookings
- View a visual seating chart

## Features
- **Seat selection:** Default (best available) or custom (user-specified)
- **Booking ID management:** Unique, reusable booking IDs
- **User-friendly errors:** Handles invalid input and booking errors gracefully
- **Unit tests:** Comprehensive test coverage for core logic and CLI

## Project Structure

```
Cinema/
├── __init__.py
├── main.py           # main console application logic
├── models.py         # Cinema, booking, and error classes
├── requirements.txt  # Python dependencies
├── test_models.py    # Unit tests for models.py
├── README.md         # Documentation
└── .gitignore        # Git ignore rules
```

## Getting Started

### 1. Clone the repository
```sh
git clone <your-repo-url>
cd Cinema
```

### 2. Set up a virtual environment (recommended)
```sh
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```sh
pip install -r requirements.txt
```

### 4. Run the application
```sh
python -m main
```

### 5. Run the tests
From the parent directory (to support relative imports):
```sh
pytest
```

## Usage
- Follow the prompts to set up the cinema and book tickets.
- You can check or cancel bookings using the booking ID provided after reservation.

## Customization
- Modify `models.py` to change seat selection logic or booking rules.
- Extend `main.py` for more CLI features.

## License
MIT License

---

*Created for educational and demonstration purposes.*
