# 🎵 MoodTune

> Describe your moment, discover your music

MoodTune is an AI-powered music discovery web app that translates natural language descriptions of moods, activities, and contexts into personalized song recommendations using LLM + Deezer API.

## 🚀 Project Status

✅ **MVP Completed** - Ready for local use and presentation.

## 🎥 Demo

> **Status**: 🚧 Video demo coming soon

🎬 **Watch MoodTune in action**: [Link to video demo - pending deployment]

**What you'll see**:
- Natural language mood input (e.g., "sad and melancholic after a breakup")
- AI analyzing the emotional context
- Personalized music recommendations
- 30-second audio previews
- Bilingual support (Spanish ↔ English)

## 🤖 AI Component Explained

### **Why is this an AI project?**

MoodTune uses **OpenAI GPT-4o-mini (Large Language Model)** to solve a problem traditional search cannot: **understanding emotional context**.

**Traditional search** (keyword matching):
- User: "sad music" → Returns only songs with word "sad" in title
- Limited to literal matches
- Ignores context, nuance, and synonyms

**MoodTune's AI approach** (semantic understanding):
- User: "feeling melancholic after a breakup, raining outside"
- AI extracts: `mood_tags: ["sad", "reflective", "calm"]`, `energy: "low"`, `genres: ["indie", "ballad", "acoustic"]`
- Translates emotions → musical characteristics
- Generates optimized search query: "sad indie ballad acoustic heartbreak"

**Technical Implementation**:
```python
# LLM analyzes natural language and returns structured data
{
  "mood_tags": ["sad", "melancholic", "reflective"],
  "energy": "low",
  "genres": ["indie", "ballad", "acoustic"],
  "search_query": "sad indie ballad acoustic reflective"
}
```

This is **transfer learning** in action: leveraging a pre-trained language model (GPT-4o-mini) for a specialized music discovery task.

## ✨ Features

- 🤖 **AI-Powered Understanding**: Uses OpenAI GPT-4o-mini to interpret complex mood descriptions (see AI explanation above).
- 🎼 **Real Music Discovery**: Integration with **Deezer Public API** (Search & Charts).
- 🎵 **Interactive Previews**: Listen to 30s song segments directly in the app.
- 🌍 **Bilingual Support**: Toggle between Spanish and English.
- 🌓 **Theme Toggle**: Beautiful dark/light mode with glassmorphism design.
- ⚡ **Resilient Backend**: Fallback to trending charts if search results are too specific.

## 🏗️ Tech Stack

**Frontend:**
- Next.js 14 (App Router)
- TypeScript
- CSS Modules

**Backend:**
- FastAPI (Python 3.11+)
- OpenAI GPT-4o-mini
- Deezer Simple API

**Deployment:**
- Frontend: Vercel
- Backend: Render

## 💻 Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- OpenAI API key

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
echo "OPENAI_API_KEY=your-key-here" > .env
python main.py
```

### Frontend Setup

```bash
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

## 📝 Documentation

- **[Briefing & Problem Definition](./BRIEFING.md)** - Project planning and MVP scope
- **[Technical Architecture](./ARQUITECTURA.md)** - System design, decisions, and learnings
- **[Project Status](./PROJECT_STATUS.md)** - Implementation checklist and features
- **[Security Guidelines](./SECURITY.md)** - Rate limiting, CORS, and deployment security
- **[API Documentation](http://localhost:8000/docs)** - Interactive Swagger docs (when backend is running)

## 👤 Author

**Umit Gungor**
- Bootcamp Final Project - AI Music Discovery

## 📄 License

MIT License - Educational purposes
