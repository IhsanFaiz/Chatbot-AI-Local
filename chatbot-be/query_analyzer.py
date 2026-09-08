import re
from typing import Dict, Any

# Keywords that strongly indicate a need for up-to-date or real-time internet data
STRONG_WEB_KEYWORDS = [
    # Indonesian
    "berita", "terbaru", "hari ini", "sekarang", "saat ini", "harga", "kurs",
    "cuaca", "presiden indonesia saat ini", "siapa presiden", "rilis terbaru",
    "versi terbaru", "update terbaru", "jadwal", "skor", "pertandingan", "gempa",
    "informasi terkini", "tren sekarang", "dokumen terbaru", "dokumentasi terbaru",
    # English
    "news", "latest", "today", "right now", "current", "currently", "price",
    "stock", "weather", "release notes", "changelog", "latest version", "recent update",
    "current president", "who is the current", "trending now", "latest documentation"
]

# Keywords that indicate general explanations, fundamentals, or coding logic that do NOT need web search
OFFLINE_CODE_KEYWORDS = [
    "apa itu", "jelaskan", "bagaimana cara", "cara membuat", "contoh kode",
    "tulis fungsi", "buatkan fungsi", "algoritma", "perbaiki kode", "struktur data",
    "what is", "explain", "how to", "how do i", "implement", "write a function",
    "code example", "refactor", "difference between", "beda antara"
]

# Regular expressions for years like 2024, 2025, 2026 or date references
TEMPORAL_REGEX = re.compile(r"\b(202[4-9]|203[0-9]|januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember|january|february|march|april|may|june|july|august|september|october|november|december)\b", re.IGNORECASE)

def extract_search_query(user_input: str) -> str:
    """
    Clean and optimize user input to create a concise search query.
    Removes conversational filler words.
    """
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
    Determine whether user query requires web search using keyword matching,
    temporal detection, and rule-based heuristics.
    
    Returns:
        {
            "need_web": bool,
            "confidence": float,
            "reason": str,
            "search_query": str
        }
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
    
    # 1. Count strong web indicators
    matched_web_keywords = [kw for kw in STRONG_WEB_KEYWORDS if kw in text_lower]
    temporal_match = bool(TEMPORAL_REGEX.search(text_lower))
    
    # 2. Count offline/conceptual indicators
    matched_offline_keywords = [kw for kw in OFFLINE_CODE_KEYWORDS if kw in text_lower]

    search_query = extract_search_query(text)

    # RULE 1: Explicit web search request by user
    if any(trigger in text_lower for trigger in ["cari di web", "cari di internet", "search the web", "search online", "browsing"]):
        return {
            "need_web": True,
            "confidence": 0.99,
            "reason": "Explicit search command requested by user",
            "search_query": search_query
        }

    # RULE 2: If strong web keywords or temporal indicators are found
    if matched_web_keywords:
        confidence = 0.95 if len(matched_web_keywords) > 1 or temporal_match else 0.88
        return {
            "need_web": True,
            "confidence": confidence,
            "reason": f"Detected web indicators: {', '.join(matched_web_keywords[:3])}",
            "search_query": search_query
        }

    if temporal_match and not matched_offline_keywords:
        return {
            "need_web": True,
            "confidence": 0.85,
            "reason": "Detected temporal year/date reference",
            "search_query": search_query
        }

    # RULE 3: Pure conceptual / algorithmic questions without freshness requirements
    if matched_offline_keywords:
        return {
            "need_web": False,
            "confidence": 0.90,
            "reason": "Conceptual/code explanation query without temporal urgency",
            "search_query": search_query
        }

    # Default fallback: general local conversation
    return {
        "need_web": False,
        "confidence": 0.80,
        "reason": "Default internal knowledge response",
        "search_query": search_query
    }
