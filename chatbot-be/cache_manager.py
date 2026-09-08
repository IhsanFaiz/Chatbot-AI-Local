import os
import json
import time
import sqlite3
import hashlib
from typing import Optional, List, Dict, Any

from config import PATHS

DB_PATH = os.path.join(PATHS.get('cache', os.path.dirname(__file__)), 'web_search_cache.db')

def _get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=5)
    conn.row_factory = sqlite3.Row
    return conn

def init_cache_db():
    """Create search cache table if not already created."""
    try:
        with _get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS search_cache (
                    query_hash TEXT PRIMARY KEY,
                    query TEXT NOT NULL,
                    results_json TEXT NOT NULL,
                    created_at REAL NOT NULL
                )
            """)
            conn.commit()
    except Exception as e:
        print(f"[CacheManager] DB init error: {e}")

# Initialize on module load
init_cache_db()

def _hash_query(query: str) -> str:
    return hashlib.sha256(query.strip().lower().encode('utf-8')).hexdigest()

def get_cached_search(query: str, ttl_hours: float = 12.0) -> Optional[List[Dict[str, Any]]]:
    """
    Retrieve cached search results if present and not expired.
    Returns None if cache missed or expired.
    """
    query_hash = _hash_query(query)
    now = time.time()
    max_age_seconds = ttl_hours * 3600

    try:
        with _get_connection() as conn:
            cursor = conn.execute(
                "SELECT results_json, created_at FROM search_cache WHERE query_hash = ?",
                (query_hash,)
            )
            row = cursor.fetchone()
            if row:
                created_at = row["created_at"]
                if (now - created_at) < max_age_seconds:
                    return json.loads(row["results_json"])
                else:
                    # Expired, clean up
                    conn.execute("DELETE FROM search_cache WHERE query_hash = ?", (query_hash,))
                    conn.commit()
    except Exception as e:
        print(f"[CacheManager] Read cache error: {e}")

    return None

def save_cached_search(query: str, results: List[Dict[str, Any]]):
    """Save search results to cache with current timestamp."""
    query_hash = _hash_query(query)
    now = time.time()

    try:
        results_json = json.dumps(results, ensure_ascii=False)
        with _get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO search_cache (query_hash, query, results_json, created_at)
                VALUES (?, ?, ?, ?)
            """, (query_hash, query.strip().lower(), results_json, now))
            conn.commit()
    except Exception as e:
        print(f"[CacheManager] Write cache error: {e}")

def clear_expired_cache(ttl_hours: float = 24.0):
    """Prune entries older than ttl_hours."""
    cutoff = time.time() - (ttl_hours * 3600)
    try:
        with _get_connection() as conn:
            conn.execute("DELETE FROM search_cache WHERE created_at < ?", (cutoff,))
            conn.commit()
    except Exception as e:
        print(f"[CacheManager] Prune cache error: {e}")
