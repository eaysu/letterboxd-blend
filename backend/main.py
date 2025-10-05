from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import shutil
from pathlib import Path
import os

from utils.unzipper import extract_letterboxd_zip, cleanup_temp
from utils.csv_parser import parse_letterboxd_data
from utils.file_manager import save_user, get_user, delete_user, list_users
from utils.blender import blend_users

app = FastAPI(title="Letterboxd Blend API")

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")

@app.get("/ping")
def ping():
    return {"status": "ok"}

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure required directories exist
Path("temp").mkdir(exist_ok=True)
Path("uploads").mkdir(exist_ok=True)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Letterboxd Blend API",
        "version": "1.0",
        "endpoints": ["/upload", "/blend", "/users", "/delete"]
    }


@app.post("/upload")
async def upload_letterboxd_data(
    username: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Upload and process Letterboxd export ZIP file.
    
    Args:
        username: User identifier
        file: ZIP file containing Letterboxd export
        
    Returns:
        Success message with user data summary
    """
    if not username:
        raise HTTPException(status_code=400, detail="Username is required")
    
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="File must be a ZIP archive")
    
    try:
        # Save uploaded file
        upload_path = Path(f"uploads/{username}.zip")
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract ZIP
        csv_paths = extract_letterboxd_zip(username, str(upload_path))
        
        # Parse CSV files
        user_data = parse_letterboxd_data(csv_paths)
        
        # Save to JSON
        save_user(username, user_data)
        
        # Cleanup
        cleanup_temp(username)
        upload_path.unlink()
        
        return {
            "success": True,
            "message": f"Data uploaded successfully for user: {username}",
            "summary": {
                "ratings_count": len(user_data.get('ratings', [])),
                "watched_count": len(user_data.get('watched', [])),
                "watchlist_count": len(user_data.get('watchlist', []))
            }
        }
        
    except Exception as e:
        # Cleanup on error
        cleanup_temp(username)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/blend")
async def blend(user1: str, user2: str):
    """
    Generate blend results for two users.
    
    Args:
        user1: First username
        user2: Second username
        
    Returns:
        Blend results with common films and recommendations
    """
    if not user1 or not user2:
        raise HTTPException(status_code=400, detail="Both usernames are required")
    
    # Get user data
    user1_data = get_user(user1)
    user2_data = get_user(user2)
    
    if not user1_data:
        raise HTTPException(status_code=404, detail=f"User not found: {user1}")
    
    if not user2_data:
        raise HTTPException(status_code=404, detail=f"User not found: {user2}")
    
    # Generate blend
    try:
        blend_result = blend_users(user1_data, user2_data)
        return {
            "success": True,
            "user1": user1,
            "user2": user2,
            "blend": blend_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating blend: {str(e)}")


@app.get("/users")
async def get_users():
    """Get list of all uploaded users."""
    try:
        users = list_users()
        return {
            "success": True,
            "users": users,
            "count": len(users)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/delete")
async def delete_user_data(username: str):
    """
    Delete a user's data.
    
    Args:
        username: Username to delete
        
    Returns:
        Success message
    """
    if not username:
        raise HTTPException(status_code=400, detail="Username is required")
    
    success = delete_user(username)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"User not found: {username}")
    
    return {
        "success": True,
        "message": f"User deleted: {username}"
    }


@app.get("/user/{username}")
async def get_user_info(username: str):
    """Get detailed information about a user."""
    user_data = get_user(username)
    
    if not user_data:
        raise HTTPException(status_code=404, detail=f"User not found: {username}")
    
    return {
        "success": True,
        "username": username,
        "data": user_data
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)