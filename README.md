# 🎬 Letterboxd Blend

A web application that allows two users to upload their Letterboxd export data and discover shared movie tastes, common favorites, and personalized recommendations.

## ✨ Features

- **Upload Letterboxd Data**: Import your Letterboxd export ZIP files
- **Blend Analysis**: Compare movie tastes between two users
- **Common Favorites**: Discover films you both loved (rated 4.0+)
- **Shared Watched Films**: See all movies you've both seen with ratings comparison
- **Personalized Recommendations**: Get movie suggestions based on what the other person loved
- **Watchlist Overlap**: Find films you both want to watch

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js (optional, for development)

### Installation

1. **Clone or create the project structure:**

```bash
mkdir letterboxd-blend
cd letterboxd-blend
```

2. **Create the following directory structure:**

```
letterboxd-blend/
├── backend/
│   ├── main.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── unzipper.py
│   │   ├── csv_parser.py
│   │   ├── blender.py
│   │   └── file_manager.py
│   └── data/users/
├── frontend/
│   └── index.html
├── requirements.txt
└── README.md
```

3. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

4. **Create empty `__init__.py` in utils folder:**

```bash
touch backend/utils/__init__.py
```

### Running the Application

1. **Start the backend server:**

```bash
cd backend
python main.py
```

The API will run on `http://localhost:8000`

2. **Open the frontend:**

Simply open `frontend/index.html` in your web browser, or serve it using:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 3000
```

Then navigate to `http://localhost:3000`

## 📖 How to Use

### Step 1: Export Your Letterboxd Data

1. Go to [Letterboxd.com](https://letterboxd.com)
2. Navigate to Settings → Import & Export
3. Click "Export your data"
4. Download the ZIP file

### Step 2: Upload Your Data

1. Open the Letterboxd Blend app
2. Enter your username (can be any identifier)
3. Select your Letterboxd export ZIP file
4. Click "Upload Data"

### Step 3: Create a Blend

1. Enter two usernames that have uploaded data
2. Click "Generate Blend"
3. Explore your shared movie taste!

## 🎯 API Endpoints

### POST `/upload`
Upload and process Letterboxd export ZIP

**Parameters:**
- `username` (form): User identifier
- `file` (form): ZIP file

**Response:**
```json
{
  "success": true,
  "message": "Data uploaded successfully",
  "summary": {
    "ratings_count": 245,
    "watched_count": 189,
    "watchlist_count": 42
  }
}
```

### GET `/blend?user1={username1}&user2={username2}`
Generate blend between two users

**Response:**
```json
{
  "success": true,
  "user1": "alice",
  "user2": "bob",
  "blend": {
    "common_watched": [...],
    "common_favorites": [...],
    "recommendations": {
      "for_user1": [...],
      "for_user2": [...]
    },
    "common_watchlist": [...],
    "stats": {...}
  }
}
```

### GET `/users`
Get list of all uploaded users

### DELETE `/delete?user={username}`
Delete a user's data

### GET `/user/{username}`
Get detailed information about a specific user

## 🛠️ Technical Details

### Backend Stack
- **FastAPI**: Modern Python web framework
- **Pandas**: CSV parsing and data manipulation
- **Python Standard Library**: ZIP extraction and file management

### Frontend Stack
- **Vanilla JavaScript**: No frameworks needed
- **Modern CSS**: Responsive design with gradients and animations
- **HTML5**: Semantic markup

### Data Storage
- User data stored as JSON files in `backend/data/users/`
- Temporary files stored in `backend/temp/` during processing
- Uploaded ZIPs stored briefly in `backend/uploads/`

## 🔒 Privacy & Data

- All data is processed and stored locally on your server
- No data is sent to third parties
- Users can delete their data at any time using the DELETE endpoint
- Temporary files are cleaned up after processing

## 🚢 Deployment

### Render

1. Create a new Web Service
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

### Railway

1. Create new project
2. Add GitHub repo
3. Railway will auto-detect Python and install dependencies
4. Set start command: `cd backend && python main.py`

### Environment Variables

For production, update the `API_URL` in `index.html`:

```javascript
const API_URL = 'https://your-api-domain.com';
```

## 🎨 Customization

### Add TMDb Posters (Optional Enhancement)

1. Get API key from [The Movie Database](https://www.themoviedb.org/settings/api)
2. Add to `blender.py`:

```python
import requests

TMDB_API_KEY = 'your_api_key'

def get_poster(film_name, year):
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': film_name,
        'year': year
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['results']:
        return f"https://image.tmdb.org/t/p/w500{data['results'][0]['poster_path']}"
    return None
```

### Add Similarity Score

Create `similarity_score.py` in utils/:

```python
import numpy as np
from scipy.stats import pearsonr

def calculate_similarity(user1_ratings, user2_ratings):
    common_films = set(user1_ratings.keys()) & set(user2_ratings.keys())
    
    if len(common_films) < 2:
        return 0
    
    ratings1 = [user1_ratings[film] for film in common_films]
    ratings2 = [user2_ratings[film] for film in common_films]
    
    correlation, _ = pearsonr(ratings1, ratings2)
    similarity = ((correlation + 1) / 2) * 100
    
    return round(similarity, 2)
```

## 🐛 Troubleshooting

**Issue: CORS errors**
- Make sure the API is running on the correct port
- Check that `API_URL` in frontend matches backend URL

**Issue: ZIP upload fails**
- Ensure the ZIP is a valid Letterboxd export
- Check file size limits (default FastAPI limit is 16MB)

**Issue: No common films found**
- Both users need to have uploaded their data
- Ensure usernames are spelled correctly
- Users need to have watched some of the same films

## 📝 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Contributions welcome! Feel free to:
- Add new features
- Improve the UI/UX
- Fix bugs
- Add documentation

## 🎬 Credits

Built for movie lovers who use [Letterboxd](https://letterboxd.com)

Inspired by music blend features in streaming platforms, adapted for cinema enthusiasts!