import asyncio
import time
from services.llm_service import analyze_mood
from services.mood_cache_service import mood_cache

async def test_cache_performance():
    """
    Test que demuestra la mejora de velocidad con caché
    """
    print("=" * 70)
    print("🧪 TESTING MOOD CACHE PERFORMANCE")
    print("=" * 70)
    
    test_queries = [
        "estudiando para examen final a las 3am",
        "studying for final exam at 3am",
        "triste después de ruptura",
        "working out at the gym intensely",
        "relajándome en casa después del trabajo"
    ]
    
    # Test 1: Primera ejecución
    print("\n📊 TEST 1: Primera ejecución (puede usar caché si existe)")
    print("-" * 70)
    
    for query in test_queries:
        start = time.time()
        result = await analyze_mood(query, "es")
        elapsed = time.time() - start
        
        print(f"\n Query: '{query}'")
        print(f" ⏱️  Time: {elapsed:.3f}s")
        print(f" 🎵 Mood: {', '.join(result.get('mood_tags', []))}")
        print(f" ⚡ Energy: {result.get('energy', 'N/A')}")
        print(f" 🎸 Genres: {', '.join(result.get('genres', []))}")
    
    # Test 2: Segunda ejecución (debe usar caché)
    print("\n" + "=" * 70)
    print("📊 TEST 2: Segunda ejecución (DEBE usar caché - instantáneo)")
    print("-" * 70)
    
    for query in test_queries:
        start = time.time()
        result = await analyze_mood(query, "es")
        elapsed = time.time() - start
        
        print(f"\n Query: '{query}'")
        print(f" ⏱️  Time: {elapsed:.3f}s {'✅ INSTANT!' if elapsed < 0.01 else '⚠️ Slow'}")
        print(f" 🎵 Mood: {', '.join(result.get('mood_tags', []))}")
    
    # Test 3: Queries similares
    print("\n" + "=" * 70)
    print("📊 TEST 3: Queries similares (fuzzy matching)")
    print("-" * 70)
    
    similar_queries = [
        ("estudiando examen final 3am", "estudiando para examen final a las 3am"),
        ("study exam 3am", "studying for final exam at 3am"),
        ("sad breakup", "triste después de ruptura")
    ]
    
    for new_query, similar_to in similar_queries:
        start = time.time()
        result = await analyze_mood(new_query, "es")
        elapsed = time.time() - start
        
        print(f"\n New: '{new_query}'")
        print(f" Similar to: '{similar_to}'")
        print(f" ⏱️  Time: {elapsed:.3f}s {'✅ CACHED!' if elapsed < 0.01 else '🤖 API call'}")
    
    # Estadísticas finales
    print("\n" + "=" * 70)
    stats = mood_cache.get_stats()
    print("📈 CACHE STATISTICS")
    print("-" * 70)
    print(f" Total entries: {stats['total_entries']}")
    print(f" Cache file: {stats['cache_file']}")
    print(f" File exists: {stats['file_exists']}")
    print("=" * 70)
    print("✅ TESTS COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_cache_performance())
