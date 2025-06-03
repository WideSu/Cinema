from typing import List, Tuple, Optional

class CinemaError(Exception):
    """Base exception for cinema-related errors"""
    pass

class InvalidSeatError(CinemaError):
    """Raised when seat selection is invalid"""
    pass

class BookingError(CinemaError):
    """Raised when booking operations fail"""
    pass

class Cinema:
    def __init__(self, title: str, rows: int, seats_per_row: int):
        if rows <= 0 or seats_per_row <= 0:
            raise ValueError("Rows and seats per row must be positive integers")
        
        self.title = title
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.seating = [['.' for _ in range(seats_per_row)] for _ in range(rows)]
        self.bookings = {}  # booking_id: List[Tuple[row, col]]
        self.booking_counter = 1  # Start booking IDs from GIC0001
        self.used_booking_numbers = set()  # Track used booking numbers

    def generate_booking_id(self) -> str:
        """Find the smallest available booking ID"""
        # Start from 1 and find the first number not in used_booking_numbers
        booking_number = 1
        while booking_number in self.used_booking_numbers:
            booking_number += 1
        
        # Add to used set and return formatted ID
        self.used_booking_numbers.add(booking_number)
        return f"GIC{booking_number:04d}"
    
    def cancel_booking(self, booking_id: str) -> bool:
        """Cancel a booking and free up its ID for reuse"""
        if booking_id not in self.bookings:
            return False
        
        try:
            # Free up the seats
            seats = self.bookings[booking_id]
            for r, c in seats:
                self.seating[r][c] = '.'
            
            # Remove from bookings
            del self.bookings[booking_id]
            
            # Extract number from booking ID and remove from used set
            booking_number = int(booking_id[3:])  # Remove "GIC" prefix
            self.used_booking_numbers.discard(booking_number)
            
            return True
        except Exception as e:
            print(f"Error cancelling booking: {e}")
            return False
    
    def display_seating(self, temp_seats: List[Tuple[int, int]] = []):
        try:
            col_headers = "    " + "".join(f"{i+1:>4}" for i in range(self.seats_per_row))
            header_len = len(col_headers)
            screen_text = "S C R E E N"
            centered_screen_text = screen_text.center(header_len-6)
            print(" "*6 + centered_screen_text)
            print("-" * header_len)
            
            for i in range(self.rows):
                row_char = chr(ord('A') + self.rows - i - 1)
                row = f"{row_char:<4}"
                
                for j in range(self.seats_per_row):
                    if (i, j) in temp_seats:
                        symbol = 'O'
                    elif self.seating[i][j] == '#':
                        symbol = '#'
                    else:
                        symbol = '.'
                    row += f"{symbol:>4}"
                
                print(row)
            
            print(col_headers)
        except Exception as e:
            print(f"Error displaying seating chart: {e}")

    def generate_default_seats(self, count: int) -> List[Tuple[int, int]]:
        if count <= 0:
            raise ValueError("Number of seats must be positive")
        
        if count > self.rows * self.seats_per_row:
            raise InvalidSeatError(f"Cannot book {count} seats. Maximum capacity is {self.rows * self.seats_per_row}")
        
        try:
            selected_seats = []
            seats_needed = count
            
            # Start from the furthest row (highest row index) and work towards the screen
            for row in reversed(range(self.rows)):
                if seats_needed == 0:
                    break
                
                # Find all available seats in this row
                available_seats = [col for col in range(self.seats_per_row) 
                                if self.seating[row][col] == '.']
                
                if not available_seats:
                    continue  # Skip fully occupied rows
                
                # Start from middle-most position and work outwards
                # For even number of seats, use left-center (e.g., for 10 seats, use seat 5 not 6)
                mid_col = (self.seats_per_row - 1) // 2
                
                # Create a list of columns ordered by distance from middle
                cols_by_distance = []
                
                # Add middle column first if available
                if mid_col in available_seats:
                    cols_by_distance.append(mid_col)
                    available_seats.remove(mid_col)
                
                # Add remaining columns by alternating left and right from center
                left_offset = 1
                right_offset = 1
                
                while available_seats:
                    # Try right side
                    right_col = mid_col + right_offset
                    if right_col < self.seats_per_row and right_col in available_seats:
                        cols_by_distance.append(right_col)
                        available_seats.remove(right_col)
                    
                    # Try left side
                    left_col = mid_col - left_offset
                    if left_col >= 0 and left_col in available_seats:
                        cols_by_distance.append(left_col)
                        available_seats.remove(left_col)
                    
                    left_offset += 1
                    right_offset += 1
                
                # Take seats from this row up to what we need
                for col in cols_by_distance:
                    if seats_needed > 0:
                        selected_seats.append((row, col))
                        seats_needed -= 1
                    else:
                        break
            
            if seats_needed > 0:
                raise InvalidSeatError(f"Only found {count - seats_needed} available seats, but {count} requested")
            
            return selected_seats
        except Exception as e:
            if isinstance(e, InvalidSeatError):
                raise
            raise InvalidSeatError(f"Error finding default seats: {e}")

    def custom_seating(self, count: int, start_row: int, start_col: int) -> List[Tuple[int, int]]:
        # print(f"DEBUG: Requesting {count} seats starting at row {start_row}, col {start_col}")
        if count <= 0:
            raise ValueError("Number of seats must be positive")
        
        # Validate starting position
        if not (0 <= start_row < self.rows):
            raise InvalidSeatError(f"Invalid row index: {start_row}")
        if not (0 <= start_col < self.seats_per_row):
            raise InvalidSeatError(f"Invalid column index: {start_col}")
        
        selected_seats = []
        seats_needed = count
        
        # First: Fill the specified row from the specified position to the right
        for col in range(start_col, self.seats_per_row):
            if seats_needed > 0 and self.seating[start_row][col] == '.':
                selected_seats.append((start_row, col))
                seats_needed -= 1
        
        # If we need more seats, overflow to next rows closer to the screen
        # Start from the immediate next row closer to screen and work our way forward
        current_row = start_row - 1  # Next row closer to screen
        
        while seats_needed > 0 and current_row >= 0:
            # Find all available seats in this row
            available_seats = [col for col in range(self.seats_per_row) 
                             if self.seating[current_row][col] == '.']
            
            if not available_seats:
                current_row -= 1  # Move to next row closer to screen
                continue
            
            # For overflow rows, use default seating logic (center outward)
            # For even number of seats, use left-center (e.g., for 10 seats, use seat 5 not 6)
            mid_col = (self.seats_per_row - 1) // 2
            
            # Create a list of columns ordered by distance from middle
            cols_by_distance = []
            
            # Add middle column first if available
            if mid_col in available_seats:
                cols_by_distance.append(mid_col)
                available_seats.remove(mid_col)
            
            # Add remaining columns by alternating left and right from center
            left_offset = 1
            right_offset = 1
            
            while available_seats:
                # Try right side
                right_col = mid_col + right_offset
                if right_col < self.seats_per_row and right_col in available_seats:
                    cols_by_distance.append(right_col)
                    available_seats.remove(right_col)
                
                # Try left side
                left_col = mid_col - left_offset
                if left_col >= 0 and left_col in available_seats:
                    cols_by_distance.append(left_col)
                    available_seats.remove(left_col)
                
                left_offset += 1
                right_offset += 1
            
            # Take seats from this row up to what we need
            for col in cols_by_distance:
                if seats_needed > 0:
                    selected_seats.append((current_row, col))
                    seats_needed -= 1
                else:
                    break
            
            # Move to next row closer to screen
            current_row -= 1
        
        if seats_needed > 0:
            raise InvalidSeatError(f"Only {len(selected_seats)} seats available, but {count} requested")
        
        return selected_seats

    def confirm_booking(self, seats: List[Tuple[int, int]], booking_id) -> str:
        if not seats:
            raise BookingError("No seats to book")
        
        # Validate all seats before booking
        for r, c in seats:
            if not (0 <= r < self.rows and 0 <= c < self.seats_per_row):
                raise BookingError(f"Invalid seat position: ({r}, {c})")
            
            if self.seating[r][c] != '.':
                raise BookingError(f"Seat ({r}, {c}) is already occupied")
        
        try:
            # Mark seats as booked
            for r, c in seats:
                self.seating[r][c] = '#'
            self.bookings[booking_id] = seats
            
            return booking_id
        except Exception as e:
            # Rollback changes if booking fails
            for r, c in seats:
                self.seating[r][c] = '.'
            raise BookingError(f"Failed to confirm booking: {e}")

    def check_booking(self, booking_id: str):
        if not booking_id or not booking_id.strip():
            print("Error: Booking ID cannot be empty")
            return
        
        booking_id = booking_id.strip()
        
        if booking_id in self.bookings:
            try:
                print(f"Booking id: {booking_id}\nSelected seats:")
                self.display_seating()
            except Exception as e:
                print(f"Error displaying booking: {e}")
        else:
            print("Invalid booking ID. Please check and try again.")