# 🎵 Deezer Full Songs - OAuth & Playlist Flow

## 🚨 Limitaciones de Deezer API

### Preview vs Full Tracks

**Deezer API Pública (sin autenticación):**
- ✅ Búsqueda de canciones ilimitada
- ✅ Metadata completa (título, artista, álbum, cover)
- ✅ **Preview URLs: Solo 30 segundos**
- ❌ No permite reproducir canciones completas
- ❌ No puede crear playlists

**Con Deezer OAuth (usuario autenticado):**
- ✅ Todo lo anterior +
- ✅ Crear playlists en la cuenta del usuario
- ✅ Añadir tracks a playlists
- ✅ **Abrir playlist en Deezer app/web → Full songs**
- ⚠️ Reproducción full solo en app oficial Deezer (no en terceros)

### ⚖️ Términos de Servicio Deezer
Según [Deezer API TOS](https://developers.deezer.com/termsofuse):
- ✅ Permitido: Previews 30s en tu app
- ✅ Permitido: Crear playlists vía OAuth
- ✅ Permitido: Deep links a Deezer app (`deezer://playlist/123`)
- ❌ Prohibido: Streaming full tracks fuera de Deezer
- ❌ Prohibido: Descargar/cachear audio

## 🔐 Solución: OAuth + Playlist Creation

### Flujo Completo (UX Óptima)

```
1. Usuario describe mood → "triste después de una ruptura"
2. LLM analiza → mood_tags: ["triste", "melancólico"]
3. Deezer search → 10 tracks con preview 30s
4. Usuario escucha previews en la app
5. Usuario hace clic en "Guardar Playlist en Deezer"
   ├─ Si no está autenticado → Redirect a OAuth
   └─ Si autenticado → Crear playlist automáticamente
6. Backend crea playlist en cuenta del usuario (Deezer API)
7. Frontend abre playlist en Deezer app/web → ¡Full songs!
```

### Ventajas de este Approach
- ✅ **Legal**: Cumple 100% con Deezer TOS
- ✅ **UX fluida**: 2 clicks (login + crear playlist)
- ✅ **Sin Premium**: Free tier de Deezer permite playlists
- ✅ **Cross-platform**: Deep links funcionan iOS/Android/Web
- ✅ **Persistente**: Playlist queda en cuenta del usuario

## 🛠️ Implementación Técnica

### 1. Registrar App en Deezer

1. Ve a [Deezer Developers](https://developers.deezer.com/myapps)
2. Crea nueva app
3. Configura:
   - **Application Domain:** `localhost` (desarrollo)
   - **Redirect URL:** `http://localhost:8000/auth/deezer/callback`
4. Copia `App ID` y `Secret Key`

### 2. Variables de Entorno

```bash
# .env
DEEZER_APP_ID=your_app_id_here
DEEZER_SECRET_KEY=your_secret_key_here
DEEZER_REDIRECT_URI=http://localhost:8000/auth/deezer/callback
```

### 3. Backend FastAPI Endpoints

#### OAuth Flow
```python
# GET /auth/deezer/login
# Redirige a Deezer OAuth con perms: manage_library

# GET /auth/deezer/callback
# Recibe code, intercambia por access_token
# Guarda token en sesión/DB
```

#### Playlist Creation
```python
# POST /playlist/create
# Body: { tracks: ["track_id1", "track_id2", ...], mood_name: "Triste" }
# 1. Crear playlist: POST /user/me/playlists
# 2. Añadir tracks: POST /playlist/{id}/tracks
# 3. Retornar playlist URL
```

### 4. Frontend Botones

**Componente: PlaylistSaveButton.tsx**
```typescript
const handleSavePlaylist = async () => {
  // 1. Check if user is authenticated
  const isAuth = await checkDeezerAuth();
  
  if (!isAuth) {
    // Redirect to OAuth login
    window.location.href = 'http://localhost:8000/auth/deezer/login';
    return;
  }
  
  // 2. Create playlist with mood tracks
  const response = await fetch('/api/playlist/create', {
    method: 'POST',
    body: JSON.stringify({ 
      tracks: selectedTracks.map(t => t.id),
      mood_name: moodTags.join(', ')
    })
  });
  
  const { playlist_url } = await response.json();
  
  // 3. Open in Deezer app/web
  window.open(playlist_url, '_blank');
};
```

## 📦 Instalación de Dependencias

```bash
pip install requests python-dotenv fastapi uvicorn
# No necesitas deezer-python, usamos requests directo
```

## 🔄 Flujo OAuth Detallado

### Step 1: Iniciar Login
```http
GET https://connect.deezer.com/oauth/auth.php
  ?app_id={DEEZER_APP_ID}
  &redirect_uri={REDIRECT_URI}
  &perms=manage_library
```

Usuario ve pantalla de Deezer pidiendo permisos.

### Step 2: Callback con Code
```http
GET http://localhost:8000/auth/deezer/callback?code=ABC123
```

### Step 3: Exchange Code por Token
```http
GET https://connect.deezer.com/oauth/access_token.php
  ?app_id={DEEZER_APP_ID}
  &secret={DEEZER_SECRET_KEY}
  &code=ABC123
  &output=json

Response: {"access_token": "fr123xyz", "expires": 3600}
```

### Step 4: Guardar Token
```python
# Guardar en sesión o DB asociado al user
user_session['deezer_token'] = access_token
```

### Step 5: Crear Playlist
```http
POST https://api.deezer.com/user/me/playlists
  ?access_token=fr123xyz
  &title=Mood: Triste y Melancólico
  &description=Generado por Asistente Musical

Response: {"id": "12345678"}
```

### Step 6: Añadir Tracks
```http
POST https://api.deezer.com/playlist/12345678/tracks
  ?access_token=fr123xyz
  &songs=3088638,916424,3135556

Response: true
```

### Step 7: Abrir Playlist
```typescript
// Deep link para app nativa
window.location.href = 'deezer://playlist/12345678';

// Fallback para web
window.open('https://www.deezer.com/playlist/12345678', '_blank');
```

## 🧪 Testing OAuth Flow

### Test Manual

1. **Start backend:**
   ```bash
   cd backend
   python main.py
   ```

2. **Visita OAuth login:**
   ```
   http://localhost:8000/auth/deezer/login
   ```

3. **Autoriza en Deezer**

4. **Callback debe redirigir con token**

5. **Test crear playlist:**
   ```bash
   curl -X POST http://localhost:8000/api/playlist/create \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer {deezer_token}" \
     -d '{
       "tracks": ["3088638", "916424"],
       "mood_name": "Test Mood"
     }'
   ```

### Test Unitario
```python
# backend/test_deezer_oauth.py
async def test_oauth_flow():
    # Simular callback
    response = await client.get("/auth/deezer/callback?code=test123")
    assert response.status_code == 200
    assert "access_token" in response.cookies
```

## 🎨 UI/UX Recomendaciones

### Estado Sin Autenticación
```
┌─────────────────────────────────────┐
│  🎵 10 canciones encontradas        │
│                                      │
│  [Preview 30s] Track 1              │
│  [Preview 30s] Track 2              │
│  ...                                 │
│                                      │
│  💡 Para escuchar canciones          │
│     completas:                       │
│  [🔐 Conectar con Deezer]           │
└─────────────────────────────────────┘
```

### Estado Autenticado
```
┌─────────────────────────────────────┐
│  🎵 10 canciones encontradas        │
│  ✅ Conectado como @usuario         │
│                                      │
│  [Preview] Track 1                  │
│  [Preview] Track 2                  │
│  ...                                 │
│                                      │
│  [💾 Guardar Playlist & Abrir en    │
│      Deezer] ← Full Songs!          │
└─────────────────────────────────────┘
```

## 🚀 Deployment Producción

### Actualizar Redirect URI
```bash
# .env.production
DEEZER_REDIRECT_URI=https://tu-dominio.com/auth/deezer/callback
```

### Configurar en Deezer Developers
- Application Domain: `tu-dominio.com`
- Redirect URL: `https://tu-dominio.com/auth/deezer/callback`

### HTTPS Obligatorio
Deezer OAuth requiere HTTPS en producción (desarrollo permite HTTP localhost).

## 📊 Alternativas Consideradas

### ❌ Spotify
- Requiere Premium para playback
- OAuth más complejo
- TOS más estrictos

### ❌ YouTube Music
- No tiene API pública oficial
- Viola TOS usar APIs no oficiales

### ✅ Deezer (Elegido)
- Free tier permite playlists
- OAuth simple
- TOS permite deep links
- Previews 30s sin auth

## 🔒 Seguridad

### Token Storage
- ⚠️ No guardar access_token en localStorage (XSS risk)
- ✅ Usar httpOnly cookies
- ✅ Refresh tokens si implementas sesiones largas

### Rate Limiting
- Deezer API: ~50 requests/5 seconds
- Implementar cache para metadata
- Throttle playlist creation (1 por minuto)

## 📚 Referencias

- [Deezer API Docs](https://developers.deezer.com/api)
- [Deezer OAuth Guide](https://developers.deezer.com/api/oauth)
- [Deezer TOS](https://developers.deezer.com/termsofuse)
- [Deep Linking Deezer](https://developers.deezer.com/guidelines/url-linking)

---

**Próximos Pasos:**
1. ✅ Implementar OAuth endpoints (backend)
2. ✅ Crear servicio DeezerAuth (backend)
3. ✅ Endpoint crear playlist
4. ✅ Frontend: Botón "Conectar Deezer"
5. ✅ Frontend: Botón "Guardar Playlist"
6. ✅ Tests OAuth flow

**Fecha:** 17 febrero 2026  
**Estado:** Implementación en curso
