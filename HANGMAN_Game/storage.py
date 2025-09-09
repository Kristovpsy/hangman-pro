import json
import pathlib
from typing import Dict, Any

def setup_accounts_file() -> pathlib.Path:
    """
    Create accounts.json file in the main directory if it doesn't exist.
    Sets up the basic file structure for account storage.
    
    Returns:
        pathlib.Path: Path to the accounts.json file
    """
    accounts_file: pathlib.Path = pathlib.Path("accounts.json")
    
    try:
        if not accounts_file.exists():
            # Create empty JSON array file
            accounts_file.write_text("[]")
            print("Created accounts.json file in the main directory.")
    except (OSError, IOError) as e:
        print(f"Error creating accounts file: {e}")
    
    return accounts_file

def load_accounts(accounts_file: pathlib.Path) -> Dict[str, Dict[str, Any]]:
    """
    Load all user accounts from JSON file into memory.
    Converts JSON array format to dictionary for easy lookup by username.
    
    Args:
        accounts_file (pathlib.Path): Path to accounts JSON file
        
    Returns:
        Dict[str, Dict[str, Any]]: Dictionary of accounts keyed by username
    """
    accounts: Dict[str, Dict[str, Any]] = {}
    
    try:
        if accounts_file.exists():
            with open(accounts_file, 'r') as f:
                accounts_data = json.load(f)
                
                # Convert JSON array to dictionary for easy username lookup
                for account_data in accounts_data:
                    username = account_data["username"]
                    accounts[username] = account_data
                    
            print(f"Loaded {len(accounts)} accounts from {accounts_file}")
    except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
        print(f"Error loading accounts: {e}")
        print("Starting with empty accounts database.")
    
    return accounts

def save_accounts(accounts: Dict[str, Dict[str, Any]], accounts_file: pathlib.Path) -> None:
    """
    Save all user accounts to JSON file.
    Converts dictionary format back to JSON array for storage.
    
    Args:
        accounts (Dict[str, Dict[str, Any]]): Dictionary of all accounts
        accounts_file (pathlib.Path): Path to accounts JSON file
    """
    try:
        # Convert dictionary back to list format for JSON storage
        accounts_data = list(accounts.values())
        
        with open(accounts_file, 'w') as f:
            json.dump(accounts_data, f, indent=2)
            
        print(f"Accounts saved to {accounts_file}")
    except (IOError, json.JSONEncodeError) as e:
        print(f"Error saving accounts: {e}")

def backup_accounts(accounts: Dict[str, Dict[str, Any]], backup_name: str = "backup") -> bool:
    """
    Create a backup copy of the accounts file.
    
    Args:
        accounts (Dict[str, Dict[str, Any]]): Dictionary of all accounts
        backup_name (str): Name for the backup file (default: "backup")
        
    Returns:
        bool: True if backup was successful, False otherwise
    """
    try:
        backup_file = pathlib.Path(f"accounts_{backup_name}.json")
        accounts_data = list(accounts.values())
        
        with open(backup_file, 'w') as f:
            json.dump(accounts_data, f, indent=2)
            
        print(f"Backup created: {backup_file}")
        return True
    except (IOError, json.JSONEncodeError) as e:
        print(f"Error creating backup: {e}")
        return False

def file_exists(file_path: str) -> bool:
    """
    Check if a file exists.
    
    Args:
        file_path (str): Path to the file to check
        
    Returns:
        bool: True if file exists, False otherwise
    """
    return pathlib.Path(file_path).exists()

def get_file_size(file_path: str) -> int:
    """
    Get the size of a file in bytes.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        int: File size in bytes, -1 if file doesn't exist
    """
    try:
        return pathlib.Path(file_path).stat().st_size
    except (FileNotFoundError, OSError):
        return -1

def validate_json_file(file_path: pathlib.Path) -> bool:
    """
    Validate that a JSON file is properly formatted.
    
    Args:
        file_path (pathlib.Path): Path to JSON file to validate
        
    Returns:
        bool: True if JSON is valid, False otherwise
    """
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        return True
    except (json.JSONDecodeError, FileNotFoundError, IOError):
        return False

def repair_accounts_file(accounts_file: pathlib.Path) -> bool:
    """
    Attempt to repair a corrupted accounts.json file.
    Creates a new empty file if repair is not possible.
    
    Args:
        accounts_file (pathlib.Path): Path to accounts file
        
    Returns:
        bool: True if repair was successful, False if new file was created
    """
    try:
        # Try to validate current file
        if validate_json_file(accounts_file):
            return True  # File is fine
            
        print("Accounts file appears to be corrupted.")
        
        # Create backup of corrupted file
        corrupted_backup = pathlib.Path("accounts_corrupted_backup.json")
        if accounts_file.exists():
            accounts_file.rename(corrupted_backup)
            print(f"Corrupted file backed up as: {corrupted_backup}")
        
        # Create new empty accounts file
        accounts_file.write_text("[]")
        print("Created new empty accounts file.")
        return False
        
    except Exception as e:
        print(f"Error repairing accounts file: {e}")
        return False

def create_save_directory() -> pathlib.Path:
    """
    Create a save directory for storing game data (optional alternative location).
    
    Returns:
        pathlib.Path: Path to save directory
    """
    save_dir = pathlib.Path("save")
    try:
        save_dir.mkdir(exist_ok=True)
        print(f"Save directory ready: {save_dir}")
    except OSError as e:
        print(f"Error creating save directory: {e}")
    
    return save_dir

def cleanup_old_backups(max_backups: int = 5) -> None:
    """
    Remove old backup files, keeping only the most recent ones.
    
    Args:
        max_backups (int): Maximum number of backup files to keep
    """
    try:
        # Find all backup files
        backup_files = list(pathlib.Path(".").glob("accounts_*.json"))
        backup_files = [f for f in backup_files if f.name != "accounts.json"]
        
        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Remove excess backups
        for old_backup in backup_files[max_backups:]:
            old_backup.unlink()
            print(f"Removed old backup: {old_backup}")
            
    except Exception as e:
        print(f"Error cleaning up backups: {e}")

def get_accounts_file_info(accounts_file: pathlib.Path) -> Dict[str, Any]:
    """
    Get information about the accounts file.
    
    Args:
        accounts_file (pathlib.Path): Path to accounts file
        
    Returns:
        Dict[str, Any]: File information including size, account count, etc.
    """
    info = {
        "exists": accounts_file.exists(),
        "size_bytes": 0,
        "account_count": 0,
        "is_valid_json": False,
        "last_modified": None
    }
    
    try:
        if accounts_file.exists():
            stat = accounts_file.stat()
            info["size_bytes"] = stat.st_size
            info["last_modified"] = stat.st_mtime
            
            if validate_json_file(accounts_file):
                info["is_valid_json"] = True
                with open(accounts_file, 'r') as f:
                    data = json.load(f)
                    info["account_count"] = len(data)
                    
    except Exception as e:
        print(f"Error getting file info: {e}")
    
    return info 