import asyncio
from services.deezer_service import deezer_service
from services.llm_service import analyze_mood

async def test_complete_flow():
    """
    Test complete flow: AI mood analysis + Deezer recommendations
    """
    print("=" * 70)
    print("🎵 TESTING COMPLETE MUSIC RECOMMENDATION SYSTEM")
    print("=" * 70)
    
    test_cases = [
        {
            "query": "estudiando para examen final a las 3am, café al lado, súper concentrado",
            "lang": "es",
            "description": "📚 Study Session - Late Night"
        },
        {
            "query": "fiesta en la playa con amigos, verano, bailando toda la noche",
            "lang": "es",
            "description": "🏖️ Beach Party - High Energy"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"TEST #{i}: {test['description']}")
        print(f"Query: '{test['query']}'")
        print("-" * 70)
        
        # Step 1: Analyze mood
        mood = await analyze_mood(test['query'], test['lang'])
        print(f"\n🧠 AI Mood Analysis:")
        print(f"   • Mood Tags: {', '.join(mood.get('mood_tags', []))}")
        print(f"   • Energy Level: {mood.get('energy', 'N/A').upper()}")
        print(f"   • Genres: {', '.join(mood.get('genres', []))}")
        
        # Step 2: Get Deezer recommendations
        results = deezer_service.search_tracks(
            mood_tags=mood.get("mood_tags", []),
            genres=mood.get("genres", []),
            energy=mood.get("energy", "medium"),
            limit=10
        )
        
        if results["success"]:
            tracks = results["tracks"]
            print(f"\n🎵 Deezer Recommendations ({len(tracks)} tracks):")
            print(f"   Search Query: '{results.get('query_used', 'N/A')}'")
            print()
            
            for idx, track in enumerate(tracks[:5], 1):
                artists = ", ".join(track["artists"])
                duration = track["duration_ms"] // 1000
                minutes = duration // 60
                seconds = duration % 60
                
                print(f"   {idx}. 🎵 {track['name']}")
                print(f"      👤 {artists}")
                print(f"      💿 {track['album']}")
                print(f"      ⏱️  {minutes}:{seconds:02d}")
                print(f"      🔗 {track['external_url']}")
                if track.get('preview_url'):
                    print(f"      🎧 Preview: {track['preview_url']}")
                print()
        else:
            print(f"\n❌ Error: {results.get('error')}")
    
    print("=" * 70)
    print("✅ ALL TESTS COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_complete_flow())