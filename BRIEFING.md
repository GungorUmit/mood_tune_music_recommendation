# 📋 BRIEFING - Proyecto Individual Bootcamp IA

## 🎯 1. Problema Identificado

### **Contexto**
Las plataformas de streaming musical (Spotify, Deezer, Apple Music) ofrecen millones de canciones, pero encontrar música que encaje con un **estado emocional específico** requiere:
- Navegar por múltiples playlists genéricas
- Conocer nombres de géneros específicos
- Perder tiempo en búsquedas iterativas

### **Pain Points**
- ❌ "Quiero música para concentrarme estudiando de noche" → ¿qué playlist busco?
- ❌ "Me siento triste después de una ruptura" → ¿lo-fi? ¿indie? ¿baladas?
- ❌ Barreras idiomáticas: usuarios no técnicos no conocen términos como "downtempo" o "chillhop"

### **Público Objetivo**
- Personas que buscan música por **contexto emocional**, no por género
- Usuarios que quieren descubrir música nueva sin esfuerzo cognitivo
- Edades 18-45 años, familiarizados con streaming pero frustrados con la búsqueda

---

## 💡 2. Propuesta de Solución

### **Concepto**
**MoodTune**: Un asistente de descubrimiento musical que traduce descripciones naturales en lenguaje humano ("estudiando con lluvia, necesito foco") a recomendaciones musicales precisas.

### **¿Por qué IA?**
- **LLM (GPT-4o-mini)** interpreta el **contexto semántico** del mood:
  - Extrae emociones ("triste", "energético", "romántico")
  - Infiere nivel de energía (low/medium/high)
  - Traduce a géneros musicales relevantes
  - Genera queries optimizadas para APIs de música

- **Sin IA**: Solo podríamos hacer búsqueda literal (keyword matching), perdiendo contexto emocional complejo.

### **Valor único**
- ✅ Interfaz en **lenguaje natural** (vs menús y filtros complejos)
- ✅ **Bilingüe** (español e inglés) con detección automática
- ✅ **Previews instantáneas** de 30 segundos (sin login)
- ✅ Resultados **explicados** (metadata con mood interpretado)

---

## 🏗️ 3. MVP Definido

### **Alcance Mínimo (In-Scope)**
- [x] Input de texto libre (10-500 caracteres)
- [x] Análisis de mood con LLM (OpenAI GPT-4o-mini)
- [x] Búsqueda en Deezer Public API (sin autenticación)
- [x] Previews de audio (30s snippets)
- [x] Frontend responsive con Next.js + TypeScript
- [x] Backend API con FastAPI
- [x] Soporte bilingüe (ES/EN)
- [x] Rate limiting básico (10 req/min)

### **Fuera de Scope (Fase 2 potencial)**
- [ ] Autenticación de usuarios
- [ ] Creación de playlists persistentes
- [ ] Historial de búsquedas
- [ ] Modelo ML propio (en vez de OpenAI)
- [ ] Integración con Spotify

---

## 🛠️ 4. Arquitectura Técnica

```
┌─────────────┐
│   Usuario   │
└──────┬──────┘
       │ Query: "triste y melancólico"
       ▼
┌─────────────────────────────────┐
│  FRONTEND (Next.js + TS)        │
│  - Validación input (10-500)    │
│  - UI states (idle/loading/OK)  │
│  - Audio preview player         │
└────────────┬────────────────────┘
             │ POST /api/discover
             ▼
┌─────────────────────────────────┐
│  BACKEND (FastAPI + Python)     │
│  - Rate limiting (10/min/IP)    │
│  - CORS middleware              │
└────────────┬────────────────────┘
             │
    ┌────────┴────────┐
    ▼                 ▼
┌──────────┐    ┌──────────────┐
│ OpenAI   │    │ Deezer API   │
│ GPT-4o   │    │ (Search)     │
│ -mini    │    │              │
│          │    │              │
│ Analiza  │    │ Devuelve     │
│ mood     │    │ tracks       │
└──────────┘    └──────────────┘
```

### **Flujo de Datos**
1. Usuario escribe: "estudiando tarde con lluvia, necesito foco"
2. Frontend valida y envía a `/api/discover` (con idioma detectado)
3. Backend llama a **LLM Service** → OpenAI analiza y devuelve:
   ```json
   {
     "mood_tags": ["focused", "calm", "studious"],
     "energy": "low",
     "genres": ["lo-fi", "ambient", "instrumental"],
     "search_query": "lo-fi study calm focus"
   }
   ```
4. Backend llama a **Deezer Service** con `search_query`
5. Deezer devuelve ~25 tracks con previews
6. Backend formatea y devuelve JSON al frontend
7. Frontend muestra cards con audio players

---

## 📚 5. Stack Tecnológico

| Capa | Tecnología | Justificación |
|------|-----------|---------------|
| **Frontend** | Next.js 14 (App Router) | SSR/SSG, React optimizado, TypeScript nativo |
| **UI Components** | React 19 + CSS Modules | Componentes reutilizables, estilos scoped |
| **Backend** | FastAPI (Python 3.11+) | Async, auto-docs, validación con Pydantic |
| **LLM** | OpenAI GPT-4o-mini | Costo-eficiente, JSON mode nativo, 128K context |
| **Music API** | Deezer Public API | Gratis, sin OAuth para búsqueda/previews |
| **HTTP Client (backend)** | httpx | Async requests necesarios para FastAPI |
| **Rate Limiting** | slowapi | Compatible con FastAPI, basado en IP |
| **Deployment** | Vercel (FE) + Render (BE) | Free tiers, CI/CD integrado |

---

## 💾 6. Datos Utilizados

### **Fuente Principal**
- **Deezer Public API** (https://api.deezer.com)
  - Catálogo: ~90M tracks
  - Géneros: Pop, Rock, Hip-Hop, Electronic, Classical, Jazz, etc.
  - Previews: MP3 de 30 segundos para cada track

### **Dataset Interno (Caché)**
- **mood_cache.json** (backend/datasets/)
  - Almacena pares `(user_query, llm_analysis)` para acelerar respuestas repetidas
  - Inicialmente vacío, se va poblando con uso real
  - Ventaja: Reduce costos de llamadas a OpenAI (cache hits ~200ms vs 2-3s)

### **Sin datos de entrenamiento**
- No se entrena un modelo ML propio (fuera de scope del MVP)
- Se usa transfer learning con GPT-4o-mini pre-entrenado

---

## 📅 7. Plan de Desarrollo (Estimado)

| Fase | Duración | Tareas |
|------|----------|--------|
| **Setup inicial** | 1 día | Crear repos, configurar FastAPI + Next.js, estructura de carpetas |
| **Backend core** | 2 días | LLM service, Deezer service, endpoint `/api/discover`, validación |
| **Frontend core** | 2 días | Form, TrackCard, audio preview, estados de carga |
| **Features UX** | 1.5 días | Bilingüe, tema oscuro/claro, ejemplos clickeables |
| **Seguridad** | 0.5 días | Rate limiting, CORS, `.env.example`, SECURITY.md |
| **Testing local** | 1 día | Tests manuales, scripts de prueba (test_llm_service.py) |
| **Documentación** | 1 día | README, PROJECT_STATUS, BRIEFING, ARQUITECTURA |
| **Deployment** | 1 día | Render + Vercel setup, variables de entorno producción |
| **Video demo** | 0.5 días | Grabar, editar, subir demo de 3 minutos |

**Total estimado**: ~10 días (asumiendo dedicación full-time)

---

## ✅ 8. Criterios de Éxito

### **Técnicos**
- [x] Backend responde en <3 segundos (promedio)
- [x] Frontend sin errores de TypeScript
- [x] Tests manuales pasando (español e inglés)
- [x] CORS configurado correctamente
- [x] Rate limiting funcionando (protección contra abuso)

### **De Negocio**
- [ ] Demo funcional mostrable en presentación de 5 min
- [ ] Código en GitHub con commits limpios
- [ ] README profesional (puede incluirse en portfolio)

### **De Aprendizaje (Bootcamp)**
- [x] Integración real de LLM en un producto usable
- [x] Arquitectura cliente-servidor bien diseñada
- [x] Buenas prácticas de seguridad y documentación
- [x] Proyecto que demuestra habilidades full-stack + IA

---

## 🚀 9. Próximos Pasos Inmediatos

1. ✅ Implementar MVP (COMPLETADO)
2. ⚠️ Crear video demo (PENDIENTE - CRÍTICO)
3. ⚠️ Finalizar documentación (ARQUITECTURA.md faltante)
4. ⚠️ Subir a GitHub y verificar que .env no esté incluido
5. ⚠️ Deploy a Vercel + Render (opcional pero recomendado)
6. ✅ Preparar presentación de 5 minutos

---

**Autor**: Umit Gungor  
**Proyecto**: MoodTune - AI-Powered Music Discovery  
**Bootcamp**: Proyecto Individual IA  
**Fecha**: Febrero 2026
