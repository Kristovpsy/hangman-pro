import string
import random
import pathlib
from typing import Dict, Any, Tuple, Optional
from display import (
    display_login_header, display_register_header, 
    display_password_requirements, get_user_name
)

def create_account(name: str, username: str, password: str) -> Dict[str, Any]:
    """
    Create a new account dictionary with all required fields.
    
    Args:
        name (str): Display name for the account
        username (str): Unique username for login
        password (str): Account password
        
    Returns:
        Dict[str, Any]: Complete account dictionary with statistics initialized to zero
    """
    return {
        "name": name,
        "username": username,
        "password": password,
        "wins": 0,                  # Total lifetime wins
        "losses": 0,                # Total lifetime losses
        "plays": 0,                 # Total lifetime games played
        "session_wins": 0,          # Wins in current session
        "session_losses": 0,        # Losses in current session
        "session_plays": 0          # Games played in current session
    }

def create_guest_account(name: str) -> Dict[str, Any]:
    """
    Create a temporary guest account (not saved to file).
    
    Args:
        name (str): Guest's display name
        
    Returns:
        Dict[str, Any]: Guest account dictionary
    """
    return create_account(name, "guest", "")

def add_session_to_totals(account: Dict[str, Any]) -> None:
    """
    Add current session statistics to lifetime totals.
    Called when user logs out or exits.
    
    Args:
        account (Dict[str, Any]): Account dictionary to update
    """
    account["wins"] += account["session_wins"]
    account["losses"] += account["session_losses"]
    account["plays"] += account["session_plays"]
    
    # Reset session counters (optional - depends on requirements)
    # account["session_wins"] = 0
    # account["session_losses"] = 0
    # account["session_plays"] = 0

def validate_password(password: str) -> bool:
    """
    Validate password meets all security requirements.
    
    Args:
        password (str): Password to validate
        
    Returns:
        bool: True if password meets all requirements
        
    Requirements:
    - At least one lowercase letter
    - At least one uppercase letter  
    - At least one digit
    - At least one symbol
    - Maximum 16 characters
    """
    if len(password) > 16 or len(password) < 1:
        return False
    
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)
    
    return has_lower and has_upper and has_digit and has_symbol

def generate_password() -> str:
    """
    Generate a secure password that meets all requirements.
    
    Returns:
        str: Generated secure password (12 characters)
    """
    lower = string.ascii_lowercase      # a-z
    upper = string.ascii_uppercase      # A-Z
    digits = string.digits             # 0-9
    symbols = "!@#$%^&*"              # Safe symbols (avoiding problematic ones)
    
    # Ensure at least one of each required character type
    password = [
        random.choice(lower),
        random.choice(upper),
        random.choice(digits),
        random.choice(symbols)
    ]
    
    # Add 8 more random characters from all allowed types
    all_chars = lower + upper + digits + symbols
    for _ in range(8):
        password.append(random.choice(all_chars))
    
    # Shuffle to avoid predictable pattern
    random.shuffle(password)
    return ''.join(password)

def handle_max_attempts(process: str, accounts: Dict[str, Dict[str, Any]], 
                       accounts_file: pathlib.Path, current_user: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Handle situation when user reaches maximum login/registration attempts.
    
    Args:
        process (str): Either "login" or "registration" 
        accounts (Dict[str, Dict[str, Any]]): All user accounts
        accounts_file (pathlib.Path): Path to accounts JSON file
        current_user (Dict[str, Any]): Current user account
        
    Returns:
        Tuple[bool, Optional[Dict[str, Any]]]: (Success status, Updated current user or None)
    """
    print(f"\nMaximum attempts reached for {process}.")
    while True:
        choice = input("Would you like to (1) Try again or (2) Return to main menu? Enter 1 or 2: ").strip()
        if choice == "1":
            # Retry the process
            if process == "login":
                return login_user(accounts, accounts_file, current_user)
            else:
                return register_user(accounts, accounts_file, current_user)
        elif choice == "2":
            # Return to main menu
            return False, current_user
        print("Invalid choice. Please enter 1 or 2.")

def login_user(accounts: Dict[str, Dict[str, Any]], accounts_file: pathlib.Path, 
               current_user: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """
    Handle complete user login process with attempt limits.
    
    Args:
        accounts (Dict[str, Dict[str, Any]]): All user accounts
        accounts_file (pathlib.Path): Path to accounts JSON file
        current_user (Dict[str, Any]): Current user account
        
    Returns:
        Tuple[bool, Dict[str, Any]]: (Login success status, Updated current user)
    """
    display_login_header()
    
    username_attempts = 0
    password_attempts = 0
    
    # Step 1: Username validation (up to 5 attempts)
    while username_attempts < 5:
        username = input("Enter username: ").strip()
        if username in accounts:
            break  # Valid username found
        print("Username not found. Please try again.")
        username_attempts += 1
    else:
        # Exceeded username attempts
        return handle_max_attempts("login", accounts, accounts_file, current_user)
    
    # Step 2: Password validation (up to 5 attempts)  
    while password_attempts < 5:
        password = input("Enter password: ").strip()
        if accounts[username]["password"] == password:
            # Login successful!
            
            # Step 3: Transfer guest session data if applicable
            if current_user["username"] == "guest":
                accounts[username]["session_wins"] += current_user["session_wins"]
                accounts[username]["session_losses"] += current_user["session_losses"]
                accounts[username]["session_plays"] += current_user["session_plays"]
            
            current_user = accounts[username]
            print(f"\nLogin successful! Welcome back, {current_user['name']}!")
            return True, current_user
            
        print("Incorrect password. Please try again.")
        password_attempts += 1
    else:
        # Exceeded password attempts
        return handle_max_attempts("login", accounts, accounts_file, current_user)

def register_user(accounts: Dict[str, Dict[str, Any]], accounts_file: pathlib.Path, 
                  current_user: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """
    Handle complete user registration process with validation.
    
    Args:
        accounts (Dict[str, Dict[str, Any]]): All user accounts
        accounts_file (pathlib.Path): Path to accounts JSON file  
        current_user (Dict[str, Any]): Current user account
        
    Returns:
        Tuple[bool, Dict[str, Any]]: (Registration success status, New user account)
    """
    from storage import save_accounts  # Import here to avoid circular import
    
    display_register_header()
    
    username_attempts = 0
    password_attempts = 0
    
    # Step 1: Username selection (up to 5 attempts)
    while username_attempts < 5:
        username = input("Enter desired username: ").strip()
        if username and username not in accounts:
            break  # Valid unique username
        if username in accounts:
            print("Username already taken. Please choose another.")
        else:
            print("Username cannot be empty. Please try again.")
        username_attempts += 1
    else:
        # Exceeded username attempts
        return handle_max_attempts("registration", accounts, accounts_file, current_user)
    
    # Step 2: Password setup - manual or automatic
    password_choice = input("\nWould you like to (1) Enter password manually or (2) Generate automatically? Enter 1 or 2: ").strip()
    
    if password_choice == "2":
        # Auto-generate secure password
        password = generate_password()
        print(f"\nGenerated password: {password}")
        print("Please save this password securely!")
    else:
        # Manual password entry with validation
        display_password_requirements()
        
        while password_attempts < 5:
            password = input("Enter password: ").strip()
            if validate_password(password):
                break  # Password meets requirements
            print("Password does not meet requirements. Please try again.")
            password_attempts += 1
        else:
            # Exceeded password attempts
            return handle_max_attempts("registration", accounts, accounts_file, current_user)
    
    # Step 3: Get display name
    name = input("Enter your display name: ").strip()
    if not name:
        name = username  # Use username as display name if not provided
    
    # Step 4: Create new account
    new_account = create_account(name, username, password)
    
    # Step 5: Transfer guest session data if applicable
    if current_user["username"] == "guest":
        new_account["session_wins"] = current_user["session_wins"]
        new_account["session_losses"] = current_user["session_losses"]
        new_account["session_plays"] = current_user["session_plays"]
    
    # Step 6: Save the new account
    accounts[username] = new_account
    save_accounts(accounts, accounts_file)
    
    print(f"\nRegistration successful! Welcome, {name}!")
    return True, new_account

def logout_user(current_user: Dict[str, Any], accounts: Dict[str, Dict[str, Any]], 
                accounts_file: pathlib.Path) -> Dict[str, Any]:
    """
    Handle user logout - save progress and return to guest mode.
    
    Args:
        current_user (Dict[str, Any]): Current logged-in user
        accounts (Dict[str, Dict[str, Any]]): All user accounts
        accounts_file (pathlib.Path): Path to accounts JSON file
        
    Returns:
        Dict[str, Any]: New guest account
    """
    from storage import save_accounts  # Import here to avoid circular import
    
    if current_user["username"] != "guest":
        # Add session statistics to permanent totals
        add_session_to_totals(current_user)
        
        # Save updated account data
        save_accounts(accounts, accounts_file)
        
        print(f"\nGoodbye, {current_user['name']}!")
        print("Your progress has been saved.")
    
    # Create new guest account
    guest_name = get_user_name()
    return create_guest_account(guest_name)

def get_account_summary(account: Dict[str, Any]) -> str:
    """
    Get a formatted summary of account statistics.
    
    Args:
        account (Dict[str, Any]): Account to summarize
        
    Returns:
        str: Formatted account summary
    """
    total_games = account["plays"]
    win_rate = (account["wins"] / total_games * 100) if total_games > 0 else 0
    
    return f"""
Account Summary for {account['name']}:
- Total Games: {total_games}
- Total Wins: {account['wins']}
- Total Losses: {account['losses']}
- Win Rate: {win_rate:.1f}%
- Current Session: {account['session_plays']} games, {account['session_wins']} wins
"""

