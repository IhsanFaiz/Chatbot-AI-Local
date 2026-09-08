import os
try:
    from dotenv import load_dotenv
    # Load .env file from chatbot-be directory or parent root directory
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
except ImportError:
    pass

# Base directory setup - defaults to 'local_llm' inside the chatbot-be folder
DEFAULT_BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'local_llm'))
BASE_DIR = os.getenv('LOCAL_LLM_DIR', DEFAULT_BASE_DIR)
PORT = int(os.getenv('PORT', '5001'))
HOST = os.getenv('HOST', '127.0.0.1')
USE_NGROK = os.getenv('USE_NGROK', 'false').lower() in ('true', '1', 't', 'yes')

PATHS = {
    'models': os.path.join(BASE_DIR, 'models'),
    'cache': os.path.join(BASE_DIR, 'cache'),
    'logs': os.path.join(BASE_DIR, 'logs'),
    'config': os.path.join(BASE_DIR, 'config'),
    'flags': os.path.join(BASE_DIR, 'flags'),
    'qwen_chat': os.path.join(BASE_DIR, 'models', 'qwen_chat'),
    'qwen_coder': os.path.join(BASE_DIR, 'models', 'qwen_coder'),
    'deepseek_coder': os.path.join(BASE_DIR, 'models', 'deepseek_coder')
}

FLAGS = {
    'environment_ready': os.path.join(PATHS['flags'], 'environment_ready.flag'),
    'model_download': os.path.join(PATHS['flags'], 'model_download.flag')
}

MODELS_CONFIG = {
    "qwen_chat": ("Qwen/Qwen2.5-3B-Instruct-GGUF", "qwen2.5-3b-instruct-q4_k_m.gguf"),
    "qwen_coder": ("Qwen/Qwen2.5-Coder-3B-Instruct-GGUF", "qwen2.5-coder-3b-instruct-q4_k_m.gguf"),
    "deepseek_coder": ("TheBloke/deepseek-coder-1.3B-instruct-GGUF", "deepseek-coder-1.3b-instruct.Q4_K_M.gguf")
}

HISTORY_FILE = os.path.join(PATHS['logs'], 'chat_history.json')

NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN", "36L2KHWDZihcXlhO1PRLNvhFWCL_2Bsmau67rspzj25xqcvUi")
WEB_SEARCH_ENABLED = os.getenv("WEB_SEARCH_ENABLED", "true").lower() in ("true", "1", "yes")
SEARCH_CACHE_TTL_HOURS = float(os.getenv("SEARCH_CACHE_TTL_HOURS", "12.0"))
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))

SYSTEM_PROMPT = """
You are Nox, a professional local AI assistant with web retrieval capability, specialized in software development, technical problem solving, and answering user inquiries.

Core capabilities & guidelines:
- When web information is provided:
  * Use the retrieved information as your factual reference.
  * Prioritize recent and up-to-date information.
  * Mention that the information comes from web sources when relevant.
- When no web information exists:
  * Answer accurately using your internal knowledge.
- If retrieved information is insufficient:
  * Clearly state limitations honestly without guessing.

Communication style:
- Provide accurate, practical, and well-structured answers.
- For coding questions, prioritize clean, runnable, and efficient code.
- Be concise, informative, and friendly. Avoid unnecessary repetition.
- Your name is Nox.
"""

def init_directories():
    """Ensure all required local_llm subdirectories exist."""
    for path in PATHS.values():
        os.makedirs(path, exist_ok=True)
