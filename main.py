import uuid
import math
from typing import List, Tuple, Optional

from .models import Cinema, InvalidSeatError, BookingError

def main():
    try:
        # Get cinema setup with error handling
        while True:
            try:
                user_input = input("Enter movie title, number of rows, and seats per row (separated by space):\n>").strip()
                parts = user_input.split()
                
                if len(parts) != 3:
                    print("Please enter exactly 3 values: title, rows, seats_per_row")
                    continue
                
                title, rows_str, seats_str = parts
                rows = int(rows_str)
                seats_per_row = int(seats_str)
                
                if rows <= 0 or seats_per_row <= 0:
                    print("Rows and seats must be positive numbers.")
                    continue
                
                if rows > 26:  # Limit to A-Z
                    print("Maximum 26 rows supported (A-Z).")
                    continue
                
                cinema = Cinema(title, rows, seats_per_row)
                break
                
            except ValueError as e:
                print(f"Invalid input: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}. Please try again.")

        # Main application loop
        while True:
            try:
                print("Welcome to GIC Cinemas!")
                print("[1] Book Tickets")
                print("[2] Check Booking")
                print("[3] Exit")
                
                choice = input("Select an option (1-3):\n>").strip()

                if choice == '1':
                    try:
                        # Get number of tickets
                        num_tickets = get_valid_input(
                            "Enter number of tickets:\n>",
                            int,
                            lambda x: 0 < x <= cinema.rows * cinema.seats_per_row,
                            f"Number must be between 1 and {cinema.rows * cinema.seats_per_row}"
                        )
                        # Generate booking ID
                        booking_id = cinema.generate_booking_id()
                        # Generate default seats
                        try:
                            default_seats = cinema.generate_default_seats(num_tickets)
                            print(f"\nSuccessfully reserved {num_tickets} {title} tickets.\nBooking ID: {booking_id}\nSelected seats:")
                            cinema.display_seating(default_seats)
                        except InvalidSeatError as e:
                            print(f"Error: {e}")
                            continue
                        
                        # Get user's seating preference
                        while True:
                            try:
                                pos = input("Press Enter to accept default, or enter seat position (e.g., A5):\n>").strip()
                                
                                if pos == '':
                                    selected = default_seats
                                    break
                                
                                # Parse custom position
                                row_index, col_index = parse_seat_position(pos, cinema.rows, cinema.seats_per_row)
                                selected = cinema.custom_seating(num_tickets, row_index, col_index)
                                
                                print(f"\nBooking ID: {booking_id}\nSelected seats:")
                                cinema.display_seating(selected)
                                
                                # FIXED: Ask for confirmation for custom seating
                                confirm_input = input("Press Enter to accept this selection, or enter another seat position:\n>").strip()
                                if confirm_input == '':
                                    break
                                else:
                                    # User wants to try a different position
                                    pos = confirm_input
                                    row_index, col_index = parse_seat_position(pos, cinema.rows, cinema.seats_per_row)
                                    selected = cinema.custom_seating(num_tickets, row_index, col_index)
                                    print(f"\nBooking ID: {booking_id}\nSelected seats:")
                                    cinema.display_seating(selected)
                                    continue

                            except (ValueError, InvalidSeatError) as e:
                                print(f"Error: {e}")
                                # Continue the loop to let user try again
                                continue
                        
                        # Confirm booking
                        if 'selected' in locals() and selected:
                            try:
                                booking_id = cinema.confirm_booking(selected, booking_id)
                                print(f"Booking ID: {booking_id} confirmed.")
                            except BookingError as e:
                                print(f"Booking failed: {e}")
                        
                    except ValueError as e:
                        print(f"Input error: {e}")
                    except Exception as e:
                        print(f"Unexpected error during booking: {e}")

                elif choice == '2':
                    try:
                        booking_id = input("Enter your booking ID:\n>").strip()
                        cinema.check_booking(booking_id)
                    except Exception as e:
                        print(f"Error checking booking: {e}")

                elif choice == '3':
                    print("Thank you for using GIC Cinemas. Bye!")
                    cinema.cancel_booking(booking_id)
                    break
                    
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
                    
            except KeyboardInterrupt:
                print("\n\n Exiting... Thank you for using GIC Cinemas!")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                print("Please try again or contact support.")

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"Fatal error: {e}")
        print("Application will now exit.")

if __name__ == '__main__':
    main()