import json
import os
from typing import Optional
from difflib import SequenceMatcher

class MoodCacheService:
    def __init__(self, cache_file: str = "datasets/mood_cache.json"):
        self.cache_file = cache_file
        self.cache = self._load_cache()
    
    def _load_cache(self) -> dict:
        """Carga el caché desde el archivo JSON"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error loading cache: {e}")
                return {}
        return {}
    
    def _save_cache(self):
        """Guarda el caché en el archivo JSON"""
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving cache: {e}")
    
    def get_similar(self, query: str, threshold: float = 0.75) -> Optional[dict]:
        """
        Busca queries similares en el caché usando similitud de strings
        
        Args:
            query: Query del usuario
            threshold: Umbral de similitud (0-1). 0.75 = 75% similar
        
        Returns:
            Resultado cacheado si encuentra match, None si no
        """
        query_lower = query.lower().strip()
        
        # Búsqueda exacta primero (más rápida)
        if query_lower in self.cache:
            print(f"✅ Exact cache hit!")
            return self.cache[query_lower]
        
        # Búsqueda por similitud
        best_match = None
        best_similarity = 0.0
        
        for cached_query, result in self.cache.items():
            similarity = SequenceMatcher(None, query_lower, cached_query.lower()).ratio()
            
            if similarity > best_similarity and similarity >= threshold:
                best_similarity = similarity
                best_match = result
        
        if best_match:
            print(f"✅ Similar cache hit! Similarity: {best_similarity:.2%}")
            return best_match
        
        print(f"❌ No cache hit (best similarity: {best_similarity:.2%})")
        return None
    
    def add(self, query: str, result: dict):
        """
        Añade un resultado al caché
        
        Args:
            query: Query original del usuario
            result: Resultado del análisis de mood
        """
        query_lower = query.lower().strip()
        self.cache[query_lower] = result
        self._save_cache()
        print(f"💾 Added to cache: '{query_lower}'")
    
    def get_stats(self) -> dict:
        """Retorna estadísticas del caché"""
        return {
            "total_entries": len(self.cache),
            "cache_file": self.cache_file,
            "file_exists": os.path.exists(self.cache_file)
        }

# Singleton instance
mood_cache = MoodCacheService()
