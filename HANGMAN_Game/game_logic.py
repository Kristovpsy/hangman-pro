import random
from typing import Dict, Any
from retrieve_word_fn import retrieve_word
from display import (
    display_game_header, get_hangman_stages, display_game_state, 
    get_letter_guess, display_game_result, display_session_stats
)

def create_game_session(word: str) -> Dict[str, Any]:
    """
    Create a new game session dictionary with initial game state.
    
    Args:
        word (str): The word to guess
        
    Returns:
        Dict[str, Any]: Game session dictionary with all game state variables
    """
    return {
        "word": word.upper(),
        "guessed_letters": [],    # All letters guessed so far
        "correct_guesses": [],    # Only correct letters
        "wrong_guesses": [],      # Only wrong letters
        "lives": 6,              # Start with 6 lives (standard hangman)
        "is_complete": False,    # Game not finished yet
        "is_won": False         # Haven't won yet
    }

def make_guess(game_session: Dict[str, Any], letter: str) -> bool:
    """
    Process a letter guess and update the game state.
    
    Args:
        game_session (Dict[str, Any]): Current game session
        letter (str): The guessed letter
        
    Returns:
        bool: True if guess was correct, False if wrong or already guessed
    """
    letter = letter.upper()
    word = game_session["word"]
    
    # Check if letter already guessed
    if letter in game_session["guessed_letters"]:
        return False
    
    # Add to guessed letters list
    game_session["guessed_letters"].append(letter)
    
    if letter in word:
        # Correct guess!
        game_session["correct_guesses"].append(letter)
        
        # Check if word is complete (all letters guessed)
        if all(char in game_session["correct_guesses"] for char in word):
            game_session["is_complete"] = True
            game_session["is_won"] = True
        return True
    else:
        # Wrong guess!
        game_session["wrong_guesses"].append(letter)
        game_session["lives"] -= 1
        
        # Check if game over (no lives left)
        if game_session["lives"] <= 0:
            game_session["is_complete"] = True
            game_session["is_won"] = False
        return False

def is_letter_already_guessed(game_session: Dict[str, Any], letter: str) -> bool:
    """
    Check if a letter has already been guessed.
    
    Args:
        game_session (Dict[str, Any]): Current game session
        letter (str): Letter to check
        
    Returns:
        bool: True if letter was already guessed
    """
    return letter.upper() in game_session["guessed_letters"]

def get_random_word() -> str:
    """
    Get a random word for the game, with fallback if API fails.
    
    Returns:
        str: A random word for the hangman game
    """
    try:
        word = retrieve_word(random.randint(4, 10))
        print(f"Retrieved word from API: {len(word)} letters")
        return word
    except Exception as e:
        print(f"Error retrieving word from API: {e}")
        # Fallback words if API is unavailable
        fallback_words = [
            "PYTHON", "PROGRAMMING", "COMPUTER", "KEYBOARD", "MONITOR", 
            "SOFTWARE", "HARDWARE", "INTERNET", "WEBSITE", "DATABASE",
            "FUNCTION", "VARIABLE", "ALGORITHM", "CODING", "DEBUGGING"
        ]
        word = random.choice(fallback_words)
        print("Using fallback word.")
        return word

def play_game(current_user: Dict[str, Any]) -> None:
    """
    Play a complete game of hangman from start to finish.
    
    Args:
        current_user (Dict[str, Any]): Current user account (for statistics tracking)
    """
    display_game_header()
    
    # Step 1: Get a random word
    word = get_random_word()
    
    # Step 2: Initialize the game session
    game_session = create_game_session(word)
    hangman_stages = get_hangman_stages()
    
    print(f"Word length: {len(word)} letters")
    print("Good luck!\n")
    
    # Step 3: Main game loop - continue until game is complete
    while not game_session["is_complete"]:
        # Display current game state
        display_game_state(game_session, hangman_stages)
        
        # Get user input
        guess = get_letter_guess()
        
        # Check if already guessed
        if is_letter_already_guessed(game_session, guess):
            print("You already guessed that letter!")
            continue
        
        # Process the guess and give feedback
        if make_guess(game_session, guess):
            print(f"Good guess! '{guess}' is in the word.")
        else:
            print(f"Sorry, '{guess}' is not in the word.")
    
    # Step 4: Game completed - show final results
    display_game_result(game_session, word, hangman_stages)
    
    # Step 5: Update user statistics
    if game_session["is_won"]:
        current_user["session_wins"] += 1
    else:
        current_user["session_losses"] += 1
    
    current_user["session_plays"] += 1
    
    # Step 6: Display session statistics
    display_session_stats(current_user)

def is_game_complete(game_session: Dict[str, Any]) -> bool:
    """
    Check if the game is complete (won or lost).
    
    Args:
        game_session (Dict[str, Any]): Current game session
        
    Returns:
        bool: True if game is complete
    """
    return game_session["is_complete"]

def is_game_won(game_session: Dict[str, Any]) -> bool:
    """
    Check if the game was won.
    
    Args:
        game_session (Dict[str, Any]): Current game session
        
    Returns:
        bool: True if game was won
    """
    return game_session["is_won"]

def get_game_stats(game_session: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get statistics about the current game session.
    
    Args:
        game_session (Dict[str, Any]): Current game session
        
    Returns:
        Dict[str, Any]: Game statistics
    """
    return {
        "total_guesses": len(game_session["guessed_letters"]),
        "correct_guesses": len(game_session["correct_guesses"]),
        "wrong_guesses": len(game_session["wrong_guesses"]),
        "lives_remaining": game_session["lives"],
        "word_completion": len(game_session["correct_guesses"]) / len(set(game_session["word"])) * 100
    } 