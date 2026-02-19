import requests
from typing import Dict, List

class DeezerService:
    def __init__(self):
        self.api_base_url = "https://api.deezer.com"
    
    def search_tracks(self, mood_tags: List[str], genres: List[str], energy: str = "medium", limit: int = 25) -> Dict:
        try:
            # Try different search strategies
            search_strategies = []
            
            # Strategy 1: Just use genres (most reliable)
            if genres:
                search_strategies.append(" ".join(genres[:2]))
            
            # Strategy 2: Single genre
            if genres and len(genres) > 0:
                search_strategies.append(genres[0])
            
            # Strategy 3: Energy-based search
            energy_genres = {
                "low": "chill ambient",
                "medium": "pop rock",
                "high": "dance electronic"
            }
            search_strategies.append(energy_genres.get(energy.lower(), "pop"))
            
            # Try each strategy until we get results
            for search_query in search_strategies:
                params = {"q": search_query, "limit": limit, "strict": "off"}
                response = requests.get(f"{self.api_base_url}/search", params=params)
                response.raise_for_status()
                data = response.json()
                
                if len(data.get("data", [])) > 0:
                    # Found results, process them
                    tracks = []
                    for track in data.get("data", []):
                        artist_name = track["artist"]["name"]
                        artist_count = sum(1 for t in tracks if artist_name in t["artists"])
                        if artist_count >= 2:
                            continue
                        
                        tracks.append({
                            "id": track["id"],
                            "name": track["title"],
                            "artists": [artist_name],
                            "album": track["album"]["title"],
                            "preview_url": track.get("preview"),
                            "external_url": track["link"],
                            "image_url": track["album"].get("cover_medium"),
                            "duration_ms": track["duration"] * 1000,
                            "rank": track.get("rank", 0)
                        })
                    
                    tracks.sort(key=lambda x: x["rank"], reverse=True)
                    return {"success": True, "tracks": tracks, "total": len(tracks), "query_used": search_query}
            
            # No results with any strategy
            return {"success": True, "tracks": [], "total": 0, "query_used": search_strategies[0] if search_strategies else "pop"}
        except Exception as e:
            return {"success": False, "error": str(e), "tracks": []}
    
    def _map_mood_to_keywords(self, mood_tags: List[str], energy: str) -> List[str]:
        keywords = []
        mood_map = {
            "happy": ["upbeat"], "sad": ["melancholic"], "energetic": ["powerful"],
            "calm": ["chill"], "romantic": ["love"], "party": ["dance"],
            "focused": ["instrumental"], "motivational": ["inspiring"]
        }
        for tag in mood_tags:
            for mood, tags in mood_map.items():
                if mood in tag.lower():
                    keywords.extend(tags[:1])
                    break
        energy_map = {"low": ["chill"], "medium": ["moderate"], "high": ["energetic"]}
        keywords.extend(energy_map.get(energy.lower(), [])[:1])
        return keywords

deezer_service = DeezerService()
