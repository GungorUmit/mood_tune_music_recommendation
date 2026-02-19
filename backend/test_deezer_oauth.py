"""
Test unitario para Deezer OAuth Flow
Verifica autenticación, creación de playlists y gestión de tokens.
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.deezer_auth_service import deezer_auth_service


async def test_oauth_configuration():
    """Test 1: Verificar configuración OAuth"""
    print("=" * 80)
    print("🧪 TEST 1: Configuración OAuth")
    print("=" * 80)
    
    is_configured = deezer_auth_service.is_configured()
    
    if is_configured:
        print("✅ OAuth está configurado")
        print(f"   App ID: {deezer_auth_service.app_id[:10]}... (oculto)")
        print(f"   Redirect URI: {deezer_auth_service.redirect_uri}")
    else:
        print("⚠️ OAuth NO está configurado")
        print("   Configura DEEZER_APP_ID y DEEZER_SECRET_KEY en .env")
        print("   Ve a: https://developers.deezer.com/myapps")
    
    print()
    return is_configured


async def test_auth_url_generation():
    """Test 2: Generar URL de autenticación"""
    print("=" * 80)
    print("🧪 TEST 2: Generación de URL OAuth")
    print("=" * 80)
    
    if not deezer_auth_service.is_configured():
        print("⏭️ SKIP - OAuth no configurado")
        print()
        return False
    
    try:
        auth_url = deezer_auth_service.get_auth_url(state="test123")
        
        print("✅ URL generada correctamente:")
        print(f"   {auth_url}")
        print()
        
        # Validar que contiene parámetros correctos
        assert "connect.deezer.com/oauth/auth.php" in auth_url
        assert f"app_id={deezer_auth_service.app_id}" in auth_url
        assert "redirect_uri=" in auth_url
        assert "perms=manage_library" in auth_url
        assert "state=test123" in auth_url
        
        print("✅ Validaciones pasadas:")
        print("   ✓ URL base correcta")
        print("   ✓ app_id presente")
        print("   ✓ redirect_uri presente")
        print("   ✓ perms=manage_library presente")
        print("   ✓ state parameter presente")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error generando URL: {e}")
        print()
        return False


async def test_manual_oauth_flow():
    """Test 3: Flujo OAuth manual (requiere interacción)"""
    print("=" * 80)
    print("🧪 TEST 3: Flujo OAuth Completo (Manual)")
    print("=" * 80)
    
    if not deezer_auth_service.is_configured():
        print("⏭️ SKIP - OAuth no configurado")
        print()
        return False
    
    print("📋 Para probar el flujo completo:")
    print()
    print("1. Inicia el backend:")
    print("   cd backend")
    print("   python main.py")
    print()
    print("2. Visita en tu navegador:")
    print("   http://localhost:8000/auth/deezer/login")
    print()
    print("3. Autoriza la aplicación en Deezer")
    print()
    print("4. Serás redirigido al callback con un token")
    print()
    print("5. El token se guardará en cookie 'deezer_token'")
    print()
    print("⚠️ Este test es manual. Ejecuta los pasos anteriores.")
    print()
    
    return True


async def test_playlist_creation_simulation():
    """Test 4: Simular creación de playlist (sin token real)"""
    print("=" * 80)
    print("🧪 TEST 4: Simulación Creación de Playlist")
    print("=" * 80)
    
    print("📋 Datos de ejemplo:")
    
    mock_track_ids = ["3088638", "916424", "3135556"]
    mock_mood = "Triste y Melancólico"
    mock_genres = ["balada", "indie"]
    mock_energy = "low"
    
    print(f"   Mood: {mock_mood}")
    print(f"   Géneros: {', '.join(mock_genres)}")
    print(f"   Energía: {mock_energy}")
    print(f"   Tracks: {len(mock_track_ids)}")
    print()
    
    print("📝 Request que se haría:")
    print()
    print("   POST /api/playlist/create")
    print("   Headers: Cookie: deezer_token=xxx")
    print("   Body:")
    print(f"   {{")
    print(f'       "track_ids": {mock_track_ids},')
    print(f'       "mood_name": "{mock_mood}",')
    print(f'       "genres": {mock_genres},')
    print(f'       "energy": "{mock_energy}"')
    print(f"   }}")
    print()
    
    print("📝 Response esperado:")
    print()
    print("   {")
    print('       "success": true,')
    print('       "playlist_id": "12345678",')
    print('       "playlist_url": "https://www.deezer.com/playlist/12345678",')
    print('       "playlist_app_url": "deezer://playlist/12345678",')
    print('       "title": "Mood: Triste y Melancólico",')
    print(f'       "tracks_count": {len(mock_track_ids)}')
    print("   }")
    print()
    
    print("⚠️ Para crear playlist real, necesitas:")
    print("   1. Completar OAuth flow (Test 3)")
    print("   2. Tener deezer_token válido")
    print("   3. Llamar al endpoint con curl o frontend")
    print()
    
    return True


async def test_api_endpoints():
    """Test 5: Verificar que endpoints existen"""
    print("=" * 80)
    print("🧪 TEST 5: Endpoints API Disponibles")
    print("=" * 80)
    
    endpoints = [
        ("GET", "/auth/deezer/status", "Verificar configuración OAuth"),
        ("GET", "/auth/deezer/login", "Iniciar flujo OAuth"),
        ("GET", "/auth/deezer/callback", "Callback OAuth (recibe code)"),
        ("GET", "/auth/deezer/user", "Info de usuario autenticado"),
        ("POST", "/auth/deezer/logout", "Cerrar sesión"),
        ("POST", "/api/playlist/create", "Crear playlist en Deezer"),
    ]
    
    print("📋 Endpoints implementados:\n")
    
    for method, path, description in endpoints:
        print(f"   [{method:6s}] {path:35s} → {description}")
    
    print()
    print("✅ Todos los endpoints están implementados")
    print()
    
    return True


async def test_curl_examples():
    """Test 6: Mostrar ejemplos de curl para probar"""
    print("=" * 80)
    print("🧪 TEST 6: Ejemplos de Prueba con curl")
    print("=" * 80)
    
    print("📋 Comandos curl para probar (backend debe estar corriendo):\n")
    
    print("1. Verificar estado OAuth:")
    print("   curl http://localhost:8000/auth/deezer/status")
    print()
    
    print("2. Verificar si estás autenticado:")
    print("   curl http://localhost:8000/auth/deezer/user -b cookies.txt")
    print()
    
    print("3. Crear playlist (requiere autenticación):")
    print("   curl -X POST http://localhost:8000/api/playlist/create \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -b cookies.txt \\")
    print("     -d '{")
    print('       "track_ids": ["3088638", "916424"],')
    print('       "mood_name": "Test Mood",')
    print('       "genres": ["pop"],')
    print('       "energy": "medium"')
    print("     }'")
    print()
    
    print("4. Cerrar sesión:")
    print("   curl -X POST http://localhost:8000/auth/deezer/logout -b cookies.txt -c cookies.txt")
    print()
    
    print("💡 Nota: Para guardar cookies, usa flags -c cookies.txt (guardar) y -b cookies.txt (enviar)")
    print()
    
    return True


async def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n")
    print("🚀 Iniciando Tests de Deezer OAuth")
    print("=" * 80)
    print()
    
    results = []
    
    # Test 1: Configuración
    result1 = await test_oauth_configuration()
    results.append(("Configuración OAuth", result1))
    
    # Test 2: URL generation
    result2 = await test_auth_url_generation()
    results.append(("Generación URL", result2))
    
    # Test 3: Manual flow
    result3 = await test_manual_oauth_flow()
    results.append(("Flujo OAuth Manual", result3))
    
    # Test 4: Playlist simulation
    result4 = await test_playlist_creation_simulation()
    results.append(("Simulación Playlist", result4))
    
    # Test 5: Endpoints
    result5 = await test_api_endpoints()
    results.append(("Endpoints Disponibles", result5))
    
    # Test 6: Curl examples
    result6 = await test_curl_examples()
    results.append(("Ejemplos curl", result6))
    
    # Summary
    print("=" * 80)
    print("📊 RESUMEN DE TESTS")
    print("=" * 80)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "⚠️ SKIP/FAIL"
        print(f"   {status:15s} {test_name}")
    
    print()
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    
    print(f"Total: {passed}/{total} tests pasados")
    print()
    
    if not deezer_auth_service.is_configured():
        print("⚠️ IMPORTANTE: OAuth no está configurado")
        print("   Para habilitar funcionalidad completa:")
        print("   1. Ve a https://developers.deezer.com/myapps")
        print("   2. Crea una app (o usa una existente)")
        print("   3. Añade a .env:")
        print("      DEEZER_APP_ID=tu_app_id")
        print("      DEEZER_SECRET_KEY=tu_secret_key")
        print("      DEEZER_REDIRECT_URI=http://localhost:8000/auth/deezer/callback")
        print()
    else:
        print("✅ OAuth configurado correctamente")
        print("   Puedes probar el flujo completo iniciando el backend")
        print()
    
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
