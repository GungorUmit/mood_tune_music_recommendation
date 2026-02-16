# 🎵 MoodTune

> Describe your moment, discover your music

MoodTune is an AI-powered music discovery web app that translates natural language descriptions of moods, activities, and contexts into personalized song recommendations using LLM + Deezer API.

## 🚀 Project Status

🚧 **In Development** - Building MVP

## ✨ Features (Planned)

- 🤖 **AI-Powered Understanding**: Uses OpenAI GPT-4o-mini to interpret complex mood descriptions
- 🎼 **Smart Music Search**: Translates emotions into optimized Deezer queries
- 🌍 **Bilingual Support**: Full support for Spanish and English
- 🌓 **Theme Toggle**: Beautiful dark/light mode with glassmorphism design
- ⚡ **Fast & Secure**: Rate-limited API with input validation and CORS protection

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

- [Technical Architecture](./docs/architecture.md) - Coming soon
- [Development Plan](./docs/development.md) - Coming soon
- [API Documentation](http://localhost:8000/docs) - Available when backend is running

## 👤 Author

**Umit Gungor**
- Bootcamp Final Project - AI Music Discovery

## 📄 License

MIT License - Educational purposes
