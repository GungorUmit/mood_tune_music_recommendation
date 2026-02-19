# 🚀 DEPLOYMENT GUIDE - MoodTune

> **Proyecto**: MoodTune - AI Music Discovery  
> **Stack**: Next.js (Frontend) + FastAPI (Backend)  
> **Fecha**: 19 de febrero de 2026

---

## ✅ ARCHIVOS DE CONFIGURACIÓN CREADOS

Los siguientes archivos ya están listos en tu proyecto:

```
✅ render.yaml                    # Configuración deployment Render (backend)
✅ frontend/vercel.json           # Configuración deployment Vercel (frontend)
✅ frontend/.env.production       # Variables de entorno producción
✅ backend/main.py                # Actualizado con CORS producción
```

---

## 📋 ARQUITECTURA FINAL

```
Usuario
   ↓
🌐 https://moodtune.umitgungor.me
   (Frontend - Next.js en Vercel)
   ↓ API calls
🔧 https://api-moodtune.umitgungor.me
   (Backend - FastAPI en Render)
   ↓ External APIs
🤖 OpenAI + 🎵 Deezer
```

---

# 🔴 PASO 1: DEPLOY BACKEND EN RENDER (15 min)

## 1.1. Push código a GitHub (YA HECHO ✅)

```bash
# Ya ejecutaste esto:
git push -u origin master
```

## 1.2. Crear Web Service en Render

1. **Ir a**: https://render.com
2. **Login/Signup** con GitHub
3. **New** → **Web Service**
4. **Connect repository**: `GungorUmit/mood_tune_music_recommendation`
5. **Configuración**:
   
   ```yaml
   Name: moodtune-api
   Region: Oregon (US West)
   Branch: master
   Runtime: Python 3
   Build Command: cd backend && pip install -r requirements.txt
   Start Command: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
   Plan: Free
   ```

6. **Advanced** → **Add Environment Variable** (añadir uno por uno):

   ```bash
   OPENAI_API_KEY=sk-proj-[TU-KEY-AQUI]
   HUGGINGFACE_TOKEN=hf_[TU-TOKEN-AQUI]
   DEEZER_APP_ID=[TU-APP-ID]
   DEEZER_SECRET_KEY=[TU-SECRET]
   DEEZER_REDIRECT_URI=https://api-moodtune.umitgungor.me/auth/deezer/callback
   FRONTEND_URL=https://moodtune.umitgungor.me
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   RATE_LIMIT_PER_HOUR=100
   ```

7. **Create Web Service**

**⏱️ Esperar**: Render tardará ~5-10 minutos en build inicial.

**✅ Verificar**: 
- URL temporal: `https://moodtune-api.onrender.com`
- Abrir: `https://moodtune-api.onrender.com/api/health`
- Deberías ver:
  ```json
  {
    "status": "healthy",
    "version": "1.0.0",
    "environment": "production",
    "cors_enabled": true,
    "allowed_origins": 5
  }
  ```

---

## 1.3. Configurar Custom Domain en Render

1. **En Render Dashboard** → Tu servicio `moodtune-api`
2. **Settings** → **Custom Domains**
3. **Add Custom Domain**: `api-moodtune.umitgungor.me`
4. Render mostrará:
   ```
   Add the following CNAME record to your DNS provider:
   
   Type: CNAME
   Name: api-moodtune
   Value: moodtune-api.onrender.com
   ```

5. **Ir a Namecheap**:
   - Login → Domain List → Manage `umitgungor.me`
   - **Advanced DNS** → **Add New Record**:
     ```
     Type: CNAME Record
     Host: api-moodtune
     Value: moodtune-api.onrender.com
     TTL: Automatic
     ```
   - **Save All Changes**

6. **Esperar 5-30 minutos** (propagación DNS)

7. **Verificar**:
   ```bash
   curl https://api-moodtune.umitgungor.me/api/health
   ```

**✅ Backend completado cuando**:
- `https://api-moodtune.umitgungor.me/api/health` responde OK
- Tiene candado 🔒 (SSL automático de Render)

---

# 🔵 PASO 2: DEPLOY FRONTEND EN VERCEL (10 min)

## 2.1. Crear proyecto en Vercel

### **Opción A: Desde CLI (Recomendado)**

```bash
# 1. Instalar Vercel CLI
npm install -g vercel

# 2. Login
vercel login
# Seguir instrucciones (email + verificación)

# 3. Ir a carpeta frontend
cd /Users/umitgungor/Downloads/asistente-musical/frontend

# 4. Deploy
vercel

# Responder prompts:
? Set up and deploy "~/Downloads/asistente-musical/frontend"? Y
? Which scope do you want to deploy to? [Tu cuenta]
? Link to existing project? N
? What's your project's name? moodtune
? In which directory is your code located? ./
? Want to modify these settings? N

# 5. Deploy a producción
vercel --prod
```

### **Opción B: Desde Vercel UI**

1. **Ir a**: https://vercel.com
2. **Login** con GitHub
3. **Add New...** → **Project**
4. **Import Git Repository** → Buscar `mood_tune_music_recommendation`
5. **Configure Project**:
   ```yaml
   Framework Preset: Next.js
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: .next
   Install Command: npm install
   ```

6. **Environment Variables** (añadir):
   ```bash
   NEXT_PUBLIC_API_URL=https://api-moodtune.umitgungor.me
   NEXT_PUBLIC_APP_NAME=MoodTune
   NEXT_PUBLIC_ENVIRONMENT=production
   ```

7. **Deploy**

**⏱️ Esperar**: ~2-5 minutos

**✅ Verificar**:
- URL temporal: `https://moodtune.vercel.app` (o similar)
- Abrir y probar búsqueda

---

## 2.2. Configurar Custom Domain en Vercel

1. **En Vercel Dashboard** → Tu proyecto `moodtune`
2. **Settings** → **Domains**
3. **Add**: `moodtune.umitgungor.me`
4. Vercel mostrará:
   ```
   Add the following CNAME record:
   
   Type: CNAME
   Name: moodtune
   Value: cname.vercel-dns.com
   ```

5. **Ir a Namecheap**:
   - **Advanced DNS** → **Add New Record**:
     ```
     Type: CNAME Record
     Host: moodtune
     Value: cname.vercel-dns.com
     TTL: Automatic
     ```
   - **Save All Changes**

6. **En Vercel**: Click **Refresh** (verificará DNS)

7. **Esperar 5-30 minutos** (propagación DNS + SSL)

**✅ Frontend completado cuando**:
- `https://moodtune.umitgungor.me` carga
- Tiene candado 🔒 (SSL automático de Vercel)
- Puede hacer búsquedas (llama al backend correctamente)

---

# 🟢 PASO 3: VERIFICACIÓN COMPLETA (5 min)

## 3.1. Test Backend

```bash
# 1. Health check
curl https://api-moodtune.umitgungor.me/api/health

# Expected:
# {
#   "status": "healthy",
#   "environment": "production",
#   ...
# }

# 2. CORS headers
curl -I https://api-moodtune.umitgungor.me/api/health

# Expected:
# access-control-allow-origin: https://moodtune.umitgungor.me
```

## 3.2. Test Frontend

1. **Abrir**: https://moodtune.umitgungor.me
2. **Escribir query**: "triste y melancólico después de una ruptura"
3. **Click**: "Descubrir Música"
4. **Verificar**:
   - ✅ Loading state aparece
   - ✅ Resultados se muestran
   - ✅ Previews de audio funcionan
   - ✅ No hay errores en Console (F12)

## 3.3. Test DevTools (Network)

1. **F12** → **Network** tab
2. Hacer búsqueda
3. Buscar request a `api-moodtune.umitgungor.me`
4. **Verificar**:
   - ✅ Status: 200 OK
   - ✅ Response contiene tracks
   - ✅ No hay errores CORS

---

# 🟣 PASO 4: INTEGRAR EN PORTFOLIO (5 min)

En tu portfolio `umitgungor.me`:

## 4.1. Añadir sección Projects

```html
<section id="projects" class="projects-section">
  <h2>Featured Projects</h2>
  
  <div class="project-grid">
    
    <!-- MoodTune Project -->
    <div class="project-card featured">
      <div class="project-image">
        <img src="/images/moodtune-preview.png" alt="MoodTune Screenshot">
        <div class="project-overlay">
          <span class="badge">AI Project</span>
        </div>
      </div>
      
      <div class="project-content">
        <h3>🎵 MoodTune</h3>
        <p class="project-description">
          AI-powered music discovery platform that translates emotional 
          descriptions into personalized song recommendations using 
          natural language processing.
        </p>
        
        <div class="tech-stack">
          <span class="tech-tag">Next.js</span>
          <span class="tech-tag">FastAPI</span>
          <span class="tech-tag">OpenAI GPT-4</span>
          <span class="tech-tag">Deezer API</span>
          <span class="tech-tag">TypeScript</span>
          <span class="tech-tag">Python</span>
        </div>
        
        <div class="project-stats">
          <span>🌐 Bilingual (ES/EN)</span>
          <span>🎨 Dark/Light Theme</span>
          <span>🎵 30s Audio Previews</span>
        </div>
        
        <div class="project-links">
          <a href="https://moodtune.umitgungor.me" 
             target="_blank" 
             rel="noopener"
             class="btn-primary">
            🚀 Launch App
          </a>
          <a href="https://github.com/GungorUmit/mood_tune_music_recommendation" 
             target="_blank"
             rel="noopener"
             class="btn-secondary">
            📦 View Code
          </a>
        </div>
      </div>
    </div>
    
    <!-- Más proyectos... -->
    
  </div>
</section>
```

## 4.2. Estilos sugeridos (CSS)

```css
.project-card.featured {
  border: 2px solid #8B5CF6;
  box-shadow: 0 8px 24px rgba(139, 92, 246, 0.2);
}

.project-card.featured:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(139, 92, 246, 0.3);
}

.tech-tag {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 16px rgba(139, 92, 246, 0.3);
}
```

---

# ✅ CHECKLIST FINAL

Antes de decir "completado":

- [ ] **Backend funcionando**
  - [ ] `https://api-moodtune.umitgungor.me/api/health` responde
  - [ ] SSL activo (🔒 candado verde)
  - [ ] Variables de entorno configuradas en Render
  
- [ ] **Frontend funcionando**
  - [ ] `https://moodtune.umitgungor.me` carga
  - [ ] SSL activo (🔒 candado verde)
  - [ ] Puede hacer búsquedas exitosamente
  - [ ] Previews de audio funcionan
  
- [ ] **Integración correcta**
  - [ ] Frontend llama al backend correcto (api-moodtune...)
  - [ ] CORS funciona (sin errores en console)
  - [ ] Búsquedas devuelven resultados
  
- [ ] **Portfolio actualizado**
  - [ ] Link a MoodTune añadido
  - [ ] Link a GitHub añadido
  - [ ] Descripción clara del proyecto
  
- [ ] **Documentación**
  - [ ] README en GitHub actualizado con links
  - [ ] Video demo grabado (pendiente)
  - [ ] Screenshots en portfolio

---

# 🚨 TROUBLESHOOTING

## Problema: Backend no responde

```bash
# 1. Verificar logs de Render
# Dashboard → moodtune-api → Logs

# 2. Verificar que el servicio está "Live" (no "Deploying")

# 3. Verificar variables de entorno
# Settings → Environment → verificar OPENAI_API_KEY

# 4. Re-deploy manual
# Dashboard → Manual Deploy → Deploy latest commit
```

## Problema: Frontend no puede conectar al backend

```bash
# 1. Verificar variable de entorno en Vercel
# Settings → Environment Variables
# NEXT_PUBLIC_API_URL debe ser: https://api-moodtune.umitgungor.me

# 2. Verificar CORS en backend
curl -H "Origin: https://moodtune.umitgungor.me" \
     -I https://api-moodtune.umitgungor.me/api/health

# Debe tener header:
# access-control-allow-origin: https://moodtune.umitgungor.me

# 3. Re-deploy frontend
vercel --prod
```

## Problema: DNS no propaga

```bash
# 1. Verificar configuración DNS en Namecheap
# Advanced DNS → verificar que CNAME está correcto

# 2. Verificar propagación
dig moodtune.umitgungor.me
dig api-moodtune.umitgungor.me

# 3. Probar con diferentes DNS
nslookup moodtune.umitgungor.me 8.8.8.8
nslookup api-moodtune.umitgungor.me 8.8.8.8

# 4. Esperar más tiempo (puede tardar hasta 48h, pero normalmente 5-30 min)
```

## Problema: OpenAI API key inválida

```bash
# 1. Verificar que la key es correcta
# En Render → Environment → OPENAI_API_KEY

# 2. Generar nueva key
# https://platform.openai.com/api-keys

# 3. Actualizar en Render
# Environment → Edit → Guardar → Re-deploy
```

---

# 📊 MÉTRICAS DE ÉXITO

Cuando todo funcione, deberías ver:

```
✅ Backend Response Time: ~2-3 segundos (primera request)
✅ Frontend Load Time: <2 segundos
✅ SSL Grade: A+ (en ambos dominios)
✅ Uptime: 99%+ (Free tier de Render puede dormirse después de 15 min de inactividad)
```

**Nota sobre Free Tier de Render**:
- El servicio "duerme" después de 15 minutos sin tráfico
- Primera request después de dormir tarda ~30-60 segundos (cold start)
- Requests subsecuentes son normales (~2-3s)

---

# 🎉 FELICIDADES

Si llegaste aquí y todo funciona:

1. ✅ Tienes un proyecto full-stack en producción
2. ✅ Con dominio custom profesional
3. ✅ SSL activo en ambos servicios
4. ✅ Integrado en tu portfolio
5. ✅ Listo para mostrar en entrevistas

**Siguiente paso**: Grabar video demo (3 min) siguiendo [VIDEO_DEMO_GUIDE.md](VIDEO_DEMO_GUIDE.md)

---

**Tiempo total estimado**: ~40 minutos  
**Costo**: $0 (todo en free tiers)  
**Dudas**: Revisa troubleshooting o consulta docs oficiales

**Autor**: GitHub Copilot  
**Fecha**: 19 de febrero de 2026  
**Proyecto**: MoodTune - AI Music Discovery
