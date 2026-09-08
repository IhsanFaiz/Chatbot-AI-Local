import re
import requests
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import trafilatura
    TRAFILATURA_AVAILABLE = True
except ImportError:
    TRAFILATURA_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
}

def clean_text(text: str) -> str:
    """Normalize whitespace and remove excessive blank lines."""
    if not text:
        return ""
    # Replace multiple newlines with at most 2
    cleaned = re.sub(r"\n\s*\n", "\n\n", text)
    # Replace multiple spaces/tabs with single space
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    return cleaned.strip()

def extract_content(url: str, timeout: float = 4.0, max_chars: int = 1800) -> Dict[str, Any]:
    """
    Extract clean article content and title from a webpage URL.
    Uses trafilatura as primary extractor, with BeautifulSoup as fallback.
    Returns:
        {
            "title": str,
            "url": str,
            "content": str
        }
    """
    result = {
        "title": "",
        "url": url,
        "content": ""
    }

    if not url:
        return result

    html_content = ""
    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout, allow_redirects=True)
        if response.status_code == 200:
            html_content = response.text
        else:
            return result
    except Exception as e:
        # Ignore network/timeout errors gracefully
        return result

    # 1. Primary extraction with trafilatura
    if TRAFILATURA_AVAILABLE and html_content:
        try:
            extracted = trafilatura.extract(
                html_content,
                include_comments=False,
                include_tables=True,
                no_fallback=False
            )
            if extracted and len(extracted.strip()) > 50:
                result["content"] = clean_text(extracted)[:max_chars]
        except Exception:
            pass

    # 2. Extract page title & fallback content with BeautifulSoup
    if BS4_AVAILABLE and html_content:
        try:
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract title if not set
            if not result["title"]:
                title_tag = soup.find("title")
                if title_tag and title_tag.string:
                    result["title"] = title_tag.string.strip()

            # If trafilatura failed or produced little text, extract using BS4
            if not result["content"] or len(result["content"]) < 80:
                # Remove unwanted tags
                for element in soup(["script", "style", "nav", "footer", "header", "aside", "form", "svg"]):
                    element.decompose()

                # Get body text or paragraph text
                paragraphs = [p.get_text().strip() for p in soup.find_all(["p", "h1", "h2", "h3", "li"])]
                text = " ".join([p for p in paragraphs if len(p) > 20])
                result["content"] = clean_text(text)[:max_chars]
        except Exception:
            pass

    return result

def scrape_multiple(items: List[Dict[str, Any]], max_workers: int = 3, timeout: float = 4.0) -> List[Dict[str, Any]]:
    """
    Scrape multiple search result URLs in parallel to reduce latency.
    Updates each item's 'content' in place with full scraped text.
    """
    if not items:
        return []

    enriched_items = [dict(item) for item in items]
    url_to_index = {item["url"]: idx for idx, item in enumerate(enriched_items) if item.get("url")}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(extract_content, url, timeout): url
            for url in url_to_index.keys()
        }

        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                idx = url_to_index.get(url)
                if idx is not None and data.get("content"):
                    enriched_items[idx]["content"] = data["content"]
                    if not enriched_items[idx].get("title") and data.get("title"):
                        enriched_items[idx]["title"] = data["title"]
            except Exception:
                pass

    return enriched_items
