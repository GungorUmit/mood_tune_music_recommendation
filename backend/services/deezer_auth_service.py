"""
Deezer OAuth Service
Gestiona autenticación OAuth y creación de playlists en Deezer.

Flujo:
1. Usuario → login → redirect a Deezer OAuth
2. Deezer → callback con code → intercambiar por access_token
3. Guardar token en sesión/cookie
4. Usar token para crear playlists y añadir tracks
"""

import os
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()


class DeezerAuthService:
    """Servicio para OAuth y gestión de playlists en Deezer"""
    
    def __init__(self):
        self.app_id = os.getenv("DEEZER_APP_ID")
        self.secret_key = os.getenv("DEEZER_SECRET_KEY")
        self.redirect_uri = os.getenv("DEEZER_REDIRECT_URI", "http://localhost:8000/auth/deezer/callback")
        
        self.oauth_url = "https://connect.deezer.com/oauth"
        self.api_url = "https://api.deezer.com"
        
        if not self.app_id or not self.secret_key:
            print("⚠️ WARNING: DEEZER_APP_ID or DEEZER_SECRET_KEY not configured")
            print("   OAuth features will be disabled")
            print("   Get credentials from: https://developers.deezer.com/myapps")
    
    def is_configured(self) -> bool:
        """Verifica si el servicio OAuth está configurado"""
        return bool(self.app_id and self.secret_key)
    
    def get_auth_url(self, state: Optional[str] = None) -> str:
        """
        Genera URL de autenticación OAuth para redirigir al usuario.
        
        Args:
            state: String opcional para prevenir CSRF attacks
        
        Returns:
            URL completa de Deezer OAuth
        """
        params = {
            "app_id": self.app_id,
            "redirect_uri": self.redirect_uri,
            "perms": "manage_library,offline_access",  # Permisos: crear playlists + token persistente
        }
        
        if state:
            params["state"] = state
        
        auth_url = f"{self.oauth_url}/auth.php?{urlencode(params)}"
        print(f"🔐 OAuth URL generated: {auth_url}")
        return auth_url
    
    def exchange_code_for_token(self, code: str) -> Optional[Dict]:
        """
        Intercambia authorization code por access token.
        
        Args:
            code: Authorization code recibido en callback
        
        Returns:
            {"access_token": "...", "expires": 3600} o None si falla
        """
        try:
            params = {
                "app_id": self.app_id,
                "secret": self.secret_key,
                "code": code,
                "output": "json"
            }
            
            url = f"{self.oauth_url}/access_token.php"
            print(f"🔄 Exchanging code for token...")
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if "access_token" in data:
                print(f"✅ Access token obtained (expires in {data.get('expires', 'N/A')}s)")
                return data
            else:
                print(f"❌ No access_token in response: {data}")
                return None
                
        except Exception as e:
            print(f"❌ Error exchanging code: {e}")
            return None
    
    def get_user_info(self, access_token: str) -> Optional[Dict]:
        """
        Obtiene información del usuario autenticado.
        
        Args:
            access_token: Token de acceso
        
        Returns:
            {"id": 123, "name": "User", ...} o None si falla
        """
        try:
            url = f"{self.api_url}/user/me"
            params = {"access_token": access_token}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            user_data = response.json()
            print(f"👤 User info: {user_data.get('name', 'Unknown')} (ID: {user_data.get('id')})")
            return user_data
            
        except Exception as e:
            print(f"❌ Error getting user info: {e}")
            return None
    
    def create_playlist(
        self,
        access_token: str,
        title: str,
        description: str = "",
        public: bool = True
    ) -> Optional[Dict]:
        """
        Crea una playlist en la cuenta del usuario.
        
        Args:
            access_token: Token de acceso
            title: Nombre de la playlist
            description: Descripción opcional
            public: Si la playlist es pública (default: True)
        
        Returns:
            {"id": "12345678", ...} o None si falla
        """
        try:
            url = f"{self.api_url}/user/me/playlists"
            params = {
                "access_token": access_token,
                "title": title,
            }
            
            if description:
                params["description"] = description
                
            # Deezer API no soporta parámetro 'public' directamente,
            # todas las playlists creadas vía API son públicas por defecto
            
            print(f"📝 Creating playlist: '{title}'")
            response = requests.post(url, params=params, timeout=10)
            response.raise_for_status()
            
            # Response es simple: {"id": 12345678} o true
            data = response.json()
            
            if isinstance(data, dict) and "id" in data:
                playlist_id = data["id"]
                print(f"✅ Playlist created: ID {playlist_id}")
                return {"id": str(playlist_id)}
            elif isinstance(data, bool) and data:
                # Algunas versiones de API retornan solo true
                print(f"✅ Playlist created (no ID returned)")
                return {"id": "unknown"}
            else:
                print(f"❌ Unexpected response: {data}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating playlist: {e}")
            return None
    
    def add_tracks_to_playlist(
        self,
        access_token: str,
        playlist_id: str,
        track_ids: List[str]
    ) -> bool:
        """
        Añade tracks a una playlist existente.
        
        Args:
            access_token: Token de acceso
            playlist_id: ID de la playlist
            track_ids: Lista de IDs de tracks ["3088638", "916424", ...]
        
        Returns:
            True si éxito, False si falla
        """
        try:
            if not track_ids:
                print("⚠️ No tracks to add")
                return False
            
            url = f"{self.api_url}/playlist/{playlist_id}/tracks"
            
            # Deezer acepta IDs separados por coma
            songs_param = ",".join(track_ids)
            
            params = {
                "access_token": access_token,
                "songs": songs_param
            }
            
            print(f"📥 Adding {len(track_ids)} tracks to playlist {playlist_id}")
            response = requests.post(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Response es simple: true o false
            if data is True or data == "true":
                print(f"✅ Tracks added successfully")
                return True
            else:
                print(f"❌ Failed to add tracks: {data}")
                return False
                
        except Exception as e:
            print(f"❌ Error adding tracks: {e}")
            return False
    
    def create_mood_playlist(
        self,
        access_token: str,
        mood_name: str,
        track_ids: List[str],
        genres: List[str] = None,
        energy: str = "medium"
    ) -> Optional[Dict]:
        """
        Crea una playlist completa con mood + añade tracks.
        Wrapper conveniente que combina create_playlist + add_tracks.
        
        Args:
            access_token: Token de acceso
            mood_name: Nombre del mood (ej: "Triste y Melancólico")
            track_ids: Lista de IDs de tracks
            genres: Géneros sugeridos (opcional)
            energy: Nivel de energía (opcional)
        
        Returns:
            {
                "id": "12345678",
                "url": "https://www.deezer.com/playlist/12345678",
                "app_url": "deezer://playlist/12345678",
                "title": "...",
                "tracks_count": 10
            }
        """
        try:
            # 1. Formatear título descriptivo
            title = f"Mood: {mood_name}"
            
            # 2. Formatear descripción
            description_parts = ["Generado por Asistente Musical AI"]
            if genres:
                description_parts.append(f"Géneros: {', '.join(genres[:3])}")
            if energy:
                energy_emoji = {"low": "🌙", "medium": "☀️", "high": "⚡"}.get(energy, "")
                description_parts.append(f"Energía: {energy} {energy_emoji}")
            
            description = " | ".join(description_parts)
            
            # 3. Crear playlist
            playlist_data = self.create_playlist(
                access_token=access_token,
                title=title,
                description=description
            )
            
            if not playlist_data or "id" not in playlist_data:
                print("❌ Failed to create playlist")
                return None
            
            playlist_id = playlist_data["id"]
            
            # 4. Añadir tracks
            success = self.add_tracks_to_playlist(
                access_token=access_token,
                playlist_id=playlist_id,
                track_ids=track_ids
            )
            
            if not success:
                print("⚠️ Playlist created but failed to add tracks")
            
            # 5. Construir respuesta con URLs
            result = {
                "id": playlist_id,
                "url": f"https://www.deezer.com/playlist/{playlist_id}",
                "app_url": f"deezer://playlist/{playlist_id}",
                "title": title,
                "description": description,
                "tracks_count": len(track_ids) if success else 0
            }
            
            print(f"🎉 Mood playlist created successfully!")
            print(f"   URL: {result['url']}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error creating mood playlist: {e}")
            return None


# Singleton instance
deezer_auth_service = DeezerAuthService()
