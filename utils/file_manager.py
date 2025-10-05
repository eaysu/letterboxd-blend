import json
from pathlib import Path
from typing import Dict, Optional, List

DATA_DIR = Path("data/users")

def ensure_data_dir():
    """Create data directory if it doesn't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def save_user(username: str, data: Dict) -> bool:
    """
    Save user data to JSON file.
    
    Args:
        username: User identifier
        data: User's parsed Letterboxd data
        
    Returns:
        True if successful
    """
    ensure_data_dir()
    
    try:
        filepath = DATA_DIR / f"{username}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving user data: {e}")
        return False


def get_user(username: str) -> Optional[Dict]:
    """
    Load user data from JSON file.
    
    Args:
        username: User identifier
        
    Returns:
        User data dictionary or None if not found
    """
    try:
        filepath = DATA_DIR / f"{username}.json"
        if not filepath.exists():
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading user data: {e}")
        return None


def delete_user(username: str) -> bool:
    """
    Delete user's data file.
    
    Args:
        username: User identifier
        
    Returns:
        True if successful
    """
    try:
        filepath = DATA_DIR / f"{username}.json"
        if filepath.exists():
            filepath.unlink()
            return True
        return False
    except Exception as e:
        print(f"Error deleting user data: {e}")
        return False


def list_users() -> List[str]:
    """
    Get list of all stored usernames.
    
    Returns:
        List of usernames
    """
    ensure_data_dir()
    
    try:
        return [f.stem for f in DATA_DIR.glob("*.json")]
    except Exception as e:
        print(f"Error listing users: {e}")
        return []