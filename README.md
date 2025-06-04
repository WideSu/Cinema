# Cinema Booking System

A simple command-line cinema seat booking system in Python. This project allows users to:

- Set up a cinema seating plan with a **movie title, number of rows, and seats per row**
- Book tickets (with default or custom seat selection)
       - If user choose customized seating, max trials = **3 times** for **valid** selection.
       - If after 3 valid selection, user still doesn't confirm the selection, the system will return to the main menu
- Check bookings by booking ID (e.g. GIC0001)
- Exit the system

## Features
- **Seat selection:** Default (best available) or custom (user-specified)
- **Booking ID management:** Unique, reusable booking IDs
- **User-friendly errors:** Handles invalid input and booking errors gracefully
- **Unit tests:** Comprehensive test coverage for core logic and CLI

## Project Structure

```
Cinema/
├── __init__.py
├── main.py           # Main application logic
├── models.py         # Cinema, booking, and error classes
├── utilities.py      # Utilities functions
├── requirements.txt  # Python dependencies
├── test_main.py      # Unit tests for main.py
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

### 2. Set up and activate a virtual environment (recommended)
#### MAC/Linux
```sh
python3 -m venv .venv
source .venv/bin/activate 
```
#### Windows
```sh
python -m venv .venv
.venv\Scripts\activate.bat
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

Output
```
(.venv) (base) huanganni@Huangs-MacBook-Pro Cinema % pytest
======================================== test session starts =========================================
platform darwin -- Python 3.10.9, pytest-8.4.0, pluggy-1.6.0
rootdir: /Users/huanganni/Documents/GitHub/Cinema
plugins: mock-3.14.1, cov-6.1.1
collected 54 items                                                                                   

test_main.py ..................................                                                [ 62%]
test_models.py ....................                                                            [100%]

========================================= 54 passed in 0.04s =========================================
```

## Usage
- Follow the prompts to set up the cinema and book tickets.
- You can check or cancel bookings using the booking ID provided after reservation.

## Customization
- Modify `models.py` to change seat selection logic or booking rules.
- Extend `main.py` for more CLI features.

## Example usage
### Undecisive customer
```bash
(.venv) (base) huanganni@Huangs-MacBook-Pro Cinema % /Users/huanganni/Documents/GitHub/Cinema/.venv/bin/pyth
on /Users/huanganni/Documents/GitHub/Cinema/main.py
Enter movie title, number of rows, and seats per row (separated by space):
>John Wick 4 8 10
Welcome to GIC Cinemas!
[1] Book Tickets
[2] Check Booking
[3] Exit
Select an option (1-3):
>1
Enter number of tickets:
>10

Successfully reserved 10 John Wick 4 tickets.
Booking ID: GIC0001
Selected seats:
                   S C R E E N              
--------------------------------------------
Legend: '.' = Available, '#' = Other Bookings, 'O' = Reserved

H      .   .   .   .   .   .   .   .   .   .
G      .   .   .   .   .   .   .   .   .   .
F      .   .   .   .   .   .   .   .   .   .
E      .   .   .   .   .   .   .   .   .   .
D      .   .   .   .   .   .   .   .   .   .
C      .   .   .   .   .   .   .   .   .   .
B      .   .   .   .   .   .   .   .   .   .
A      O   O   O   O   O   O   O   O   O   O
       1   2   3   4   5   6   7   8   9  10
Press Enter to accept default, or enter seat position (e.g., A5):
>A5

Booking ID: GIC0001
Selected seats:
                   S C R E E N              
--------------------------------------------
Legend: '.' = Available, '#' = Other Bookings, 'O' = Reserved

H      .   .   .   .   .   .   .   .   .   .
G      .   .   .   .   .   .   .   .   .   .
F      .   .   .   .   .   .   .   .   .   .
E      .   .   .   .   .   .   .   .   .   .
D      .   .   .   .   .   .   .   .   .   .
C      .   .   .   .   .   .   .   .   .   .
B      .   .   .   O   O   O   O   .   .   .
A      .   .   .   .   O   O   O   O   O   O
       1   2   3   4   5   6   7   8   9  10
Press Enter to accept this selection, or enter another seat position:
>B8

Booking ID: GIC0001
Selected seats:
                   S C R E E N              
--------------------------------------------
Legend: '.' = Available, '#' = Other Bookings, 'O' = Reserved

H      .   .   .   .   .   .   .   .   .   .
G      .   .   .   .   .   .   .   .   .   .
F      .   .   .   .   .   .   .   .   .   .
E      .   .   .   .   .   .   .   .   .   .
D      .   .   .   .   .   .   .   .   .   .
C      .   O   O   O   O   O   O   O   .   .
B      .   .   .   .   .   .   .   O   O   O
A      .   .   .   .   .   .   .   .   .   .
       1   2   3   4   5   6   7   8   9  10
Exceeded maximum 3 tries. Please start over.
```

### Continuous booking
```bash
(.venv) (base) huanganni@Huangs-MacBook-Pro Cinema % /Users/huanganni/Documents/GitHub/Cinema/.venv/bi
n/python /Users/huanganni/Documents/GitHub/Cinema/main.py
Enter movie title, number of rows, and seats per row (separated by space):
>John Wick 8 10
Welcome to GIC Cinemas!
[1] Book Tickets
[2] Check Booking
[3] Exit
Select an option (1-3):
>1
Enter number of tickets:
>5

Successfully reserved 5 John Wick tickets.
Booking ID: GIC0001
Selected seats:
                   S C R E E N              
--------------------------------------------
Legend: '.' = Available, '#' = Other Bookings, 'O' = Reserved

H      .   .   .   .   .   .   .   .   .   .
G      .   .   .   .   .   .   .   .   .   .
F      .   .   .   .   .   .   .   .   .   .
E      .   .   .   .   .   .   .   .   .   .
D      .   .   .   .   .   .   .   .   .   .
C      .   .   .   .   .   .   .   .   .   .
B      .   .   .   .   .   .   .   .   .   .
A      .   .   O   O   O   O   O   .   .   .
       1   2   3   4   5   6   7   8   9  10
Press Enter to accept default, or enter seat position (e.g., A5):
>B8

Booking ID: GIC0001
Selected seats:
                   S C R E E N              
--------------------------------------------
Legend: '.' = Available, '#' = Other Bookings, 'O' = Reserved

H      .   .   .   .   .   .   .   .   .   .
G      .   .   .   .   .   .   .   .   .   .
F      .   .   .   .   .   .   .   .   .   .
E      .   .   .   .   .   .   .   .   .   .
D      .   .   .   .   .   .   .   .   .   .
C      .   .   .   .   O   O   .   .   .   .
B      .   .   .   .   .   .   .   O   O   O
A      .   .   .   .   .   .   .   .   .   .
       1   2   3   4   5   6   7   8   9  10
Press Enter to accept this selection, or enter another seat position:
>C6

Booking ID: GIC0001
Selected seats:
                   S C R E E N              
--------------------------------------------
Legend: '.' = Available, '#' = Other Bookings, 'O' = Reserved

H      .   .   .   .   .   .   .   .   .   .
G      .   .   .   .   .   .   .   .   .   .
F      .   .   .   .   .   .   .   .   .   .
E      .   .   .   .   .   .   .   .   .   .
D      .   .   .   .   .   .   .   .   .   .
C      .   .   .   .   .   O   O   O   O   O
B      .   .   .   .   .   .   .   .   .   .
A      .   .   .   .   .   .   .   .   .   .
       1   2   3   4   5   6   7   8   9  10
Press Enter to accept default, or enter seat position (e.g., A5):
>D5

Booking ID: GIC0001
Selected seats:
                   S C R E E N              
--------------------------------------------
Legend: '.' = Available, '#' = Other Bookings, 'O' = Reserved

H      .   .   .   .   .   .   .   .   .   .
G      .   .   .   .   .   .   .   .   .   .
F      .   .   .   .   .   .   .   .   .   .
E      .   .   .   .   .   .   .   .   .   .
D      .   .   .   .   O   O   O   O   O   .
C      .   .   .   .   .   .   .   .   .   .
B      .   .   .   .   .   .   .   .   .   .
A      .   .   .   .   .   .   .   .   .   .
       1   2   3   4   5   6   7   8   9  10
Press Enter to accept this selection, or enter another seat position:
>
Booking ID: GIC0001 confirmed.
Welcome to GIC Cinemas!
[1] Book Tickets
[2] Check Booking
[3] Exit
Select an option (1-3):
>2
Enter your booking ID:
>GIC0001
Booking id: GIC0001
Selected seats:
Seating plan highlighting Booking ID: GIC0001
                   S C R E E N              
--------------------------------------------

Highlighting seats for Booking ID: GIC0001
Legend: '.' = Available, '#' = Other Bookings, 'B' = Your Booked Seats

H      .   .   .   .   .   .   .   .   .   .
G      .   .   .   .   .   .   .   .   .   .
F      .   .   .   .   .   .   .   .   .   .
E      .   .   .   .   .   .   .   .   .   .
D      .   .   .   .   B   B   B   B   B   .
C      .   .   .   .   .   .   .   .   .   .
B      .   .   .   .   .   .   .   .   .   .
A      .   .   .   .   .   .   .   .   .   .
       1   2   3   4   5   6   7   8   9  10

Booking Details for GIC0001:
Number of seats: 5
Booked seats: D5, D6, D7, D8, D9
Welcome to GIC Cinemas!
[1] Book Tickets
[2] Check Booking
[3] Exit
Select an option (1-3):
>1
Enter number of tickets:
>3

Successfully reserved 3 John Wick tickets.
Booking ID: GIC0002
Selected seats:
                   S C R E E N              
--------------------------------------------
Legend: '.' = Available, '#' = Other Bookings, 'O' = Reserved

H      .   .   .   .   .   .   .   .   .   .
G      .   .   .   .   .   .   .   .   .   .
F      .   .   .   .   .   .   .   .   .   .
E      .   .   .   .   .   .   .   .   .   .
D      .   .   .   .   #   #   #   #   #   .
C      .   .   .   .   .   .   .   .   .   .
B      .   .   .   .   .   .   .   .   .   .
A      .   .   .   O   O   O   .   .   .   .
       1   2   3   4   5   6   7   8   9  10
Press Enter to accept default, or enter seat position (e.g., A5):
>B5

Booking ID: GIC0002
Selected seats:
                   S C R E E N              
--------------------------------------------
Legend: '.' = Available, '#' = Other Bookings, 'O' = Reserved

H      .   .   .   .   .   .   .   .   .   .
G      .   .   .   .   .   .   .   .   .   .
F      .   .   .   .   .   .   .   .   .   .
E      .   .   .   .   .   .   .   .   .   .
D      .   .   .   .   #   #   #   #   #   .
C      .   .   .   .   .   .   .   .   .   .
B      .   .   .   .   O   O   O   .   .   .
A      .   .   .   .   .   .   .   .   .   .
       1   2   3   4   5   6   7   8   9  10
Press Enter to accept this selection, or enter another seat position:
>C2

Booking ID: GIC0002
Selected seats:
                   S C R E E N              
--------------------------------------------
Legend: '.' = Available, '#' = Other Bookings, 'O' = Reserved

H      .   .   .   .   .   .   .   .   .   .
G      .   .   .   .   .   .   .   .   .   .
F      .   .   .   .   .   .   .   .   .   .
E      .   .   .   .   .   .   .   .   .   .
D      .   .   .   .   #   #   #   #   #   .
C      .   O   O   O   .   .   .   .   .   .
B      .   .   .   .   .   .   .   .   .   .
A      .   .   .   .   .   .   .   .   .   .
       1   2   3   4   5   6   7   8   9  10
Press Enter to accept default, or enter seat position (e.g., A5):
>
Booking ID: GIC0002 confirmed.
Welcome to GIC Cinemas!
[1] Book Tickets
[2] Check Booking
[3] Exit
Select an option (1-3):
>2
Enter your booking ID:
>GIC0002
Booking id: GIC0002
Selected seats:
Seating plan highlighting Booking ID: GIC0002
                   S C R E E N              
--------------------------------------------

Highlighting seats for Booking ID: GIC0002
Legend: '.' = Available, '#' = Other Bookings, 'B' = Your Booked Seats

H      .   .   .   .   .   .   .   .   .   .
G      .   .   .   .   .   .   .   .   .   .
F      .   .   .   .   .   .   .   .   .   .
E      .   .   .   .   .   .   .   .   .   .
D      .   .   .   .   #   #   #   #   #   .
C      .   B   B   B   .   .   .   .   .   .
B      .   .   .   .   .   .   .   .   .   .
A      .   .   .   .   .   .   .   .   .   .
       1   2   3   4   5   6   7   8   9  10

Booking Details for GIC0002:
Number of seats: 3
Booked seats: C2, C3, C4
Welcome to GIC Cinemas!
[1] Book Tickets
[2] Check Booking
[3] Exit
Select an option (1-3):
>3
Thank you for using GIC Cinemas. Bye!
```

## License
MIT License

---

*Created for educational and demonstration purposes.*
