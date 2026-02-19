from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn
import os
from services.llm_service import analyze_mood
from services.deezer_service import deezer_service
from services.deezer_auth_service import deezer_auth_service

app = FastAPI(
    title="MoodTune API",
    description="AI-powered music discovery API",
    version="1.0.0"
)

@app.get("/health", include_in_schema=False)  # Add this line if needed
@app.head("/health")  # Add this new decorator
async def health():
    return {"status": "ok"}



# CORS configuration - allow frontend to make requests
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Configure allowed origins based on environment
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
]

if ENVIRONMENT == "production":
    allowed_origins.extend([
        "https://moodtune.umitgungor.me",
        "https://api-moodtune.umitgungor.me",
        FRONTEND_URL
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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


class CreatePlaylistRequest(BaseModel):
    """Request para crear playlist en Deezer con mood tracks"""
    track_ids: List[str] = Field(..., min_items=1, max_items=50, description="Lista de IDs de tracks de Deezer")
    mood_name: str = Field(..., min_length=3, max_length=100, description="Nombre descriptivo del mood")
    genres: Optional[List[str]] = Field(default=None, description="Géneros musicales opcionales")
    energy: Optional[str] = Field(default="medium", description="Nivel de energía: low/medium/high")
    
    class Config:
        json_schema_extra = {
            "examples": [{
                "track_ids": ["3088638", "916424", "3135556"],
                "mood_name": "Triste y Melancólico",
                "genres": ["balada", "indie"],
                "energy": "low"
            }]
        }


class PlaylistResponse(BaseModel):
    """Response con información de la playlist creada"""
    success: bool
    playlist_id: str
    playlist_url: str
    playlist_app_url: str
    title: str
    tracks_count: int


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
    """Health check endpoint for monitoring and deployment verification"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": ENVIRONMENT,
        "cors_enabled": True,
        "allowed_origins": len(allowed_origins)
    }


@app.post("/api/discover", response_model=DiscoverResponse)
async def discover_music(request: DiscoverRequest):
    """
    Discover music based on mood description using AI + Deezer.
    """
    
    try:
        # Step 1: Analyze mood with AI
        mood_analysis = await analyze_mood(request.user_query, request.language)
        
        # Step 2: Search tracks on Deezer
        deezer_result = deezer_service.search_tracks(
            mood_tags=mood_analysis["mood_tags"],
            genres=mood_analysis["genres"],
            energy=mood_analysis["energy"],
            limit=10
        )
        
        if not deezer_result["success"]:
            raise HTTPException(status_code=500, detail="Error searching music")
        
        # Step 3: Format response
        tracks = []
        for track in deezer_result["tracks"][:10]:
            tracks.append({
                "id": str(track["id"]),
                "title": track["name"],
                "artist": track["artists"][0] if track["artists"] else "Unknown",
                "album": track["album"],
                "preview_url": track.get("preview_url"),
                "deezer_link": track["external_url"],
                "cover_image": track.get("image_url"),
                "duration": track["duration_ms"] // 1000
            })
        
        mood_tags_str = ", ".join(mood_analysis["mood_tags"][:3])
        
        return {
            "success": True,
            "tracks": tracks,
            "metadata": {
                "interpreted_mood": mood_tags_str,
                "energy_level": mood_analysis["energy"],
                "suggested_genres": mood_analysis["genres"][:3],
                "search_query_used": mood_analysis.get("search_query", request.user_query)
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


# ============================================
# DEEZER OAUTH ENDPOINTS
# ============================================

@app.get("/auth/deezer/status")
async def check_deezer_oauth_status():
    """
    Verifica si el servicio OAuth de Deezer está configurado.
    Frontend usa esto para mostrar/ocultar botones de autenticación.
    """
    is_configured = deezer_auth_service.is_configured()
    
    return {
        "oauth_enabled": is_configured,
        "message": "OAuth configured" if is_configured else "Deezer OAuth not configured. Set DEEZER_APP_ID and DEEZER_SECRET_KEY in .env"
    }


@app.get("/auth/deezer/login")
async def deezer_oauth_login():
    """
    Inicia el flujo OAuth de Deezer.
    Redirige al usuario a la página de autorización de Deezer.
    
    Query params opcionales:
    - state: String para prevenir CSRF (opcional)
    """
    if not deezer_auth_service.is_configured():
        raise HTTPException(
            status_code=503,
            detail="Deezer OAuth not configured. Please set DEEZER_APP_ID and DEEZER_SECRET_KEY"
        )
    
    # Generar URL de autorización
    auth_url = deezer_auth_service.get_auth_url()
    
    # Redirigir a Deezer OAuth
    return RedirectResponse(url=auth_url)


@app.get("/auth/deezer/callback")
async def deezer_oauth_callback(code: str, response: Response):
    """
    Callback de Deezer OAuth.
    Recibe authorization code y lo intercambia por access token.
    
    Query params:
    - code: Authorization code de Deezer
    - state: CSRF token (si se usó en login)
    
    Retorna: Redirige al frontend con token en cookie
    """
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")
    
    # Intercambiar code por token
    token_data = deezer_auth_service.exchange_code_for_token(code)
    
    if not token_data or "access_token" not in token_data:
        raise HTTPException(status_code=401, detail="Failed to obtain access token")
    
    access_token = token_data["access_token"]
    
    # Obtener info del usuario para confirmar
    user_info = deezer_auth_service.get_user_info(access_token)
    
    # Guardar token en cookie httpOnly (seguro contra XSS)
    # En producción, considera usar JWT y guardar en DB con user session
    response.set_cookie(
        key="deezer_token",
        value=access_token,
        httponly=True,  # No accesible desde JS (seguridad)
        secure=False,   # En producción: True (requiere HTTPS)
        samesite="lax", # CSRF protection
        max_age=3600    # 1 hora (ajustar según expires de token)
    )
    
    # Redirigir al frontend con éxito
    # En producción, usa tu dominio frontend
    frontend_url = "http://localhost:3000"
    redirect_url = f"{frontend_url}?deezer_auth=success&user={user_info.get('name', 'User') if user_info else 'Unknown'}"
    
    return RedirectResponse(url=redirect_url)


@app.get("/auth/deezer/user")
async def get_deezer_user(request: Request):
    """
    Obtiene información del usuario autenticado en Deezer.
    Requiere cookie deezer_token.
    
    Returns:
        {"authenticated": true, "user": {...}}
    """
    token = request.cookies.get("deezer_token")
    
    if not token:
        return {"authenticated": False, "user": None}
    
    user_info = deezer_auth_service.get_user_info(token)
    
    if not user_info:
        return {"authenticated": False, "user": None}
    
    return {
        "authenticated": True,
        "user": {
            "id": user_info.get("id"),
            "name": user_info.get("name"),
            "picture": user_info.get("picture_small")
        }
    }


@app.post("/auth/deezer/logout")
async def deezer_logout(response: Response):
    """Cierra sesión eliminando el token de Deezer"""
    response.delete_cookie("deezer_token")
    return {"success": True, "message": "Logged out"}


# ============================================
# PLAYLIST CREATION ENDPOINT
# ============================================

@app.post("/api/playlist/create", response_model=PlaylistResponse)
async def create_mood_playlist(request: CreatePlaylistRequest, http_request: Request):
    """
    Crea una playlist en Deezer con los tracks del mood analysis.
    Requiere autenticación OAuth (cookie deezer_token).
    
    Body:
        {
            "track_ids": ["3088638", "916424", ...],
            "mood_name": "Triste y Melancólico",
            "genres": ["balada", "indie"],
            "energy": "low"
        }
    
    Returns:
        {
            "success": true,
            "playlist_id": "12345678",
            "playlist_url": "https://www.deezer.com/playlist/12345678",
            "playlist_app_url": "deezer://playlist/12345678",
            "title": "Mood: Triste y Melancólico",
            "tracks_count": 10
        }
    """
    # 1. Verificar autenticación
    token = http_request.cookies.get("deezer_token")
    
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated. Please login with Deezer first."
        )
    
    # 2. Validar que hay tracks
    if not request.track_ids:
        raise HTTPException(
            status_code=400,
            detail="No tracks provided. track_ids cannot be empty."
        )
    
    # 3. Crear playlist con mood
    try:
        playlist_data = deezer_auth_service.create_mood_playlist(
            access_token=token,
            mood_name=request.mood_name,
            track_ids=request.track_ids,
            genres=request.genres or [],
            energy=request.energy or "medium"
        )
        
        if not playlist_data:
            raise HTTPException(
                status_code=500,
                detail="Failed to create playlist on Deezer"
            )
        
        # 4. Retornar respuesta exitosa
        return PlaylistResponse(
            success=True,
            playlist_id=playlist_data["id"],
            playlist_url=playlist_data["url"],
            playlist_app_url=playlist_data["app_url"],
            title=playlist_data["title"],
            tracks_count=playlist_data["tracks_count"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating playlist: {str(e)}"
        )


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
