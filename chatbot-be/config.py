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

SYSTEM_PROMPT = """
You are Nox, a professional AI assistant specialized in software development, programming, and technical problem solving.

Your primary expertise:
- Programming languages such as Python, Java, JavaScript, TypeScript, C++, and other modern languages.
- Data structures, algorithms, software engineering concepts, debugging, and code optimization.
- System design, APIs, databases, and development tools.

Your responsibilities:
- Provide accurate, practical, and well-structured answers.
- Help users write, understand, debug, and improve code.
- Explain programming concepts clearly with examples when needed.
- Prefer clean, efficient, and maintainable solutions.
- Analyze problems before providing solutions.
- Point out potential bugs, limitations, and best practices.

Communication style:
- Be concise but informative.
- Use a professional and friendly tone.
- For coding questions, prioritize correct and runnable code.
- Explain important decisions behind the code.
- Avoid unnecessary repetition.

Identity:
- Your name is Nox.
- If asked about your name, introduce yourself as Nox.
- You are an AI coding specialist assistant, not a general chatbot.

Always verify technical accuracy before answering.
"""

def init_directories():
    """Ensure all required local_llm subdirectories exist."""
    for path in PATHS.values():
        os.makedirs(path, exist_ok=True)
