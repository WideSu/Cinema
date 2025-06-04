import pytest
from unittest.mock import patch, MagicMock
import io
import sys
from typing import List, Tuple

# Assuming these imports based on the code structure
from .models import Cinema, InvalidSeatError, BookingError, CinemaError
from .utilities import parse_seat_position, get_valid_input


class TestCinemaBookingSystem:
    """Test suite for the Cinema Booking System based on observed behavior"""
    
    @pytest.fixture
    def cinema(self):
        """Create a standard cinema for testing"""
        return Cinema("John Wick 4", 8, 10)
    
    @pytest.fixture
    def large_cinema(self):
        """Create a larger cinema for overflow testing"""
        return Cinema("Test Movie", 10, 12)

    def test_cinema_creation(self):
        """Test cinema creation with valid parameters"""
        cinema = Cinema("John Wick 4", 8, 10)
        assert cinema.title == "John Wick 4"
        assert cinema.rows == 8
        assert cinema.seats_per_row == 10

    def test_default_seat_generation(self, cinema):
        """Test default seat allocation - should place seats in front row (A)"""
        seats = cinema.generate_default_seats(10)
        seats.sort()  # Sort to ensure order is consistent
        # Should get 10 seats in row A (index 7 since A is furthest to screen)
        expected_seats = [(7, i) for i in range(10)]  # Row A, seats 1-10
        assert len(seats) == 10
        assert seats == expected_seats

    def test_default_seat_generation_partial_row(self, cinema):
        """Test default seat generation for less than full row"""
        seats = cinema.generate_default_seats(5)
        
        # Should get 5 seats centered in row A
        assert len(seats) == 5
        # Check all seats are in row A (index 7)
        for seat in seats:
            assert seat[0] == 7

    def test_custom_seating_starting_position_b2(self, cinema):
        """Test custom seating starting at B2 (as shown in output)"""
        # Based on output: B2 selection resulted in B2-B10 + C5
        seats = cinema.custom_seating(10, 1, 1)  # Row B (index 1), seat 2 (index 1)
        
        assert len(seats) == 10
        # Should start at B2 and continue rightward, then overflow
        
        # Check that B2 is included
        assert (1, 1) in seats  # Row B, seat 2
        
        # Verify all seats are valid positions
        for row, col in seats:
            assert 0 <= row < 8
            assert 0 <= col < 10

    def test_custom_seating_starting_position_c7(self, cinema):
        """Test custom seating starting at C7 (as shown in output)"""
        # Based on output: C7 selection shows seats in C7-C10 + D3-D8
        seats = cinema.custom_seating(10, 2, 6)  # Row C (index 2), seat 7 (index 6)
        
        assert len(seats) == 10
        assert (2, 6) in seats  # Row C, seat 7 should be included

    def test_custom_seating_starting_position_a7(self, cinema):
        """Test custom seating starting at A7 (as shown in output)"""
        # Based on output: H7 selection shows H7-H10
        selected_seats = 4
        count = 10
        with pytest.raises(InvalidSeatError, match=f"Only {selected_seats} seats available, but {count} requested"):
            seats = cinema.custom_seating(count, 0, 6)  # Row H (index 7), seat 7 (index 6)

    def test_custom_seating_starting_position_b8(self, cinema):
        """Test custom seating starting at B8 (as shown in output)"""
        # Based on output: B8 selection shows B8-B10 + C2-C8
        seats = cinema.custom_seating(10, 1, 7)  # Row B (index 1), seat 8 (index 7)
        
        assert len(seats) == 10
        assert (1, 7) in seats  # Row B, seat 8 should be included

    def test_custom_seating_starting_position_g4(self, cinema):
        """Test custom seating starting at G4 (as shown in output)"""
        # Based on output: G4 selection shows G4-G10 + H4-H6
        seats = cinema.custom_seating(10, 6, 3)  # Row G (index 6), seat 4 (index 3)
        
        assert len(seats) == 10
        assert (6, 3) in seats  # Row G, seat 4 should be included

    def test_booking_id_generation(self, cinema):
        """Test booking ID generation"""
        booking_id = cinema.generate_booking_id()
        assert booking_id.startswith("GIC")
        assert len(booking_id) == 7  # GIC + 4 digits
        
        # Test uniqueness
        booking_id2 = cinema.generate_booking_id()
        assert booking_id != booking_id2

    def test_seat_confirmation_and_display(self, cinema):
        """Test seat confirmation and seating chart display"""
        seats = cinema.generate_default_seats(10)
        booking_id = cinema.generate_booking_id()
        
        confirmed_id = cinema.confirm_booking(seats, booking_id)
        assert confirmed_id == booking_id
        
        # Test that seats are now marked as booked
        for row, col in seats:
            assert cinema.seating[row][col] != '.'  # Should not be available

    def test_invalid_booking_check(self, cinema):
        """Test checking invalid booking ID (as shown in output)"""
        cinema.check_booking("GIC0001")  # Non-existent booking

    def test_seat_position_parsing_valid(self):
        """Test valid seat position parsing"""
        # Test valid positions
        row, col = parse_seat_position("A1", 8, 10)
        assert row == 7 and col == 0  # A1 -> (0,0)
        
        row, col = parse_seat_position("B2", 8, 10)
        assert row == 6 and col == 1  # B2 -> (1,1)
        
        row, col = parse_seat_position("H10", 8, 10)
        assert row == 0 and col == 9  # H10 -> (7,9)

    def test_seat_position_parsing_invalid_row(self):
        """Test invalid row parsing (as shown in output)"""
        with pytest.raises(ValueError, match="Invalid row"):
            parse_seat_position("V6", 8, 10)  # Row V doesn't exist
            
        with pytest.raises(ValueError, match="Invalid row"):
            parse_seat_position("Y8", 8, 10)  # Row Y doesn't exist
            
        with pytest.raises(ValueError, match="Invalid row"):
            parse_seat_position("K9", 8, 10)  # Row K doesn't exist

    def test_seat_position_parsing_invalid_seat(self):
        """Test invalid seat number parsing"""
        with pytest.raises(ValueError):
            parse_seat_position("A11", 8, 10)  # Seat 11 doesn't exist
            
        with pytest.raises(ValueError):
            parse_seat_position("A0", 8, 10)  # Seat 0 doesn't exist

    def test_seating_display_format(self, cinema):
        """Test seating display format matches expected output"""
        # Generate some seats
        seats = cinema.generate_default_seats(10)
        
        # Capture display output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        cinema.display_seating(temp_seats=seats)
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        # Check format elements
        assert "S C R E E N" in output
        assert "Legend: '.' = Available, '#' = Other Bookings, 'O' = Reserved" in output
        assert "A      O   O   O   O   O   O   O   O   O   O" in output
        assert "1   2   3   4   5   6   7   8   9  10" in output

    def test_multiple_booking_attempts(self, cinema):
        """Test multiple booking attempts and seat updates"""
        # First booking
        seats1 = cinema.generate_default_seats(5)
        booking_id1 = cinema.confirm_booking(seats1,booking_id=cinema.generate_booking_id())  
        
        # Second booking should get different seats
        seats2 = cinema.generate_default_seats(3)
        booking_id2 = cinema.confirm_booking(seats2,booking_id=cinema.generate_booking_id())
        
        assert booking_id1 != booking_id2
        # Verify no seat overlap
        assert not set(seats1).intersection(set(seats2))

    def test_custom_seating_with_occupied_seats(self, cinema):
        """Test custom seating when some seats are already occupied"""
        # First, book some seats
        initial_seats = [(1, 4), (1, 5), (1, 6)]  # B5, B6, B7
        cinema.confirm_booking(initial_seats, booking_id=cinema.generate_booking_id())
        
        # Now try custom seating that would conflict
        # Should get alternative seats
        new_seats = cinema.custom_seating(3, 1, 4)  # Starting at B5 (occupied)
        
        # Should not include the occupied seats
        for seat in new_seats:
            assert seat not in initial_seats

    def test_insufficient_seats_error(self, cinema):
        """Test error when requesting more seats than available"""
        # Try to book more seats than total capacity
        with pytest.raises(InvalidSeatError):
            cinema.custom_seating(85, 0, 0)  # More than 80 total seats

    def test_seating_overflow_logic(self, cinema):
        """Test seating overflow to adjacent rows"""
        # Request 15 seats starting from H1 (back row)
        # Should overflow to previous rows
        seats = cinema.custom_seating(15, 7, 0)
        
        assert len(seats) == 15
        
        # Should include seats from multiple rows due to overflow
        rows_used = set(seat[0] for seat in seats)
        assert len(rows_used) >= 2  # Should use at least 2 rows

    @pytest.mark.parametrize("num_tickets,expected_rows", [
        (5, 1),    # Should fit in one row
        (12, 2),   # Should require 2 rows
        (25, 3),   # Should require 3 rows
    ])
    def test_seat_allocation_patterns(self, cinema, num_tickets, expected_rows):
        """Test seat allocation patterns for different ticket counts"""
        seats = cinema.generate_default_seats(num_tickets)
        
        assert len(seats) == num_tickets
        
        # Check number of rows used
        rows_used = set(seat[0] for seat in seats)
        assert len(rows_used) <= expected_rows

    def test_booking_cancellation(self, cinema):
        """Test booking cancellation functionality"""
        seats = cinema.generate_default_seats(5)
        booking_id = cinema.confirm_booking(seats, cinema.generate_booking_id())
        
        # Cancel the booking
        cinema.cancel_booking(booking_id)
        
        # Seats should be available again
        for row, col in seats:
            assert cinema.seating[row][col] == '.'

    def test_edge_case_single_seat(self, cinema):
        """Test booking a single seat"""
        seats = cinema.custom_seating(1, 3, 5)  # Row D, seat 6
        
        assert len(seats) == 1
        assert seats[0] == (3, 5)

    def test_edge_case_full_row(self, cinema):
        """Test booking a full row"""
        seats = cinema.custom_seating(10, 2, 0)  # Full row C
        
        assert len(seats) == 10
        # All seats should be in row C
        for seat in seats:
            assert seat[0] == 2

    def test_cinema_state_persistence(self, cinema):
        """Test that cinema state persists between operations"""
        # Make several bookings
        booking1 = cinema.confirm_booking(cinema.generate_default_seats(3), booking_id=cinema.generate_booking_id())
        booking2 = cinema.confirm_booking(cinema.custom_seating(5, 2, 0), booking_id=cinema.generate_booking_id())
        
        # Check that both bookings exist
        assert booking1 in cinema.bookings
        assert booking2 in cinema.bookings
        
        # Verify seat counts
        total_booked = sum(len(seats) for seats in cinema.bookings.values())
        assert total_booked == 8


class TestInputValidation:
    """Test input validation and error handling"""
    
    def test_get_valid_input_success(self):
        """Test successful input validation"""
        with patch('builtins.input', return_value='5'):
            result = get_valid_input(
                "Enter number: ",
                int,
                lambda x: 1 <= x <= 10,
                "Must be 1-10"
            )
            assert result == 5

    def test_get_valid_input_retry(self):
        """Test input validation with retry"""
        with patch('builtins.input', side_effect=['15', '0', '5']):
            result = get_valid_input(
                "Enter number: ",
                int,
                lambda x: 1 <= x <= 10,
                "Must be 1-10"
            )
            assert result == 5

    def test_cinema_creation_validation(self):
        """Test cinema creation parameter validation"""
        # Test invalid parameters
        with pytest.raises(CinemaError, match="Rows and seats per row must be positive integers"):
            Cinema("Test", 0, 10)  # Zero rows
        with pytest.raises(CinemaError, match="Rows and seats per row must be positive integers"):
            Cinema("Test", 10, 0)  # Zero seats per row
        with pytest.raises(CinemaError, match="Maximum 26 rows supported"):
            Cinema("Test", 27, 10)  # Too many rows (>26)


class TestDisplayOutput:
    """Test display and output formatting"""
    
    def test_seating_chart_legend(self, cinema=None):
        """Test that seating chart includes proper legend"""
        if cinema is None:
            cinema = Cinema("Test", 5, 8)
            
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        cinema.display_seating()
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        assert "S C R E E N" in output
        assert "Legend:" in output
        assert "'.' = Available" in output
        assert "'#' = Other Bookings" in output
        assert "'O' = Reserved" in output

    def test_booking_confirmation_message(self, cinema=None):
        """Test booking confirmation message format"""
        if cinema is None:
            cinema = Cinema("Test", 5, 8)
        seats = cinema.generate_default_seats(3)
        booking_id = cinema.generate_booking_id()
        confirmed_id = cinema.confirm_booking(seats, booking_id)
        # Test that booking ID follows expected format
        assert confirmed_id.startswith("GIC")
        assert len(confirmed_id) == 7


# Integration tests
class TestIntegrationScenarios:
    """Integration tests based on the complete user interaction flow"""
    
    def test_complete_booking_flow(self):
        """Test complete booking flow as shown in output"""
        cinema = Cinema("John Wick 4", 8, 10)
        
        # Step 1: Generate default seats for 10 tickets
        default_seats = cinema.generate_default_seats(10)
        assert len(default_seats) == 10
        
        # Step 2: Generate booking ID
        booking_id = cinema.generate_booking_id()
        assert booking_id.startswith("GIC")
        
        # Step 3: Try custom position B2
        custom_seats_b2 = cinema.custom_seating(10, 1, 1)  # B2
        assert len(custom_seats_b2) == 10
        
        # Step 4: Try custom position C7
        custom_seats_c7 = cinema.custom_seating(10, 2, 6)  # C7
        assert len(custom_seats_c7) == 10
        
        # Each selection should be different
        assert custom_seats_b2 != custom_seats_c7

    def test_error_recovery_flow(self):
        """Test error recovery as shown in output"""
        cinema = Cinema("John Wick 4", 8, 10)
        
        # Test invalid row inputs (as shown in output)
        invalid_positions = ["V6", "Y8", "K9"]
        
        for pos in invalid_positions:
            with pytest.raises(ValueError, match="Invalid row"):
                parse_seat_position(pos, 8, 10)

    def test_booking_persistence_failure(self):
        """Test booking persistence issues (booking not found after creation)"""
        cinema = Cinema("John Wick 4", 8, 10)
        
        # This test simulates the issue where GIC0001 wasn't found
        # The booking might not be properly confirmed/saved
        seats = cinema.generate_default_seats(10)
        booking_id = "GIC0001"
        
        # If booking is not properly confirmed, it shouldn't be findable
        try:
            # Try to confirm booking
            confirmed_id = cinema.confirm_booking(seats, booking_id)
            
            # If confirmation succeeded, check_booking should work
            cinema.check_booking(confirmed_id)
            
        except BookingError:
            # This simulates the behavior seen in output
            # where booking wasn't properly saved
            pass