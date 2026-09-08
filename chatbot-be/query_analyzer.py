import re
from typing import Dict, Any

# Common greetings, chitchat, and conversational pleasantries that NEVER need web search
GREETINGS_AND_CHITCHAT = [
    "halo", "halo!", "hai", "haii", "hei", "helo", "hello", "hi", "hey",
    "apa kabar", "gimana kabarnya", "bagaimana kabarmu", "how are you",
    "kamu siapa", "siapa kamu", "siapa namamu", "namamu siapa", "what is your name", "who are you",
    "kamu model apa", "kamu ai apa", "kamu bisa apa", "bisa bantu apa", "apa yang bisa kamu lakukan",
    "terima kasih", "makasih", "makasi", "thanks", "thank you", "thx",
    "selamat pagi", "selamat siang", "selamat sore", "selamat malam", "good morning", "good evening",
    "tes", "test", "testing", "ok", "oke", "okay", "sip", "mantap", "keren",
    "bye", "dadah", "sampai jumpa", "see you", "goodbye"
]

# Patterns asking about the bot itself or its capabilities
BOT_IDENTITY_PATTERNS = [
    r"\b(kamu|dirimu|anda|nox|bot|ai)\s+(siapa|bisa apa|dibuat|dari mana|versi berapa)\b",
    r"\bwho\s+(are\s+you|made\s+you)\b",
    r"\btell\s+me\s+about\s+(yourself|you)\b",
    r"\bceritakan\s+tentang\s+(dirimu|kamu)\b"
]

# Informational multi-word triggers that genuinely require up-to-date internet search
AUTHENTIC_WEB_PATTERNS = [
    # News and current affairs (e.g. berita AI terbaru, kabar terbaru, berita hari ini)
    r"\b(berita|kabar|peristiwa|kejadian|news|headlines|updates)\b.{0,30}\b(terbaru|hari ini|terkini|sekarang|saat ini|today|latest|current)\b",
    # Live prices, rates, stocks, currency
    r"\b(harga|kurs|nilai tukar|saham|price of|stock of)\b.{0,30}\b(hari ini|sekarang|terbaru|saat ini|today|now|latest|current)\b",
    r"\b(harga|kurs|nilai)\s+(emas|bitcoin|btc|eth|crypto|kripto|dolar|usd|rupiah|bbri|bbca)\b",
    # Weather
    r"\b(cuaca|prakiraan cuaca|weather|temperature)\b.{0,30}\b(hari ini|besok|sekarang|today|now)\b",
    # Specific current public figures / status
    r"\b(siapa|who is)\s+(presiden|menteri|gubernur|ceo|pemimpin|juara|pemenang)\b.{0,30}\b(sekarang|saat ini|terbaru|current|now|202[4-9])\b",
    # Release notes, latest versions, changelog of software/frameworks
    r"\b(versi|rilis|update|release|changelog|fitur baru)\s+(terbaru|latest|terkini)\b",
    r"\b(dokumentasi|documentation)\s+(terbaru|latest)\b",
    # Explicit search commands
    r"\b(cari di (web|internet|google)|search (the web|online|internet)|browsing)\b"
]

# General concepts, coding, and theory that should always use internal model knowledge
INTERNAL_KNOWLEDGE_PATTERNS = [
    r"\b(apa itu|jelaskan|bagaimana cara|cara kerja|konsep|teori|definisi)\b",
    r"\b(what is|explain|how does|how to|concept of|difference between|difference of)\b",
    r"\b(tulis|buatkan|bikin|contoh|implementasi|coding|kode|code|function|fungsi|class|algoritma|debug|error|fix)\b"
]

def extract_search_query(user_input: str) -> str:
    """Clean and optimize user input for a concise search query."""
    cleaned = user_input.strip()
    filler_patterns = [
        r"^(tolong|coba|bisakah|bisa|tolong carikan|carikan|cari)\s+",
        r"^(please|can you|search for|find me|look up)\s+",
        r"^(apa|siapa|apakah|bagaimana)\s+"
    ]
    for pattern in filler_patterns:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE).strip()
    
    return cleaned if len(cleaned) > 3 else user_input.strip()

def needs_web_search(user_input: str) -> Dict[str, Any]:
    """
    Determine strictly whether user query requires live web retrieval.
    Prioritizes model internal knowledge and conversational chitchat first.
    Only triggers web search if real-time or external live data is needed.
    """
    text = (user_input or "").strip()
    if not text:
        return {
            "need_web": False,
            "confidence": 1.0,
            "reason": "Empty input",
            "search_query": ""
        }

    text_lower = text.lower()
    # Normalize punctuation for comparison
    normalized = re.sub(r"[^\w\s]", "", text_lower).strip()

    # 1. Immediate filter: Greetings and Chitchat (Basa-basi)
    if normalized in GREETINGS_AND_CHITCHAT or any(normalized.startswith(g) for g in ["terima kasih", "makasih", "thanks", "thank you", "selamat pagi", "selamat siang", "selamat malam"]):
        return {
            "need_web": False,
            "confidence": 0.99,
            "reason": "Conversational greeting or chitchat",
            "search_query": ""
        }

    # If sentence starts with greeting and is short (< 6 words)
    words = normalized.split()
    if len(words) <= 5 and any(words[0] == g for g in ["halo", "hai", "hello", "hi", "hey"]):
        return {
            "need_web": False,
            "confidence": 0.98,
            "reason": "Short conversational opening",
            "search_query": ""
        }

    # 2. Immediate filter: Bot identity or capabilities inquiry
    for pattern in BOT_IDENTITY_PATTERNS:
        if re.search(pattern, text_lower):
            return {
                "need_web": False,
                "confidence": 0.98,
                "reason": "Question about AI identity or capabilities",
                "search_query": ""
            }

    # 3. Authentic Web Search triggers (Live news, prices, weather, current status, explicit search)
    for pattern in AUTHENTIC_WEB_PATTERNS:
        if re.search(pattern, text_lower):
            return {
                "need_web": True,
                "confidence": 0.95,
                "reason": "Matched real-time information request",
                "search_query": extract_search_query(text)
            }

    # 4. Standard internal knowledge / coding questions
    for pattern in INTERNAL_KNOWLEDGE_PATTERNS:
        if re.search(pattern, text_lower):
            # Unless it explicitly asks for "terbaru / hari ini / 2026"
            if not any(fresh in text_lower for fresh in ["hari ini", "terbaru", "terkini", "saat ini", "today", "latest", "current"]):
                return {
                    "need_web": False,
                    "confidence": 0.95,
                    "reason": "Concept or programming question handled by internal knowledge",
                    "search_query": ""
                }

    # 5. Default fallback: Answer using model internal knowledge
    return {
        "need_web": False,
        "confidence": 0.85,
        "reason": "Default to internal knowledge base",
        "search_query": extract_search_query(text)
    }
