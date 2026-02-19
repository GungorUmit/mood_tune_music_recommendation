# 🎬 GUÍA DE GRABACIÓN - Video Demo MoodTune

## 🎯 Objetivo
Grabar un video de **2-3 minutos** demostrando MoodTune funcionalmente para cumplir con requisitos del Bootcamp.

---

## 📋 Checklist Antes de Grabar

### **Setup Técnico**
- [ ] Backend corriendo: `cd backend && python main.py` (puerto 8000)
- [ ] Frontend corriendo: `cd frontend && npm run dev` (puerto 3000)
- [ ] Navegador abierto en `http://localhost:3000`
- [ ] Audio del sistema funcionando (para previews de canciones)
- [ ] Cerrar tabs innecesarias (solo MoodTune visible)

### **Setup de Grabación**
- [ ] Herramienta de grabación lista:
  - **Mac**: QuickTime Player (gratis)
  - **Windows**: OBS Studio (gratis) o Xbox Game Bar
  - **Multiplataforma**: Loom (gratis, recomendado)
- [ ] Micrófono testeado (audio claro)
- [ ] Ventana del navegador en **tamaño medio** (no fullscreen para mejor visibilidad)
- [ ] Preparar script mental (ver abajo)

---

## 🎥 Estructura del Video (2:30 min)

### **INTRO (0:00 - 0:20) - 20 segundos**
```
[Pantalla: MoodTune homepage]

🎤 Narración:
"Hola, mi nombre es Umit y este es MoodTune, mi proyecto final del 
Bootcamp de IA. Es un asistente de descubrimiento musical que traduce 
descripciones emocionales en lenguaje natural a recomendaciones 
musicales personalizadas usando Inteligencia Artificial."

[Mostrar brevemente la interfaz sin hacer nada]
```

---

### **DEMO 1: Query en Español (0:20 - 1:00) - 40 segundos**
```
[Escribir en el textarea mientras hablas]

🎤 Narración:
"Voy a demostrar cómo funciona. Imagina que me siento triste después 
de una ruptura y quiero música apropiada."

[Escribir]: "triste y melancólico después de una ruptura"

"Hago click en Descubrir Música..."

[Click en botón]
[Esperar loading state - mostrar spinner]

"El sistema está usando OpenAI GPT-4o-mini para analizar el contexto 
emocional de mi descripción..."

[Resultados aparecen]

"¡Y aquí están las recomendaciones! El AI interpretó mi mood como 
'Triste y Melancólico' con energía baja, y sugirió géneros como 
balada, indie y música acústica."

[Scroll por las canciones brevemente]

"Puedo escuchar previews de 30 segundos directamente en la app..."

[Click en play de UNA canción - dejar sonar 5 segundos]
[Pausar la canción]
```

---

### **DEMO 2: Query en Inglés + Features (1:00 - 1:50) - 50 segundos**
```
[Click en "Nueva Búsqueda" en la parte superior]

🎤 Narración:
"Ahora pruebo en inglés. Quiero música para entrenar en el gimnasio."

[Escribir]: "working out at the gym, need energy"

[Click en Descubrir Música]
[Esperar resultados]

"Perfecto, ahora el AI detectó un mood energético, sugiriendo géneros 
como EDM, Hip-Hop y Electrónica."

[Mostrar las canciones brevemente]

"La aplicación es completamente bilingüe..."

[Click en icono de idioma en el header - cambiar a español]
[Mostrar cómo la interfaz cambia a español]

"...y también tiene modo oscuro y claro."

[Click en icono de sol/luna - toggle theme]
[Mostrar el cambio visual]

[Volver a modo oscuro para mejor contraste]
```

---

### **TECNOLOGÍA (1:50 - 2:20) - 30 segundos**
```
[Opción A: Mostrar código brevemente]
[Abrir VSCode con llm_service.py visible]

🎤 Narración:
"Por detrás, la arquitectura usa un backend en FastAPI con Python que 
se comunica con la API de OpenAI. El modelo GPT-4o-mini analiza el 
lenguaje natural del usuario y extrae mood tags, nivel de energía y 
géneros musicales en formato JSON estructurado."

[Mostrar el código de analyze_mood por 5 segundos]

"Luego, esos datos se envían a la API de Deezer para buscar canciones 
reales, y el frontend en Next.js con TypeScript renderiza los resultados 
de forma interactiva."

[Volver al navegador con los resultados visible]

---

[Opción B: Mostrar diagrama]
[Si tienes ARQUITECTURA.md abierto, mostrar el diagrama ASCII]

🎤 Narración:
"La arquitectura es sencilla pero efectiva: el usuario interactúa con 
un frontend en Next.js, que envía queries a un backend FastAPI. Este 
llama a OpenAI para análisis de mood y a Deezer para obtener música 
real con previews de 30 segundos."
```

---

### **CIERRE (2:20 - 2:30) - 10 segundos**
```
[Pantalla: Homepage de MoodTune o resultados]

🎤 Narración:
"Todo el código está disponible en GitHub con documentación completa. 
Gracias por ver la demo de MoodTune."

[Fade out o corte]
```

---

## 🎬 Tips de Grabación

### **Audio**
- ✅ Graba en un lugar **silencioso** (sin ruido de fondo)
- ✅ Habla **claro y a velocidad normal** (no apresures)
- ✅ Sonríe al hablar (se nota en la voz, más energía)
- ⚠️ Evita muletillas ("ehhh", "umm")

### **Video**
- ✅ **Resolución mínima**: 1080p (1920x1080)
- ✅ **Frame rate**: 30 FPS o superior
- ✅ No grabes en fullscreen (ventana de navegador mediana se ve mejor)
- ✅ Cursor visible y movimientos lentos (no saltes por la pantalla)

### **Timing**
- ⚠️ No te apresures en las transiciones (deja 1-2 segundos entre acciones)
- ⚠️ Si cometes un error, **pausa grabación y reinicia esa sección** (edita después)
- ✅ Practica el script 2-3 veces antes de grabar final

### **Edición (Opcional)**
- **Necesario**: Cortar intro/outro si usas Loom
- **Opcional**: Agregar texto overlay con tu nombre y proyecto
- **Herramientas gratis**:
  - Mac: iMovie
  - Windows: Microsoft Clipchamp
  - Multiplataforma: CapCut (web)

---

## 📤 Publicación del Video

### **Opción 1: YouTube (Recomendado)**
```
1. Subir a YouTube (cuenta personal)
2. Configurar como "No listado" si no quieres que sea público
3. Título: "MoodTune - AI Music Discovery | Bootcamp IA Project"
4. Descripción corta: Ver abajo
5. Copiar link y poner en README
```

**Descripción sugerida para YouTube**:
```
MoodTune - AI-Powered Music Discovery Assistant

Demo del proyecto final del Bootcamp de Inteligencia Artificial.

Tecnologías:
- Frontend: Next.js 14 + TypeScript
- Backend: FastAPI + Python
- AI: OpenAI GPT-4o-mini (LLM)
- Music API: Deezer

Repository: [tu-github-link-aquí]

Autor: Umit Gungor
Fecha: Febrero 2026
```

### **Opción 2: Loom**
```
1. Grabar directamente con Loom (extensión de Chrome)
2. Auto-sube a Loom cloud
3. Copiar link shareable
4. Poner en README
```

### **Opción 3: Google Drive**
```
1. Subir archivo .mp4
2. Click derecho → "Obtener enlace" → "Cualquiera con el enlace"
3. Copiar link
4. Poner en README
```

---

## ✅ Update del README después de grabar

```markdown
## 🎥 Demo

🎬 **Watch MoodTune in action**: [Video Demo (3 min)](https://youtube.com/...)

**What you'll see**:
- Natural language mood input (e.g., "sad and melancholic after a breakup")
- AI analyzing the emotional context in real-time
- Personalized music recommendations
- 30-second audio previews
- Bilingual support (Spanish ↔ English)
- Dark/Light theme toggle
```

---

## 🚨 Troubleshooting

### **Problema: Backend no responde**
```bash
# Verificar que está corriendo:
curl http://localhost:8000/api/health

# Si no responde, reiniciar:
cd backend
source venv/bin/activate  # Mac/Linux
python main.py
```

### **Problema: Frontend da error de CORS**
```bash
# Verificar NEXT_PUBLIC_API_URL en .env.local:
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > frontend/.env.local

# Reiniciar frontend:
cd frontend
npm run dev
```

### **Problema: OpenAI API key inválida**
```bash
# Verificar .env en backend:
cd backend
cat .env  # Debe tener OPENAI_API_KEY=sk-proj-...

# Si falta, recrear:
echo "OPENAI_API_KEY=tu-key-aqui" > .env
```

### **Problema: Previews de audio no suenan**
- ✅ Verificar que tu navegador permite autoplay (Chrome puede bloquearlo)
- ✅ Verificar volumen del sistema
- ✅ Algunos tracks de Deezer no tienen preview → probar con otra canción

---

## 📊 Checklist Post-Grabación

- [ ] Video grabado (2-3 minutos)
- [ ] Audio claro y sin ruidos
- [ ] Se ven todas las features principales
- [ ] Video subido a YouTube/Loom/Drive
- [ ] Link agregado a README.md
- [ ] Link agregado a BRIEFING.md (si corresponde)
- [ ] Video testeado (reproducible por otros)

---

**¡Éxito con la grabación! 🎬🎵**

Si tienes problemas, recuerda:
- No necesita ser perfecto, solo funcional y claro
- 2-3 minutos es suficiente (no te extiendas)
- Muestra el valor del proyecto, no cada línea de código
