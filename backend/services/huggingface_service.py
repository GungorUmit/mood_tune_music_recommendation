import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import json
import re

load_dotenv()

async def analyze_with_huggingface(query: str, language: str = "en") -> dict:
    """
    Analiza el mood musical de una query usando Hugging Face.
    Detecta automáticamente el idioma y responde en ese idioma.
    Prioriza canciones actuales en search_query.
    
    Args:
        query: Texto del usuario describiendo su mood/contexto musical
        language: Idioma preferido (usado como fallback, pero se detecta auto)
    
    Returns:
        dict con mood_tags, energy, genres, search_query (o None si falla)
    """
    token = os.getenv("HUGGINGFACE_TOKEN")
    if not token:
        raise ValueError("HUGGINGFACE_TOKEN not found")
    
    try:
        client = InferenceClient(token=token)
        
        # System message: Prompt mejorado con detección de idioma y priorización de hits actuales
        system_msg = """You are an expert music mood analyzer. 

CRITICAL RULES:
1. DETECT the language: If query has Spanish words (triste, feliz, fiesta, etc.) → respond in Spanish. If English words (sad, happy, party, etc.) → respond in English
2. MANDATORY: mood_tags and genres MUST be in the SAME language as the query
3. PRIORITIZE current hits: ALWAYS include "2026" or "top" or "hits" in search_query
4. Return ONLY valid JSON, no extra text

RESPONSE FORMAT:
{
  "mood_tags": ["tag1", "tag2"],
  "energy": "low" or "medium" or "high",
  "genres": ["genre1", "genre2"],
  "search_query": "optimized query with 2026/top/hits"
}

EXAMPLES - Spanish queries:
Input: "estudiando por la noche"
{"mood_tags": ["concentrado", "tranquilo"], "energy": "low", "genres": ["lo-fi", "ambiental"], "search_query": "lofi estudio 2026"}

Input: "fiesta en la playa"
{"mood_tags": ["fiesta", "energético"], "energy": "high", "genres": ["reggaeton", "dance"], "search_query": "fiesta playa 2026 top"}

EXAMPLES - English queries:
Input: "studying late at night"
{"mood_tags": ["focused", "calm"], "energy": "low", "genres": ["lo-fi", "ambient"], "search_query": "lofi study 2026"}

Input: "working out at gym"
{"mood_tags": ["motivated", "intense"], "energy": "high", "genres": ["hip-hop", "electronic"], "search_query": "workout gym 2026 top"}"""

        # User message con instrucciones claras sobre idioma
        user_msg = f"""Analyze: "{query}"

IMPORTANT: 
- If the query is in Spanish → respond with Spanish mood_tags and genres
- If the query is in English → respond with English mood_tags and genres
- Always include "2026" or "top" in search_query

Return ONLY JSON, nothing else."""

        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ]
        
        # Chat completion con max_tokens aumentado para respuestas más completas
        response = client.chat_completion(
            messages=messages,
            model="mistralai/Mistral-7B-Instruct-v0.2",
            max_tokens=250,  # Aumentado de 200 a 250 para respuestas completas
            temperature=0.5
        )
        
        # Extract the response content
        content = response.choices[0].message.content
        
        print(f"📝 Hugging Face raw response: {content[:300]}...")
        
        # Clean response: Remove markdown code blocks
        cleaned = content.strip()
        cleaned = re.sub(r'^```json\s*', '', cleaned)
        cleaned = re.sub(r'^```\s*', '', cleaned)
        cleaned = re.sub(r'\s*```$', '', cleaned)
        cleaned = cleaned.strip()
        
        # Extract JSON object usando regex robusto
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', cleaned)
        if json_match:
            cleaned = json_match.group(0)
        
        # Parse JSON
        result = json.loads(cleaned)
        
        # Validate required fields
        required_fields = ["mood_tags", "energy", "genres", "search_query"]
        if all(field in result for field in required_fields):
            # Normalize energy value (low/medium/high)
            energy = str(result["energy"]).lower()
            if "low" in energy or "bajo" in energy:
                result["energy"] = "low"
            elif "high" in energy or "alto" in energy or "alta" in energy:
                result["energy"] = "high"
            else:
                result["energy"] = "medium"
            
            # Ensure search_query has current year/hits if not already included
            search_q = result.get("search_query", "")
            if "2026" not in search_q and "2025" not in search_q:
                # Add "2026" if year not present
                if any(word in query.lower() for word in ["spanish", "español", "triste", "feliz", "romántico"]):
                    result["search_query"] = f"{search_q} 2026".strip()
                else:
                    result["search_query"] = f"{search_q} 2026".strip()
            
            print(f"✅ Parsed successfully: {result}")
            return result
        else:
            missing = [f for f in required_fields if f not in result]
            print(f"❌ Missing required fields: {missing}")
            return None
            
    except Exception as e:
        print(f"❌ Error in Hugging Face analysis: {e}")
        return None
