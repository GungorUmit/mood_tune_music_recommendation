# 🎵 Reproducción de Canciones Completas - Guía de Implementación

## ✅ Implementación Completa

Se ha implementado exitosamente el flujo OAuth de Deezer para crear playlists y reproducir canciones completas.

### 🎯 ¿Qué se logró?

1. **Previews 30s** → Disponibles sin autenticación ✅
2. **OAuth Deezer** → Autenticación de usuarios ✅
3. **Crear Playlists** → Guardar mood tracks en cuenta del usuario ✅
4. **Canciones Completas** → Abrir playlist en Deezer app/web ✅
5. **Frontend Integrado** → Botón "Guardar Playlist en Deezer" ✅

---

## 🚀 Configuración Rápida

### Paso 1: Registrar App en Deezer

1. Ve a **[Deezer Developer Portal](https://developers.deezer.com/myapps)**
2. Click en **"Create new App"** o usa una existente
3. Completa los campos:
   - **Application Name:** `Asistente Musical` (o el nombre que prefieras)
   - **Application Domain:** `localhost` (para desarrollo)
   - **Redirect URL after authentication:** `http://localhost:8000/auth/deezer/callback`
   - **Description:** Tu descripción
4. Guarda y copia:
   - **Application ID** (número)
   - **Secret Key** (string largo)

### Paso 2: Configurar Variables de Entorno

Edita el archivo `.env` en `backend/`:

```bash
# Deezer OAuth Configuration
DEEZER_APP_ID=123456  # Tu Application ID
DEEZER_SECRET_KEY=tu_secret_key_aquí  # Tu Secret Key
DEEZER_REDIRECT_URI=http://localhost:8000/auth/deezer/callback

# Hugging Face (ya configurado)
HUGGINGFACE_TOKEN=hf_tu_token_aquí

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

### Paso 3: Reiniciar Backend

```bash
cd backend
python main.py
```

Deberías ver:
```
INFO:     Application startup complete.
```

Sin advertencias de `DEEZER_APP_ID not configured`.

### Paso 4: Reiniciar Frontend

```bash
cd frontend
npm run dev
```

### Paso 5: ¡Probar!

1. Abre **http://localhost:3000**
2. Describe un mood: _"triste después de una ruptura"_
3. Click **"Descubrir Música"**
4. Verás:
   - ✅ Metadata del mood
   - ✅ Botón **"🔐 Conectar con Deezer"**
5. Click en **"Conectar con Deezer"**
   - Serás redirigido a Deezer
   - Autoriza la aplicación
   - Vuelves al frontend autenticado
6. Ahora verás:
   - ✅ Usuario conectado (avatar + nombre)
   - ✅ Botón **"💾 Guardar Playlist en Deezer"**
7. Click en **"Guardar Playlist"**
   - Se crea playlist en tu cuenta
   - Se abre automáticamente en Deezer
   - **¡Canciones completas! 🎉**

---

## 📋 Archivos Creados/Modificados

### Backend

1. **`services/deezer_auth_service.py`** (NUEVO)
   - Servicio OAuth completo
   - Métodos: `get_auth_url()`, `exchange_code_for_token()`, `create_playlist()`, `create_mood_playlist()`

2. **`main.py`** (MODIFICADO)
   - Nuevos endpoints OAuth:
     - `GET /auth/deezer/status` - Verificar configuración
     - `GET /auth/deezer/login` - Iniciar OAuth
     - `GET /auth/deezer/callback` - Callback OAuth
     - `GET /auth/deezer/user` - Info usuario
     - `POST /auth/deezer/logout` - Cerrar sesión
     - `POST /api/playlist/create` - Crear playlist

3. **`.env.example`** (MODIFICADO)
   - Añadidas variables `DEEZER_APP_ID`, `DEEZER_SECRET_KEY`, `DEEZER_REDIRECT_URI`

4. **`test_deezer_oauth.py`** (NUEVO)
   - Tests unitarios para OAuth
   - Ejecutar: `python test_deezer_oauth.py`

5. **`DEEZER_OAUTH_GUIDE.md`** (NUEVO)
   - Documentación técnica completa
   - Explica limitaciones, TOS, y alternativas

### Frontend

1. **`components/DeezerPlaylistButton.tsx`** (NUEVO)
   - Componente React para OAuth + crear playlist
   - Estados: no autenticado, autenticado, loading, success, error

2. **`components/DeezerPlaylistButton.module.css`** (NUEVO)
   - Estilos para el botón con diseño Vibrante Musical

3. **`app/page.tsx`** (MODIFICADO)
   - Importa y renderiza `DeezerPlaylistButton`
   - Posicionado después de metadata, antes de playlist player

---

## 🔧 Testing

### Test 1: Verificar Configuración

```bash
cd backend
python test_deezer_oauth.py
```

Deberías ver:
```
✅ OAuth está configurado
✅ Todos los endpoints están implementados
```

### Test 2: Verificar Endpoint Status

```bash
curl http://localhost:8000/auth/deezer/status
```

Response esperado:
```json
{
  "oauth_enabled": true,
  "message": "OAuth configured"
}
```

### Test 3: Flujo OAuth Manual

1. Visita: **http://localhost:8000/auth/deezer/login**
2. Autoriza en Deezer
3. Serás redirigido a `http://localhost:3000?deezer_auth=success&user=TuNombre`
4. Cookie `deezer_token` estará guardada

### Test 4: Verificar Autenticación

```bash
curl http://localhost:8000/auth/deezer/user \
  -b cookies.txt
```

Response esperado:
```json
{
  "authenticated": true,
  "user": {
    "id": 123456,
    "name": "Tu Nombre",
    "picture": "https://..."
  }
}
```

### Test 5: Crear Playlist (con token)

```bash
curl -X POST http://localhost:8000/api/playlist/create \
  -H 'Content-Type: application/json' \
  -b cookies.txt \
  -d '{
    "track_ids": ["3088638", "916424", "3135556"],
    "mood_name": "Test Mood",
    "genres": ["pop", "indie"],
    "energy": "medium"
  }'
```

Response esperado:
```json
{
  "success": true,
  "playlist_id": "12345678",
  "playlist_url": "https://www.deezer.com/playlist/12345678",
  "playlist_app_url": "deezer://playlist/12345678",
  "title": "Mood: Test Mood",
  "tracks_count": 3
}
```

---

## 📊 Flujo Completo Explicado

### 1. Usuario sin Autenticar

```
┌─────────────────────────────────────┐
│  Mood: "Triste"                     │
│  10 tracks encontrados              │
│                                      │
│  [Preview 30s] Track 1              │
│  [Preview 30s] Track 2              │
│  ...                                 │
│                                      │
│  💡 ¿Quieres canciones completas?   │
│  [🔐 Conectar con Deezer]           │
└─────────────────────────────────────┘
```

**Click en "Conectar"** →

### 2. Redirect a Deezer OAuth

```
https://connect.deezer.com/oauth/auth.php
  ?app_id=123456
  &redirect_uri=http://localhost:8000/auth/deezer/callback
  &perms=manage_library,offline_access
```

Usuario ve pantalla de Deezer:
```
┌─────────────────────────────────────┐
│  Asistente Musical quiere:          │
│  ✓ Ver tu perfil                    │
│  ✓ Gestionar tus playlists          │
│                                      │
│  [Autorizar]  [Cancelar]            │
└─────────────────────────────────────┘
```

**Usuario click "Autorizar"** →

### 3. Callback con Code

```
GET http://localhost:8000/auth/deezer/callback?code=ABC123XYZ
```

Backend:
1. Intercambia `code` por `access_token`
2. Guarda token en cookie `deezer_token` (httpOnly, secure)
3. Redirect a frontend: `http://localhost:3000?deezer_auth=success&user=TuNombre`

### 4. Usuario Autenticado

```
┌─────────────────────────────────────┐
│  Mood: "Triste"                     │
│  ✅ Conectado como @usuario         │
│                                      │
│  [Preview] Track 1                  │
│  [Preview] Track 2                  │
│  ...                                 │
│                                      │
│  [💾 Guardar Playlist en Deezer]   │
│      (10 canciones)                 │
└─────────────────────────────────────┘
```

**Click en "Guardar Playlist"** →

### 5. Creación de Playlist

Frontend → POST `/api/playlist/create`:
```json
{
  "track_ids": ["3088638", "916424", ...],
  "mood_name": "Triste y Melancólico",
  "genres": ["balada", "indie"],
  "energy": "low"
}
```

Backend:
1. Verifica cookie `deezer_token`
2. Llama Deezer API:
   - `POST /user/me/playlists` → crear playlist
   - `POST /playlist/{id}/tracks` → añadir tracks
3. Retorna URL de playlist

### 6. Abrir en Deezer

Frontend:
1. Intenta deep link: `deezer://playlist/12345678` (app nativa)
2. Fallback a web: `https://www.deezer.com/playlist/12345678`

```
┌─────────────────────────────────────┐
│  🎉 ¡Playlist creada!               │
│                                      │
│  Se ha abierto en Deezer.           │
│  Si no se abrió automáticamente:    │
│                                      │
│  [🎧 Abrir Playlist en Deezer]     │
└─────────────────────────────────────┘
```

**Usuario escucha canciones completas en Deezer app/web** ✅

---

## 🔒 Seguridad

### Tokens Seguros

- ✅ **httpOnly cookies** - No accesibles desde JavaScript (protege contra XSS)
- ✅ **SameSite=lax** - Protección CSRF
- ⚠️ En producción: Añadir `secure=True` (requiere HTTPS)

### Validaciones

- ✅ Verifica token en cada request a `/api/playlist/create`
- ✅ Valida track_ids (max 50 tracks)
- ✅ Sanitiza mood_name (max 100 chars)

### Rate Limiting

Recomendado para producción:
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/api/playlist/create")
@limiter.limit("10/minute")  # Max 10 playlists por minuto
async def create_playlist(...):
    ...
```

---

## 🌐 Deployment Producción

### Backend (Railway/Render/Heroku)

1. **Actualizar `.env` en plataforma:**
   ```bash
   DEEZER_REDIRECT_URI=https://tu-api.com/auth/deezer/callback
   FRONTEND_URL=https://tu-frontend.com
   ```

2. **Actualizar Deezer App:**
   - Application Domain: `tu-api.com`
   - Redirect URL: `https://tu-api.com/auth/deezer/callback`

3. **HTTPS obligatorio** (Deezer OAuth no funciona con HTTP en producción)

### Frontend (Vercel/Netlify)

1. **Environment Variables:**
   ```bash
   NEXT_PUBLIC_API_URL=https://tu-api.com
   ```

2. **CORS en backend:**
   ```python
   allow_origins=[
       "https://tu-frontend.com",
       "http://localhost:3000"  # Keep for local dev
   ]
   ```

---

## ⚠️ Troubleshooting

### Problema: "OAuth not configured"

**Síntoma:**
```
⚠️ WARNING: DEEZER_APP_ID or DEEZER_SECRET_KEY not configured
```

**Solución:**
1. Verifica que `.env` existe en `backend/`
2. Verifica que contiene `DEEZER_APP_ID` y `DEEZER_SECRET_KEY`
3. Reinicia el backend

### Problema: "Failed to obtain access token"

**Síntoma:**
```
❌ Failed to obtain access token
```

**Causas:**
1. **Redirect URI no coincide** - Verifica que sea exacta en Deezer app y `.env`
2. **Secret Key incorrecta** - Verifica que copiaste bien
3. **Code expirado** - Códigos OAuth expiran en 10 min, intenta de nuevo

**Solución:**
```bash
# Verificar redirect URI
echo $DEEZER_REDIRECT_URI
# Debe ser: http://localhost:8000/auth/deezer/callback

# Re-intentar OAuth flow
curl http://localhost:8000/auth/deezer/login
```

### Problema: "Playlist created but failed to add tracks"

**Síntoma:**
```
⚠️ Playlist created but failed to add tracks
```

**Causas:**
1. **Track IDs inválidos** - Algunas canciones no existen o no están disponibles
2. **Permisos insuficientes** - Verifica que OAuth tiene `manage_library`

**Solución:**
1. Verifica los track IDs en Deezer:
   ```bash
   curl https://api.deezer.com/track/3088638
   ```
2. Re-autoriza la app con permisos correctos

### Problema: Frontend no muestra botón

**Síntoma:**
No aparece el botón "Conectar con Deezer"

**Causas:**
1. Backend no está corriendo
2. `DEEZER_APP_ID` no configurado
3. No hay tracks (búsqueda sin resultados)

**Solución:**
1. Verifica backend:
   ```bash
   curl http://localhost:8000/auth/deezer/status
   ```
   Debe retornar: `{"oauth_enabled": true}`

2. Verifica que hay tracks en `results.tracks`

---

## 📚 Referencias

- [Deezer API Documentation](https://developers.deezer.com/api)
- [Deezer OAuth Guide](https://developers.deezer.com/api/oauth)
- [Deezer Developer Portal](https://developers.deezer.com/myapps)
- [Deezer Terms of Use](https://developers.deezer.com/termsofuse)
- [Deep Linking](https://developers.deezer.com/guidelines/url-linking)

---

## 🎯 Próximos Pasos

### Mejoras Sugeridas

1. **Refresh Tokens**
   - Implementar renovación automática de tokens
   - Guardar en DB para sesiones persistentes

2. **Playlist Management**
   - Listar playlists existentes
   - Añadir tracks a playlists existentes
   - Eliminar/editar playlists

3. **Social Features**
   - Compartir playlists
   - Seguir a otros usuarios
   - Playlists colaborativas

4. **Analytics**
   - Track qué moods generan más playlists
   - Géneros más populares
   - Engagement metrics

5. **Multi-idioma en Playlists**
   - Títulos y descripciones en idioma del usuario
   - Traducción automática de moods

---

## ✅ Checklist de Implementación

- [x] Servicio OAuth configurado (`deezer_auth_service.py`)
- [x] Endpoints backend implementados
- [x] Frontend component creado (`DeezerPlaylistButton.tsx`)
- [x] Integración en página principal
- [x] Tests unitarios (`test_deezer_oauth.py`)
- [x] Documentación completa
- [ ] Deezer App registrada (requiere acción del usuario)
- [ ] `.env` configurado con credentials (requiere acción del usuario)
- [ ] Testing end-to-end con OAuth real
- [ ] Deployment en producción

---

**¡Listo para usar!** 🎉

Una vez configures tu Deezer App y añadas las credentials al `.env`, podrás crear playlists y escuchar canciones completas en Deezer.

**Autor:** Asistente Musical AI  
**Fecha:** 17 de febrero de 2026  
**Versión:** 1.0
