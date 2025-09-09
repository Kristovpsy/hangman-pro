"""
Hangman Game - Main Program Controller
This is the entry point of the Hangman game application.
It coordinates all other modules and handles the main game loop.
"""

from typing import Dict, Any

# Import all the modules we created
from display import display_welcome, display_main_menu, get_menu_choice, get_user_name
from game_logic import play_game
from accounts import (
    create_guest_account, login_user, register_user, logout_user, 
    add_session_to_totals
)
from storage import setup_accounts_file, load_accounts, save_accounts


def exit_game(current_user: Dict[str, Any], accounts: Dict[str, Dict[str, Any]], 
              accounts_file) -> None:
    """
    Handle complete game exit with proper data saving.
    
    Args:
        current_user (Dict[str, Any]): Current user account
        accounts (Dict[str, Dict[str, Any]]): All user accounts
        accounts_file: Path to accounts JSON file
    """
    if current_user["username"] != "guest":
        # Save registered user's progress before exiting
        add_session_to_totals(current_user)
        save_accounts(accounts, accounts_file)
        print(f"\nGoodbye, {current_user['name']}! Your progress has been saved.")
    else:
        # Guest user - no saving needed
        print(f"\nGoodbye, {current_user['name']}!")
    
    print("Thank you for playing Hangman!")


def main() -> None:
    """
    Main game loop and entry point of the application.
    Coordinates all modules and handles the primary game flow.
    """
    try:
        # Step 1: Initialize file system and load data
        print("Initializing Hangman Game...")
        accounts_file = setup_accounts_file()
        accounts = load_accounts(accounts_file)
        
        # Step 2: Display welcome and setup guest account
        display_welcome()
        guest_name = get_user_name()
        current_user = create_guest_account(guest_name)
        
        # Step 3: Main program loop - continues until user exits
        while True:
            display_main_menu(current_user)
            choice = get_menu_choice()
            
            # Step 4: Handle menu choices based on current user status
            if current_user["username"] == "guest":
                # Guest user menu options
                if choice == "1":  # Quick Game
                    play_game(current_user)
                    
                elif choice == "2":  # Login
                    success, current_user = login_user(accounts, accounts_file, current_user)
                    
                elif choice == "3":  # Register
                    success, current_user = register_user(accounts, accounts_file, current_user)
                    
                elif choice == "4":  # Exit
                    exit_game(current_user, accounts, accounts_file)
                    break  # Exit the main loop
                    
            else:
                # Logged-in user menu options
                if choice == "1":  # Play Game
                    play_game(current_user)
                    
                elif choice == "2":  # Logout
                    current_user = logout_user(current_user, accounts, accounts_file)
                    
                elif choice == "3":  # Exit
                    exit_game(current_user, accounts, accounts_file)
                    break  # Exit the main loop
                    
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\nGame interrupted by user. Goodbye!")
        
    except Exception as e:
        # Handle any unexpected errors
        print(f"\nAn unexpected error occurred: {e}")
        print("Please restart the game.")
        print("If this problem persists, check that all module files are present:")
        print("- display.py")
        print("- game_logic.py") 
        print("- accounts.py")
        print("- storage.py")
        print("- retrieve_word_fn.py")


def run_game() -> None:
    """
    Alternative entry point for running the game.
    Can be used for testing or alternative startup methods.
    """
    main()


if __name__ == "__main__":
    # Program entry point - this runs when you execute: python main.py
    main()