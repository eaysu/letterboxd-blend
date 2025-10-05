import pandas as pd
from typing import Dict, List, Optional

def parse_ratings_csv(csv_path: str) -> List[Dict]:
    """Parse ratings.csv file."""
    try:
        df = pd.read_csv(csv_path)
        ratings = []
        
        for _, row in df.iterrows():
            film = {
                'name': row.get('Name', ''),
                'year': row.get('Year', ''),
                'rating': float(row.get('Rating', 0)),
                'letterboxd_uri': row.get('Letterboxd URI', '')
            }
            ratings.append(film)
        
        return ratings
    except Exception as e:
        print(f"Error parsing ratings CSV: {e}")
        return []


def parse_watched_csv(csv_path: str) -> List[Dict]:
    """Parse watched.csv file."""
    try:
        df = pd.read_csv(csv_path)
        watched = []
        
        for _, row in df.iterrows():
            film = {
                'name': row.get('Name', ''),
                'year': row.get('Year', ''),
                'letterboxd_uri': row.get('Letterboxd URI', ''),
                'date': row.get('Date', '')
            }
            watched.append(film)
        
        return watched
    except Exception as e:
        print(f"Error parsing watched CSV: {e}")
        return []


def parse_watchlist_csv(csv_path: str) -> List[Dict]:
    """Parse watchlist.csv file."""
    try:
        df = pd.read_csv(csv_path)
        watchlist = []
        
        for _, row in df.iterrows():
            film = {
                'name': row.get('Name', ''),
                'year': row.get('Year', ''),
                'letterboxd_uri': row.get('Letterboxd URI', '')
            }
            watchlist.append(film)
        
        return watchlist
    except Exception as e:
        print(f"Error parsing watchlist CSV: {e}")
        return []


def parse_letterboxd_data(csv_paths: Dict[str, Optional[str]]) -> Dict:
    """
    Parse all Letterboxd CSV files and return normalized JSON.
    
    Args:
        csv_paths: Dictionary with paths to CSV files
        
    Returns:
        Dictionary with parsed data
    """
    data = {
        'ratings': [],
        'watched': [],
        'watchlist': []
    }
    
    if csv_paths.get('ratings'):
        data['ratings'] = parse_ratings_csv(csv_paths['ratings'])
    
    if csv_paths.get('watched'):
        data['watched'] = parse_watched_csv(csv_paths['watched'])
    
    if csv_paths.get('watchlist'):
        data['watchlist'] = parse_watchlist_csv(csv_paths['watchlist'])
    
    return data