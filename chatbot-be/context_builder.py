from typing import List, Dict, Any

def sanitize_text(text: str) -> str:
    """Neutralize ChatML special tokens if present in scraped text."""
    if not text:
        return ""
    return (
        text.replace("<|im_start|>", "[im_start]")
            .replace("<|im_end|>", "[im_end]")
            .replace("<|endoftext|>", "[endoftext]")
    )

def build_context(results: List[Dict[str, Any]], max_sources: int = 5, max_chars: int = 6500) -> str:
    """
    Format web search & scraped results into a structured prompt context for the LLM.
    
    Format:
    [SOURCE 1]
    Title: <title>
    URL: <url>
    Content: <content>

    [SOURCE 2]
    ...
    """
    if not results:
        return ""

    context_blocks = []
    total_length = 0

    valid_sources = [r for r in results if r.get("title") and (r.get("content") or r.get("snippet"))]
    selected_sources = valid_sources[:max_sources]

    for idx, item in enumerate(selected_sources, 1):
        title = sanitize_text(item.get("title", "Untitled").strip())
        url = item.get("url", "").strip()
        # Prefer full scraped content over snippet
        raw_content = (item.get("content") or item.get("snippet") or "").strip()
        content = sanitize_text(raw_content)

        if not content:
            continue

        # Per source character limit (~1200 chars)
        content_snippet = content[:1200].strip()

        block = (
            f"[SOURCE {idx}]\n"
            f"Title: {title}\n"
            f"URL: {url}\n"
            f"Content:\n{content_snippet}\n"
        )

        if total_length + len(block) > max_chars:
            remaining_chars = max_chars - total_length
            if remaining_chars > 200:
                truncated_block = block[:remaining_chars].rsplit(" ", 1)[0] + "..."
                context_blocks.append(truncated_block)
            break

        context_blocks.append(block)
        total_length += len(block)

    if not context_blocks:
        return ""

    header = "=== WEB RETRIEVAL CONTEXT (FACTUAL REFERENCES) ===\n\n"
    footer = "\n=== END OF WEB RETRIEVAL CONTEXT ===\n"
    return header + "\n".join(context_blocks) + footer

def get_source_citations(results: List[Dict[str, Any]], max_sources: int = 5) -> List[Dict[str, str]]:
    """
    Return clean list of title and URL pairs for user-facing citations.
    """
    citations = []
    for item in results[:max_sources]:
        title = sanitize_text(item.get("title", "").strip())
        url = item.get("url", "").strip()
        if title and url:
            citations.append({
                "title": title,
                "url": url
            })
    return citations
