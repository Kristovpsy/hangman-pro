from typing import Dict, Any, List

def display_welcome() -> None:
    """Display welcome message when game starts."""
    print("=" * 50)
    print("     WELCOME TO HANGMAN GAME!")
    print("     Guess the word letter by letter")
    print("     You have 6 wrong guesses before you lose")
    print("=" * 50)

def get_user_name() -> str:
    """
    Get user name for guest account with input validation.
    
    Returns:
        str: User's name
    """
    while True:
        name = input("Please enter your name: ").strip()
        if name:
            return name
        print("Name cannot be empty. Please try again.")

def display_main_menu(current_user: Dict[str, Any]) -> None:
    """
    Display the appropriate main menu based on login status.
    
    Args:
        current_user (Dict[str, Any]): Current user account
    """
    print("\n" + "=" * 30)
    print("MAIN MENU")
    print("=" * 30)
    
    if current_user["username"] != "guest":
        print(f"Welcome back, {current_user['name']}!")
        print("1. Play Game")
        print("2. Logout")
        print("3. Exit")
    else:
        print(f"Playing as: {current_user['name']}")
        print("1. Quick Game")
        print("2. Login")
        print("3. Register")
        print("4. Exit")

def get_menu_choice() -> str:
    """
    Get user's menu choice with input validation.
    
    Returns:
        str: Valid menu choice (1-4)
    """
    while True:
        choice = input("\nEnter your choice: ").strip()
        if choice in ["1", "2", "3", "4"]:
            return choice
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

def get_hangman_stages() -> List[str]:
    """
    Get ASCII art for hangman stages - visual representation of game progress.
    
    Returns:
        List[str]: List of hangman ASCII art stages (0=empty gallows, 6=complete hangman)
    """
    return [
        # Stage 0: Empty gallows
        """
   +---+
   |   |
       |
       |
       |
       |
=========
""",
        # Stage 1: Head appears
        """
   +---+
   |   |
   O   |
       |
       |
       |
=========
""",
        # Stage 2: Body appears  
        """
   +---+
   |   |
   O   |
   |   |
       |
       |
=========
""",
        # Stage 3: Left arm appears
        """
   +---+
   |   |
   O   |
  /|   |
       |
       |
=========
""",
        # Stage 4: Right arm appears
        """
   +---+
   |   |
   O   |
  /|\\  |
       |
       |
=========
""",
        # Stage 5: Left leg appears
        """
   +---+
   |   |
   O   |
  /|\\  |
  /    |
       |
=========
""",
        # Stage 6: Right leg appears - GAME OVER!
        """
   +---+
   |   |
   O   |
  /|\\  |
  / \\  |
       |
=========
"""
    ]

def display_game_state(game_session: Dict[str, Any], hangman_stages: List[str]) -> None:
    """
    Display the current state of the hangman game.
    
    Args:
        game_session (Dict[str, Any]): Current game session data
        hangman_stages (List[str]): ASCII art stages for hangman
    """
    print(hangman_stages[6 - game_session["lives"]])
    print(f"Word: {get_display_word(game_session)}")
    print(f"Lives remaining: {game_session['lives']}")
    
    if game_session["guessed_letters"]:
        print(f"Guessed letters: {', '.join(sorted(game_session['guessed_letters']))}")

def get_display_word(game_session: Dict[str, Any]) -> str:
    """
    Get the word with unguessed letters as underscores.
    
    Args:
        game_session (Dict[str, Any]): Current game session
        
    Returns:
        str: Display word with underscores for unguessed letters (e.g., "P Y _ H O _")
    """
    word = game_session["word"]
    correct_guesses = game_session["correct_guesses"]
    return " ".join([letter if letter in correct_guesses else "_" for letter in word])

def get_letter_guess() -> str:
    """
    Get a valid letter guess from the user.
    
    Returns:
        str: Single uppercase letter
    """
    while True:
        guess = input("\nEnter a letter: ").strip().upper()
        if len(guess) == 1 and guess.isalpha():
            return guess
        print("Please enter a single letter.")

def display_game_result(game_session: Dict[str, Any], word: str, hangman_stages: List[str]) -> None:
    """
    Display the final game result (win or loss).
    
    Args:
        game_session (Dict[str, Any]): Completed game session
        word (str): The word that was being guessed
        hangman_stages (List[str]): ASCII art stages for hangman
    """
    # Show final hangman state
    print(hangman_stages[6 - game_session["lives"]])
    print(f"The word was: {word}")
    
    if game_session["is_won"]:
        print("🎉 Congratulations! You won! 🎉")
    else:
        print("💀 Game over! Better luck next time! 💀")

def display_session_stats(current_user: Dict[str, Any]) -> None:
    """
    Display current session statistics for the user.
    
    Args:
        current_user (Dict[str, Any]): Current user account
    """
    print(f"\nSession Statistics for {current_user['name']}:")
    print(f"Games played this session: {current_user['session_plays']}")
    print(f"Wins this session: {current_user['session_wins']}")
    print(f"Losses this session: {current_user['session_losses']}")

def display_login_header() -> None:
    """Display login section header."""
    print("\n" + "=" * 30)
    print("LOGIN")
    print("=" * 30)

def display_register_header() -> None:
    """Display registration section header."""
    print("\n" + "=" * 30)
    print("REGISTER")
    print("=" * 30)

def display_game_header() -> None:
    """Display game start header."""
    print("\n" + "=" * 40)
    print("HANGMAN GAME STARTED")
    print("=" * 40)

def display_password_requirements() -> None:
    """Display password requirements for manual password entry."""
    print("\nPassword requirements:")
    print("- At least one lowercase letter")
    print("- At least one uppercase letter")
    print("- At least one digit")
    print("- At least one symbol (!@#$%^&*)")
    print("- Maximum length of 16 characters")