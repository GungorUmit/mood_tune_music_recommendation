from services.huggingface_service import analyze_with_huggingface
from services.mood_cache_service import mood_cache

async def analyze_mood(query: str, language: str = "en") -> dict:
    """
    Analiza el mood del usuario usando:
    1. Caché inteligente (instantáneo si hay match)
    2. Hugging Face API (si no hay caché)
    
    Auto-guarda resultados nuevos en caché para futuras búsquedas.
    """
    print(f"🔄 Analyzing mood for: '{query[:50]}...'")
    
    # PASO 1: Intentar caché primero (mucho más rápido)
    cached_result = mood_cache.get_similar(query, threshold=0.75)
    if cached_result:
        print(f"⚡ Using cached result (instant response!)")
        return cached_result
    
    # PASO 2: Si no hay caché, usar Hugging Face
    print(f"🤖 No cache found, calling Hugging Face API...")
    result = await analyze_with_huggingface(query, language)
    
    if result:
        print(f"✅ Hugging Face analysis successful")
        
        # PASO 3: Guardar en caché para futuras búsquedas similares
        mood_cache.add(query, result)
        
        return result
    else:
        print(f"❌ Hugging Face analysis failed, using defaults")
        
        # Resultado por defecto
        default_result = {
            "mood_tags": ["neutral"], 
            "energy": "medium", 
            "genres": ["pop"], 
            "search_query": f"{query} 2026 top"
        }
        
        # Guardar el default también (evita llamadas innecesarias)
        mood_cache.add(query, default_result)
        
        return default_result
