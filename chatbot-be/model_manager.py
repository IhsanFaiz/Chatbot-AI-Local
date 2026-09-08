import gc
import os
import json
import torch
import psutil
import threading

from config import PATHS, FLAGS, MODELS_CONFIG, SYSTEM_PROMPT, init_directories
from huggingface_hub import hf_hub_download

try:
    from llama_cpp import Llama
    LLAMA_INSTALLED = True
except ImportError:
    LLAMA_INSTALLED = False

current_model = None
current_model_name = ""
_model_lock = threading.Lock()

def check_sys():
    """Display system hardware info (GPU, VRAM, RAM)."""
    cuda_avail = torch.cuda.is_available()
    gpu_name = torch.cuda.get_device_name(0) if cuda_avail else "No GPU (CPU Mode)"
    vram = torch.cuda.get_device_properties(0).total_memory / 1024**3 if cuda_avail else 0
    ram = psutil.virtual_memory().total / 1024**3
    print(f"[SysInfo] GPU: {gpu_name}")
    print(f"[SysInfo] VRAM: {vram:.2f} GB")
    print(f"[SysInfo] System RAM: {ram:.2f} GB")
    return {"gpu": gpu_name, "vram_gb": round(vram, 2), "ram_gb": round(ram, 2), "cuda": cuda_avail}

def download_models():
    """Download required GGUF model files from HuggingFace Hub."""
    init_directories()
    download_flag = FLAGS['model_download']

    success_count = 0
    total_models = len(MODELS_CONFIG)

    for key, (repo, filename) in MODELS_CONFIG.items():
        try:
            target_file = os.path.join(PATHS[key], filename)
            if os.path.exists(target_file):
                print(f"[ModelManager] Model '{key}' already downloaded at {target_file}")
                success_count += 1
                continue

            print(f"[ModelManager] Downloading {key} ({repo})...")
            hf_hub_download(repo_id=repo, filename=filename, local_dir=PATHS[key])
            print(f"[ModelManager] Successfully downloaded {key}")
            success_count += 1
        except Exception as e:
            print(f"[ModelManager] Error downloading {key}: {e}")
            print("[ModelManager] Continuing to next model...")

    if success_count == total_models:
        with open(download_flag, 'w', encoding='utf-8') as f:
            f.write('downloaded')
        print("[ModelManager] All models are ready.")

def get_vram_usage():
    """Get reserved CUDA VRAM in MB."""
    if torch.cuda.is_available():
        return torch.cuda.memory_reserved(0) / 1024**2
    return 0

def unload_model():
    """Unload current model from memory and clear cache."""
    global current_model, current_model_name
    if current_model is not None:
        del current_model
        current_model = None
        current_model_name = ""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()

def load_model(model_key, silent=True):
    """Load specified GGUF model into memory."""
    global current_model, current_model_name
    if not LLAMA_INSTALLED:
        raise RuntimeError("llama-cpp-python package is not installed.")

    with _model_lock:
        if current_model_name == model_key and current_model is not None:
            return current_model

        if model_key not in MODELS_CONFIG:
            raise ValueError(f"Unknown model key: {model_key}")

        unload_model()

        repo, filename = MODELS_CONFIG[model_key]
        model_path = os.path.join(PATHS[model_key], filename)

        if not os.path.exists(model_path):
            print(f"[ModelManager] Model file missing: {model_path}. Attempting download...")
            download_models()

        gpu_layers = 28 if torch.cuda.is_available() else 0

        try:
            current_model = Llama(
                model_path=model_path,
                n_gpu_layers=gpu_layers,
                n_ctx=4096,
                n_batch=256,
                use_mmap=True,
                logits_all=False,
                verbose=False
            )
            current_model_name = model_key
            if not silent:
                print(f"[ModelManager] Model {model_key} active. VRAM: {get_vram_usage():.0f}MB")
        except Exception as e:
            print(f"[ModelManager] Warning: Failed loading with GPU layers ({e}). Falling back to CPU.")
            current_model = Llama(model_path=model_path, n_gpu_layers=0, n_ctx=4096, verbose=False)
            current_model_name = model_key

        return current_model

def get_model_route(user_input):
    """Route user query to the most appropriate model based on content."""
    code_keywords = [
        'python', 'javascript', 'typescript', 'java', 'cpp', 'c++', 'c#', 'code',
        'coding', 'debug', 'error', 'function', 'class', 'algorithm', 'database',
        'sql', 'html', 'css', 'react', 'next.js', 'api', 'rest', 'bug', 'fix'
    ]
    input_lower = user_input.lower()

    if any(kw in input_lower for kw in code_keywords):
        if len(user_input) > 500:
            return "deepseek_coder"
        return "qwen_coder"
    return "qwen_chat"

def build_prompt(user_input, history, max_history=3, web_context=""):
    """Build Qwen ChatML formatted prompt with conversation history and optional web context."""
    system_text = SYSTEM_PROMPT.strip()
    if web_context:
        system_text += f"\n\n{web_context.strip()}"

    full_prompt = f"<|im_start|>system\n{system_text}<|im_end|>\n"

    recent_history = history[-max_history:] if history else []
    for chat in recent_history:
        user_msg = chat.get('user', '')
        assistant_msg = chat.get('assistant', '')
        full_prompt += f"<|im_start|>user\n{user_msg}<|im_end|>\n"
        full_prompt += f"<|im_start|>assistant\n{assistant_msg}<|im_end|>\n"

    full_prompt += f"<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant\n"
    return full_prompt

def generate_stream(user_input, history, web_context="", on_complete_callback=None):
    """Generator yielding SSE formatted tokens for streaming API."""
    target_model_key = get_model_route(user_input)
    load_model(target_model_key, silent=True)

    full_prompt = build_prompt(user_input, history, web_context=web_context)
    assistant_buffer = ""

    try:
        with _model_lock:
            streamer = current_model(
                full_prompt,
                max_tokens=1024,
                temperature=0.2,
                top_p=0.8,
                stop=["<|im_end|>", "<|endoftext|>"],
                stream=True
            )

            for chunk in streamer:
                token = chunk['choices'][0]['text']
                if token:
                    assistant_buffer += token
                    yield f"data: {json.dumps({'text': token})}\n\n"

        if on_complete_callback:
            on_complete_callback(user_input, assistant_buffer)

        yield "data: [DONE]\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

def generate_response(user_input, history, web_context=""):
    """Non-streaming complete response generator for CLI mode."""
    target_model_key = get_model_route(user_input)
    load_model(target_model_key, silent=True)

    full_prompt = build_prompt(user_input, history, web_context=web_context)

    with _model_lock:
        output = current_model(
            full_prompt,
            max_tokens=1024,
            temperature=0.2,
            top_p=0.8,
            stop=["<|im_end|>", "<|endoftext|>"],
            echo=False
        )

    response = output['choices'][0]['text'].strip()
    return response
