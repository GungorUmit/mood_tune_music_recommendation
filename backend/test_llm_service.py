"""
Test unitario para LLM Service - Análisis de mood con detección de idioma
Verifica que el servicio responda en español o inglés según la query
"""
import asyncio
from services.llm_service import analyze_mood

async def test_mood_analysis():
    """
    Tests con queries en español e inglés para verificar:
    1. Detección automática de idioma
    2. Respuestas en el idioma correcto
    3. Inclusión de keywords de hits actuales (2026/top)
    """
    
    print("=" * 80)
    print("🧪 TEST: Análisis de Mood con Detección de Idioma")
    print("=" * 80)
    
    # Test cases: (query, esperado_idioma, descripción)
    test_cases = [
        {
            "query": "triste y melancólico después de una ruptura",
            "idioma": "español",
            "descripcion": "Query en español - mood triste"
        },
        {
            "query": "fiesta en la playa con amigos",
            "idioma": "español", 
            "descripcion": "Query en español - mood energético"
        },
        {
            "query": "studying late at night for exams",
            "idioma": "inglés",
            "descripcion": "Query en inglés - mood concentrado"
        },
        {
            "query": "working out at the gym",
            "idioma": "inglés",
            "descripcion": "Query en inglés - mood motivador"
        },
        {
            "query": "romántico y relajado para una cena",
            "idioma": "español",
            "descripcion": "Query en español - mood romántico"
        }
    ]
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'─' * 80}")
        print(f"📝 Test {i}/{len(test_cases)}: {test['descripcion']}")
        print(f"Query: \"{test['query']}\"")
        print(f"Idioma esperado: {test['idioma']}")
        
        try:
            # Analizar mood
            result = await analyze_mood(test['query'])
            
            if result:
                print(f"\n✅ Resultado:")
                print(f"   mood_tags: {result.get('mood_tags', [])}")
                print(f"   energy: {result.get('energy', 'N/A')}")
                print(f"   genres: {result.get('genres', [])}")
                print(f"   search_query: \"{result.get('search_query', '')}\"")
                
                # Verificar que search_query contiene keywords de hits actuales
                search_q = result.get('search_query', '').lower()
                has_current_keywords = any(keyword in search_q for keyword in ['2026', '2025', 'top', 'hits', 'actuales', 'nuevos'])
                
                if has_current_keywords:
                    print(f"   ✓ Contiene keywords de música actual")
                else:
                    print(f"   ⚠️ No contiene keywords de hits actuales (2026/top/hits)")
                
                # Verificar idioma (aproximado por palabras en español/inglés)
                tags_text = ' '.join(result.get('mood_tags', []))
                genres_text = ' '.join(result.get('genres', []))
                combined = f"{tags_text} {genres_text} {search_q}".lower()
                
                spanish_words = ['triste', 'feliz', 'romántico', 'energético', 'tranquilo', 'melancólico', 'música', 'actuales']
                english_words = ['sad', 'happy', 'romantic', 'energetic', 'calm', 'melancholic', 'music', 'current']
                
                has_spanish = any(word in combined for word in spanish_words)
                has_english = any(word in combined for word in english_words)
                
                detected_lang = "español" if has_spanish else "inglés" if has_english else "indeterminado"
                lang_match = detected_lang == test['idioma']
                
                print(f"   Idioma detectado: {detected_lang} {'✓' if lang_match else '⚠️ (esperado: ' + test['idioma'] + ')'}")
                
                results.append({
                    "test": test['descripcion'],
                    "success": True,
                    "has_current_keywords": has_current_keywords,
                    "language_match": lang_match
                })
            else:
                print(f"\n❌ Error: No se pudo analizar el mood")
                results.append({
                    "test": test['descripcion'],
                    "success": False
                })
                
        except Exception as e:
            print(f"\n❌ Error en test: {e}")
            results.append({
                "test": test['descripcion'],
                "success": False,
                "error": str(e)
            })
    
    # Resumen final
    print(f"\n{'=' * 80}")
    print("📊 RESUMEN DE TESTS")
    print(f"{'=' * 80}")
    
    total = len(results)
    successful = sum(1 for r in results if r.get('success', False))
    with_keywords = sum(1 for r in results if r.get('has_current_keywords', False))
    lang_matches = sum(1 for r in results if r.get('language_match', False))
    
    print(f"Total tests: {total}")
    print(f"✅ Exitosos: {successful}/{total} ({successful/total*100:.0f}%)")
    print(f"🎵 Con keywords actuales: {with_keywords}/{successful} ({with_keywords/max(successful,1)*100:.0f}%)")
    print(f"🌍 Idioma correcto: {lang_matches}/{successful} ({lang_matches/max(successful,1)*100:.0f}%)")
    
    if successful == total and with_keywords >= successful * 0.8 and lang_matches >= successful * 0.8:
        print(f"\n🎉 ¡TESTS PASADOS! El servicio funciona correctamente")
    else:
        print(f"\n⚠️ Algunos tests fallaron o no cumplen criterios")
    
    print(f"{'=' * 80}\n")

if __name__ == "__main__":
    # Ejecutar tests
    asyncio.run(test_mood_analysis())
