from typing import Tuple

from settings import MAX_TRIES


def get_valid_input(prompt: str, input_type: type, validation_func=None, error_msg: str = None) -> any:
    """Get valid input with proper error handling"""
    max_attempts = MAX_TRIES
    attempts = 0
    
    while attempts < max_attempts:
        try:
            user_input = input(prompt).strip()
            
            if not user_input and input_type != str:
                print("Input cannot be empty. Please try again.")
                attempts += 1
                continue
            
            converted = input_type(user_input)
            
            if validation_func and not validation_func(converted):
                print(error_msg or "Invalid input. Please try again.")
                attempts += 1
                continue
                
            return converted
            
        except ValueError as e:
            print(f"Invalid input format. Expected {input_type.__name__}. Please try again.")
            attempts += 1
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")
            attempts += 1
    
    raise ValueError(f"Failed to get valid input after {max_attempts} attempts")

def parse_seat_position(pos: str, rows: int, seats_per_row: int) -> Tuple[int, int]:
    """Parse seat position string and return row, col indices"""
    pos = pos.strip().upper()
    
    if len(pos) < 2:
        raise ValueError("Seat position must include both row and column (e.g., A5)")
    
    row_str = pos[0]
    col_str = pos[1:]
    
    # Validate row
    if not row_str.isalpha():
        raise ValueError("Row must be a letter")
    
    if ord(row_str) < ord('A') or ord(row_str) >= ord('A') + rows:
        raise ValueError(f"Invalid row '{row_str}'. Use A-{chr(ord('A') + rows - 1)}")
    
    # Validate column
    try:
        col_num = int(col_str)
        if col_num < 1 or col_num > seats_per_row:
            raise ValueError(f"Invalid column '{col_str}'. Use 1-{seats_per_row}")
    except ValueError:
        raise ValueError(f"Column must be a number between 1-{seats_per_row}")
    
    # FIXED: Correct row index calculation
    row_index = rows - 1 - (ord(row_str) - ord('A'))
    col_index = col_num - 1
    
    return row_index, col_index