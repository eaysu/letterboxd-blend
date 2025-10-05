import re
from typing import Dict, List


def normalize_title(title: str) -> str:
    """Normalize film titles for better matching."""
    return re.sub(r'[^a-z0-9]', '', title.lower().strip())


def create_film_key(film: Dict) -> str:
    """Create unique key for film matching."""
    title = normalize_title(film.get('name', ''))
    year = str(film.get('year', '')).strip()
    return f"{title}_{year}"


def blend_users(user1_data: Dict, user2_data: Dict) -> Dict:
    """
    Compare two users' Letterboxd data and generate blend results.
    Args:
        user1_data: dict from user1 (parsed from ratings.csv, watched.csv, watchlist.csv)
        user2_data: dict from user2
    Returns:
        Dictionary containing blend results.
    """

    # --- Load and normalize user data ---
    user1_ratings = {create_film_key(f): f for f in user1_data.get("ratings", [])}
    user2_ratings = {create_film_key(f): f for f in user2_data.get("ratings", [])}
    user1_watchlist = {create_film_key(f): f for f in user1_data.get("watchlist", [])}
    user2_watchlist = {create_film_key(f): f for f in user2_data.get("watchlist", [])}

    # --- Common watched films ---
    common_keys = set(user1_ratings.keys()) & set(user2_ratings.keys())
    common_watched = []
    for key in common_keys:
        f1 = user1_ratings[key]
        f2 = user2_ratings[key]
        avg = (float(f1.get("rating", 0)) + float(f2.get("rating", 0))) / 2
        common_watched.append({
            "name": f1.get("name"),
            "year": f1.get("year"),
            "letterboxd_uri": f1.get("letterboxd_uri"),
            "user1_rating": float(f1.get("rating", 0)),
            "user2_rating": float(f2.get("rating", 0)),
            "avg_rating": avg
        })

    # Sort by average rating (descending)
    common_watched.sort(key=lambda x: x["avg_rating"], reverse=True)
    top_common = common_watched[:15]

    # --- Common favorites (rated >=4 both sides) ---
    common_favorites = [
        f for f in common_watched if f["user1_rating"] >= 4.0 and f["user2_rating"] >= 4.0
    ]

    # --- Common watchlist ---
    common_watchlist_keys = set(user1_watchlist.keys()) & set(user2_watchlist.keys())
    common_watchlist = [user1_watchlist[k] for k in common_watchlist_keys][:5]

    # --- Personalized Recommendations ---
    # User1 → unseen high-rated films from User2
    user1_recs = [
        {
            "name": f.get("name"),
            "year": f.get("year"),
            "letterboxd_uri": f.get("letterboxd_uri"),
            "rating": float(f.get("rating", 0))
        }
        for k, f in user2_ratings.items()
        if k not in user1_ratings and float(f.get("rating", 0)) >= 4.0
    ]
    user1_recs.sort(key=lambda x: x["rating"], reverse=True)

    # User2 → unseen high-rated films from User1
    user2_recs = [
        {
            "name": f.get("name"),
            "year": f.get("year"),
            "letterboxd_uri": f.get("letterboxd_uri"),
            "rating": float(f.get("rating", 0))
        }
        for k, f in user1_ratings.items()
        if k not in user2_ratings and float(f.get("rating", 0)) >= 4.0
    ]
    user2_recs.sort(key=lambda x: x["rating"], reverse=True)

    # --- Stats ---
    stats = {
        "total_common_watched": len(common_watched),
        "total_common_favorites": len(common_favorites),
        "total_common_watchlist": len(common_watchlist),
        "user1_total_rated": len(user1_ratings),
        "user2_total_rated": len(user2_ratings)
    }

    return {
        "top_common_films": top_common,
        "common_favorites": common_favorites[:10],
        "recommendations": {
            "for_user1": user1_recs[:10],
            "for_user2": user2_recs[:10]
        },
        "common_watchlist": common_watchlist,
        "stats": stats
    }
