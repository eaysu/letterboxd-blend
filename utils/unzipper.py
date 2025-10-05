import zipfile
import os
from pathlib import Path
from typing import Dict, Optional

def extract_letterboxd_zip(username: str, zip_path: str) -> Dict[str, Optional[str]]:
    """
    Extract Letterboxd export ZIP file and return paths to CSV files.
    
    Args:
        username: User identifier
        zip_path: Path to uploaded ZIP file
        
    Returns:
        Dictionary with paths to ratings, watched, and watchlist CSV files
    """
    temp_dir = Path(f"temp/{username}")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    result = {
        'ratings': None,
        'watched': None,
        'watchlist': None
    }
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Look for CSV files
        for file in temp_dir.glob('*.csv'):
            filename = file.name.lower()
            if 'rating' in filename:
                result['ratings'] = str(file)
            elif 'watched' in filename:
                result['watched'] = str(file)
            elif 'watchlist' in filename:
                result['watchlist'] = str(file)
        
        return result
        
    except zipfile.BadZipFile:
        raise ValueError("Invalid ZIP file")
    except Exception as e:
        raise Exception(f"Error extracting ZIP: {str(e)}")


def cleanup_temp(username: str):
    """Remove temporary extraction directory for a user."""
    import shutil
    temp_dir = Path(f"temp/{username}")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)