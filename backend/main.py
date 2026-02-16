from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

app = FastAPI(
    title="MoodTune API",
    description="AI-powered music discovery API",
    version="1.0.0"
)

# CORS configuration - allow frontend to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Frontend dev servers
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ============================================
# REQUEST/RESPONSE MODELS
# ============================================

class DiscoverRequest(BaseModel):
    user_query: str = Field(..., min_length=10, max_length=500, description="User's mood/activity description")
    language: str = Field(..., pattern="^(en|es)$", description="Language: 'en' or 'es'")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "user_query": "studying late night with rain, need focus",
                    "language": "en"
                }
            ]
        }


class Track(BaseModel):
    id: str
    title: str
    artist: str
    album: str
    preview_url: Optional[str]
    deezer_link: str
    cover_image: str
    duration: int


class Metadata(BaseModel):
    interpreted_mood: str
    energy_level: str
    suggested_genres: List[str]
    search_query_used: str


class DiscoverResponse(BaseModel):
    success: bool
    tracks: List[Track]
    metadata: Metadata


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    error_code: str


# ============================================
# MOCK DATA
# ============================================

MOCK_TRACKS = [
    {
        "id": "3135556",
        "title": "Weightless",
        "artist": "Marconi Union",
        "album": "Ambient Transmissions Vol. 1",
        "preview_url": "https://cdns-preview-e.dzcdn.net/stream/example",
        "deezer_link": "https://www.deezer.com/track/3135556",
        "cover_image": "https://e-cdns-images.dzcdn.net/images/cover/2e018122f7e4c6e423e22e987294a79a/250x250-000000-80-0-0.jpg",
        "duration": 385
    },
    {
        "id": "916424",
        "title": "Intro",
        "artist": "The xx",
        "album": "xx",
        "preview_url": "https://cdns-preview-e.dzcdn.net/stream/example2",
        "deezer_link": "https://www.deezer.com/track/916424",
        "cover_image": "https://e-cdns-images.dzcdn.net/images/cover/d41d8cd98f00b204e9800998ecf8427e/250x250-000000-80-0-0.jpg",
        "duration": 130
    },
    {
        "id": "123456",
        "title": "Lofi Study",
        "artist": "Chillhop Music",
        "album": "Lo-fi Beats",
        "preview_url": None,
        "deezer_link": "https://www.deezer.com/track/123456",
        "cover_image": "https://via.placeholder.com/250x250/6366F1/ffffff?text=Lo-fi",
        "duration": 180
    },
    {
        "id": "789012",
        "title": "Calm Piano",
        "artist": "Peaceful Piano",
        "album": "Piano Reflections",
        "preview_url": "https://cdns-preview-e.dzcdn.net/stream/example3",
        "deezer_link": "https://www.deezer.com/track/789012",
        "cover_image": "https://via.placeholder.com/250x250/8B5CF6/ffffff?text=Piano",
        "duration": 240
    },
    {
        "id": "345678",
        "title": "Focus Flow",
        "artist": "Study Music Project",
        "album": "Deep Focus",
        "preview_url": "https://cdns-preview-e.dzcdn.net/stream/example4",
        "deezer_link": "https://www.deezer.com/track/345678",
        "cover_image": "https://via.placeholder.com/250x250/10B981/ffffff?text=Focus",
        "duration": 195
    },
]


# ============================================
# ENDPOINTS
# ============================================

@app.get("/")
async def root():
    """Root endpoint - API info"""
    return {
        "name": "MoodTune API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "version": "1.0.0"
    }


@app.post("/api/discover", response_model=DiscoverResponse)
async def discover_music(request: DiscoverRequest):
    """
    Discover music based on mood description.
    
    Currently returns mock data for testing.
    Will be integrated with LLM + Deezer API in Phase 3 & 4.
    """
    
    # Mock response based on language
    mood_text = "calm, focused, productive" if request.language == "en" else "tranquilo, enfocado, productivo"
    
    return {
        "success": True,
        "tracks": MOCK_TRACKS,
        "metadata": {
            "interpreted_mood": mood_text,
            "energy_level": "low",
            "suggested_genres": ["lo-fi", "ambient", "instrumental"],
            "search_query_used": request.user_query
        }
    }


# ============================================
# RUN SERVER
# ============================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
