import pytest
from .models import Cinema, CinemaError, InvalidSeatError, BookingError

# Test Cinema creation and validation
def test_cinema_creation_valid():
    c = Cinema("Test Movie", 5, 8)
    assert c.title == "Test Movie"
    assert c.rows == 5
    assert c.seats_per_row == 8
    assert len(c.seating) == 5
    assert all(len(row) == 8 for row in c.seating)

def test_cinema_creation_invalid():
    with pytest.raises(CinemaError):
        Cinema("Bad", 0, 5)
    with pytest.raises(CinemaError):
        Cinema("Bad", 5, 0)

# Test booking ID generation and reuse
def test_generate_booking_id_and_reuse():
    c = Cinema("Test", 2, 2)
    id1 = c.generate_booking_id()
    id2 = c.generate_booking_id()
    assert id1 == "GIC0001"
    assert id2 == "GIC0002"
    # Simulate booking and cancellation
    c.bookings[id1] = [(0,0)]
    c.cancel_booking(id1)
    id3 = c.generate_booking_id()
    assert id3 == "GIC0001"  # Reused

def test_generate_booking_id_gap():
    c = Cinema("Test", 2, 2)
    ids = [c.generate_booking_id() for _ in range(3)]
    c.bookings[ids[1]] = [(0,0)]
    c.cancel_booking(ids[1])
    new_id = c.generate_booking_id()
    assert new_id == ids[1]  # Should reuse the cancelled ID

# Test default seat selection
def test_generate_default_seats():
    c = Cinema("Test", 2, 3)
    seats = c.generate_default_seats(2)
    assert len(seats) == 2
    # Should be in the furthest row (row 1)
    assert all(r == 1 for r, _ in seats)

# Test error when not enough seats
def test_generate_default_seats_not_enough():
    c = Cinema("Test", 1, 2)
    c.seating[0][0] = '#'
    c.seating[0][1] = '#'
    with pytest.raises(InvalidSeatError):
        c.generate_default_seats(1)

# Test custom seating valid and invalid
def test_custom_seating_valid():
    c = Cinema("Test", 3, 3)
    seats = c.custom_seating(2, 2, 1)
    assert seats == [(2,1),(2,2)]

def test_custom_seating_invalid():
    c = Cinema("Test", 3, 3)
    with pytest.raises(InvalidSeatError):
        c.custom_seating(2, 3, 0)  # Invalid row
    with pytest.raises(InvalidSeatError):
        c.custom_seating(2, 0, 3)  # Invalid col

# Edge case: custom_seating overflow to next row
def test_custom_seating_overflow():
    c = Cinema("Test", 2, 2)
    seats = c.custom_seating(3, 1, 1)  # Should fill (1,1), (0,0), (0,1)
    assert (1,1) in seats and (0,0) in seats and (0,1) in seats

# Test confirm booking and error cases
def test_confirm_booking_success():
    c = Cinema("Test", 2, 2)
    booking_id = c.generate_booking_id()
    seats = [(1,0),(1,1)]
    result = c.confirm_booking(seats, booking_id)
    assert result == booking_id
    assert c.seating[1][0] == '#'
    assert c.seating[1][1] == '#'
    assert c.bookings[booking_id] == seats

def test_confirm_booking_seat_taken():
    c = Cinema("Test", 2, 2)
    booking_id = c.generate_booking_id()
    c.seating[1][0] = '#'
    seats = [(1,0),(1,1)]
    with pytest.raises(BookingError):
        c.confirm_booking(seats, booking_id)

def test_confirm_booking_invalid_seat():
    c = Cinema("Test", 2, 2)
    booking_id = c.generate_booking_id()
    seats = [(2,0)]  # Invalid row
    with pytest.raises(BookingError):
        c.confirm_booking(seats, booking_id)

def test_confirm_booking_no_seats():
    c = Cinema("Test", 2, 2)
    booking_id = c.generate_booking_id()
    with pytest.raises(BookingError):
        c.confirm_booking([], booking_id)

# Test cancel booking
def test_cancel_booking():
    c = Cinema("Test", 2, 2)
    booking_id = c.generate_booking_id()
    seats = [(1,0),(1,1)]
    c.confirm_booking(seats, booking_id)
    assert c.cancel_booking(booking_id)
    assert c.seating[1][0] == '.'
    assert c.seating[1][1] == '.'
    assert booking_id not in c.bookings

def test_cancel_nonexistent_booking():
    c = Cinema("Test", 2, 2)
    assert not c.cancel_booking("GIC9999")

# Test display seating
def test_display_seating_no_exception():
    c = Cinema("Test", 2, 2)
    try:
        c.display_seating()
    except Exception:
        pytest.fail("display_seating() raised an exception unexpectedly!")

def test_display_seating_with_temp_seats(capsys):
    c = Cinema("Test", 2, 2)
    temp_seats = [(1, 0), (1, 1)]
    c.display_seating(temp_seats)
    captured = capsys.readouterr()
    assert 'O' in captured.out

# Test check_booking prints invalid id
def test_check_booking_invalid_id(capsys):
    c = Cinema("Test", 2, 2)
    c.check_booking("BADID")
    captured = capsys.readouterr()
    assert "Invalid booking ID" in captured.out

def test_check_booking_valid_id(capsys):
    c = Cinema("Test", 2, 2)
    booking_id = c.generate_booking_id()
    seats = [(1,0),(1,1)]
    c.confirm_booking(seats, booking_id)
    c.check_booking(booking_id)
    captured = capsys.readouterr()
    assert f"Booking id: {booking_id}" in captured.out

# Edge case: try to overbook
def test_generate_default_seats_overbook():
    c = Cinema("Test", 2, 2)
    with pytest.raises(InvalidSeatError):
        c.generate_default_seats(5)
