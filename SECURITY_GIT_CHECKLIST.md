# 🔒 CHECKLIST DE SEGURIDAD GIT - MoodTune

> **Fecha de auditoría**: 19 de febrero de 2026  
> **Status**: ✅ APROBADO - Sin vulnerabilidades críticas detectadas

---

## ✅ VERIFICACIONES COMPLETADAS

### **🔐 1. Secretos y API Keys**

- [x] ✅ `.env` NO está en git (verificado con `git ls-files`)
- [x] ✅ `frontend/.env.local` NO está en git
- [x] ✅ API keys NO hardcodeadas en código Python (grep búsqueda negativa)
- [x] ✅ `.env.example` SÍ está (OK para subir sin secretos)
- [x] ✅ `.env` incluido en `.gitignore`

**Archivos secretos protegidos**:
```
✅ backend/.env                    # OpenAI API Key, HuggingFace Token
✅ frontend/.env.local             # Next.js API URL
```

**Archivos públicos (OK)**:
```
✅ backend/.env.example            # Template sin valores reales
✅ frontend/.env.local.example     # Template sin valores reales
```

---

### **🗑️ 2. Cache y Archivos Temporales**

- [x] ✅ `__pycache__/` NO está en git
- [x] ✅ `.next/` NO está en git (40+ archivos >1MB detectados)
- [x] ✅ `node_modules/` NO está en git
- [x] ✅ `venv/` NO está en git
- [x] ✅ `.DS_Store` NO está en git (múltiples encontrados en disco, pero ignorados)

**Archivos temporales encontrados (ignorados correctamente)**:
```
⚠️ test_deezer_complete.py.save   # Ahora en .gitignore (*.save)
⚠️ .DS_Store (varios)              # Ahora en .gitignore
```

---

### **📦 3. Archivos Grandes**

**Análisis de tamaño**:
```bash
backend/datasets/       12 KB   ✅ OK para subir (cache de mood queries)
.next/dev/cache/        >200MB  ✅ Ignorado (cache Next.js)
node_modules/           ~500MB  ✅ Ignorado (dependencias npm)
venv/                   ~150MB  ✅ Ignorado (virtualenv Python)
```

**Decisión**: 
- ✅ `datasets/mood_cache.json` (12KB) puede subirse (cache útil para dev)
- ⚠️ Si crece >1MB, descomentar línea en `.gitignore`:
  ```gitignore
  # backend/datasets/mood_cache.json
  ```

---

### **🛡️ 4. .gitignore Optimizado**

**Cambios aplicados**:
- ✅ Añadido `*.save` (archivos de editor)
- ✅ Añadido `*.bak` (backups)
- ✅ Añadido `*.tmp` (temporales)
- ✅ Removido entradas innecesarias:
  - ❌ `.huggingface/` (no usas HF local)
  - ❌ `models/` (no entrenas modelos)
  - ❌ `checkpoints/` (no usas)
  - ❌ `data/` (no tienes carpeta data/)
  - ❌ `.streamlit/` (no usas Streamlit)
- ✅ Añadida sección de documentación con headers claros

**Versión actual**: Ver [.gitignore](./.gitignore)

---

## 🚨 COMANDOS DE LIMPIEZA (Si fuera necesario)

### **Si encontraras .env en git** (NO es tu caso)

```bash
# ⚠️ SOLO SI .env ESTUVIERA EN GIT (actualmente NO lo está)
# NO ejecutar estos comandos sin verificar primero

# Verificar si .env está en git:
git ls-files | grep "\.env$"

# Si devuelve algo (NO en tu caso):
git rm --cached backend/.env
git rm --cached frontend/.env.local
git commit -m "security: remove .env files from git history"

# IMPORTANTE: Cambiar todas las API keys expuestas
# 1. Ir a https://platform.openai.com/api-keys
# 2. Revocar key antigua
# 3. Crear nueva key
# 4. Actualizar backend/.env con nueva key
```

### **Limpiar archivos grandes accidentalmente commiteados**

```bash
# Verificar archivos >1MB en git:
git rev-list --objects --all | 
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' |
  awk '$3 > 1048576 {print $3/1048576 " MB", $4}' |
  sort -n

# Si encuentras algo grande (ejemplo: model.bin):
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/large/file.bin' \
  --prune-empty --tag-name-filter cat -- --all

git push origin --force --all
```

### **Limpiar .DS_Store de todo el historial** (opcional, cosmético)

```bash
# Solo si quieres historial 100% limpio antes de hacer público:
find . -name .DS_Store -print0 | xargs -0 git rm -f --ignore-unmatch
git commit -m "chore: remove .DS_Store files"

# Limpiar de historial completo:
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch **/.DS_Store' \
  --prune-empty --tag-name-filter cat -- --all
```

---

## ✅ CHECKLIST ANTES DE PUSH A GITHUB

### **Pre-Push Security Check**

```bash
# 1. Verificar que .env NO está staged
git status | grep ".env"
# Expected: No output o solo "Untracked files" (nunca "Changes to be committed")

# 2. Verificar que no hay API keys en código
grep -r "sk-proj-\|sk-\|hf_" backend/*.py frontend/**/*.ts
# Expected: No matches

# 3. Verificar tamaño del repo
du -sh .git
# Expected: <50MB (idealmente <10MB sin node_modules/venv)

# 4. Ver qué se va a subir
git status
git diff --cached --stat

# 5. Commit y push
git add .
git commit -m "docs: add project documentation and security improvements"
git push origin main
```

### **Post-Push Verification**

```bash
# 1. Clonar en carpeta temporal (simular descarga de GitHub)
cd /tmp
git clone https://github.com/tu-usuario/moodtune.git test-moodtune
cd test-moodtune

# 2. Verificar que secretos NO están
ls -la backend/.env        # Should NOT exist
ls -la frontend/.env.local # Should NOT exist

# 3. Verificar que ejemplos SÍ están
ls -la backend/.env.example        # Should exist ✅
ls -la frontend/.env.local.example # Should exist ✅

# 4. Cleanup
cd ..
rm -rf test-moodtune
```

---

## 📋 CHECKLIST RÁPIDO (5 MIN)

Antes de hacer público tu repo, verifica:

- [ ] ✅ `.env` NO está en git (`git ls-files | grep ".env$"` → vacío)
- [ ] ✅ API keys NO en código (`grep -r "sk-" backend/`)
- [ ] ✅ `.gitignore` actualizado (versión feb 2026)
- [ ] ✅ README sin tokens/secrets
- [ ] ✅ Repo <50MB sin dependencias
- [ ] ⚠️ Si usas GitHub Actions: secrets en Settings → Secrets
- [ ] ⚠️ Si deployeas: usar variables de entorno del hosting (Render/Vercel)

---

## 🔥 RED FLAGS A EVITAR

### **Errores comunes que exponen secretos**

❌ **NUNCA HACER ESTO**:
```python
# ❌ MAL: Hardcodear API key
openai.api_key = "sk-proj-abc123xyz..."

# ✅ BIEN: Usar variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")
```

❌ **NUNCA HACER ESTO**:
```bash
# ❌ MAL: Commit de .env
git add backend/.env
git commit -m "add env file"

# ✅ BIEN: Solo .env.example
git add backend/.env.example
```

❌ **NUNCA HACER ESTO**:
```markdown
# ❌ MAL: Token en README
OPENAI_API_KEY=sk-proj-abc123...
```

---

## 🎓 BUENAS PRÁCTICAS RECOMENDADAS

### **1. Dos archivos para configuración**

```bash
backend/
  ├── .env              # ❌ NO SUBIR (gitignore)
  │   OPENAI_API_KEY=sk-proj-real-key
  │
  └── .env.example      # ✅ SUBIR (template)
      OPENAI_API_KEY=sk-proj-your-key-here
```

### **2. Verificar antes de commit**

```bash
# Pre-commit hook (opcional, avanzado)
# Crear: .git/hooks/pre-commit

#!/bin/bash
if git diff --cached --name-only | grep -E "\.env$"; then
  echo "❌ ERROR: Trying to commit .env file!"
  exit 1
fi
```

### **3. Usar .gitignore global (macOS)**

```bash
# En tu home directory
cat > ~/.gitignore_global << EOF
.DS_Store
*.swp
*.swo
*~
EOF

git config --global core.excludesfile ~/.gitignore_global
```

---

## 📊 RESUMEN DE AUDITORÍA

| Categoría | Status | Detalles |
|-----------|--------|----------|
| **Secretos** | ✅ SEGURO | .env protegido, no en git |
| **Cache** | ✅ SEGURO | __pycache__, .next/ ignorados |
| **Archivos grandes** | ✅ SEGURO | Solo datasets/ (12KB) en git |
| **.gitignore** | ✅ OPTIMIZADO | Actualizado feb 2026 |
| **API Keys** | ✅ SEGURO | No hardcodeadas en código |
| **Historial** | ✅ LIMPIO | No hay .env en commits previos |

**Puntuación de seguridad: 10/10** ✅

---

## 🚀 PRÓXIMOS PASOS

1. **Ahora** (5 min):
   ```bash
   cd /Users/umitgungor/Downloads/asistente-musical
   git add .gitignore
   git commit -m "security: optimize .gitignore for MoodTune"
   ```

2. **Antes de push a GitHub** (2 min):
   ```bash
   # Verificación final
   git ls-files | grep -E "(\.env$|\.DS_Store)"
   # Should be empty
   
   # Push
   git push origin main
   ```

3. **Después de push** (3 min):
   - Verificar en GitHub UI que `.env` NO aparece
   - Verificar que `.env.example` SÍ aparece
   - Verificar tamaño del repo en GitHub

---

## 🆘 RECURSOS DE AYUDA

- **GitHub Secret Scanning**: https://docs.github.com/en/code-security/secret-scanning
- **Git Filter-Branch Docs**: https://git-scm.com/docs/git-filter-branch
- **BFG Repo-Cleaner** (limpiar historial): https://rtyley.github.io/bfg-repo-cleaner/

---

**✅ Tu repositorio está LISTO para hacerse público de forma segura.**

**Último check antes de push**: `git ls-files | grep "\.env$"` → debe estar vacío ✅

---

**Auditoría realizada por**: GitHub Copilot (Revisor Senior Git)  
**Fecha**: 19 de febrero de 2026  
**Proyecto**: MoodTune - AI Music Discovery
