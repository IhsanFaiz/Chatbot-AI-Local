import time
import requests
from typing import List, Dict, Any

try:
    from ddgs import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    try:
        from duckduckgo_search import DDGS
        DDGS_AVAILABLE = True
    except ImportError:
        DDGS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

from cache_manager import get_cached_search, save_cached_search
from config import SEARCH_CACHE_TTL_HOURS

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def _fallback_ddg_html(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Secondary fallback search using direct DuckDuckGo HTML endpoint."""
    results = []
    if not BS4_AVAILABLE:
        return results

    try:
        url = "https://html.duckduckgo.com/html/"
        resp = requests.post(url, data={"q": query}, headers=DEFAULT_HEADERS, timeout=5.0)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            result_divs = soup.find_all("div", class_="result")
            for div in result_divs:
                title_elem = div.find("a", class_="result__a")
                snippet_elem = div.find("a", class_="result__snippet")
                if title_elem and title_elem.get("href"):
                    raw_href = title_elem["href"]
                    # Clean up DuckDuckGo redirect url if present
                    if "uddg=" in raw_href:
                        import urllib.parse
                        parsed = urllib.parse.parse_qs(urllib.parse.urlparse(raw_href).query)
                        final_url = parsed.get("uddg", [raw_href])[0]
                    else:
                        final_url = raw_href

                    title = title_elem.get_text(strip=True)
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""

                    if title and final_url:
                        results.append({
                            "title": title,
                            "url": final_url,
                            "snippet": snippet,
                            "content": snippet
                        })
                        if len(results) >= max_results:
                            break
    except Exception as e:
        print(f"[WebSearch] Fallback HTML search error: {e}")

    return results

def search_web(query: str, max_results: int = 5, use_cache: bool = True) -> List[Dict[str, Any]]:
    """
    Search the web using DDGS with automatic HTML fallback and caching.
    Returns up to max_results formatted dictionaries:
    [
        {
            "title": str,
            "url": str,
            "snippet": str,
            "content": str
        }
    ]
    """
    cleaned_query = (query or "").strip()
    if not cleaned_query:
        return []

    # 1. Check cache first
    if use_cache:
        cached = get_cached_search(cleaned_query, ttl_hours=SEARCH_CACHE_TTL_HOURS)
        if cached:
            return cached

    results: List[Dict[str, Any]] = []

    # 2. Try primary DDGS
    if DDGS_AVAILABLE:
        try:
            with DDGS() as ddgs:
                raw_results = list(ddgs.text(cleaned_query, max_results=max_results))

            for item in raw_results:
                title = item.get("title", "").strip()
                url = item.get("href", item.get("link", "")).strip()
                snippet = item.get("body", item.get("snippet", "")).strip()

                if url and title:
                    results.append({
                        "title": title,
                        "url": url,
                        "snippet": snippet,
                        "content": snippet
                    })
        except Exception as e:
            print(f"[WebSearch] DDGS primary failed ({e}), falling back to direct HTML.")

    # 3. If primary returned 0 results or failed, execute fallback
    if not results:
        results = _fallback_ddg_html(cleaned_query, max_results=max_results)

    # 4. Save to cache if we got results
    if results and use_cache:
        save_cached_search(cleaned_query, results)

    return results
