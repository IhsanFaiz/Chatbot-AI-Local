# Nox AI Chatbot Backend (`chatbot-be`)

Backend service berbasis Python Flask & `llama-cpp-python` yang didesain untuk menjalankan model AI lokal (GGUF) dengan streaming SSE (Server-Sent Events), intelligent model routing, manajemen memori percakapan, serta integrasi tunneling Pyngrok.

---

## 🚀 Fitur Utama

- **Lokal & Privacy-First**: Menjalankan model bahasa (GGUF) secara lokal di komputer tanpa bergantung pada API berbayar luar.
- **Intelligent Model Routing**: Otomatis mengarahkan pertanyaan pengguna ke model yang paling sesuai:
  - **Qwen 2.5 Coder 3B**: Untuk pertanyaan pemrograman & koding tingkat standar.
  - **DeepSeek Coder 1.3B**: Untuk penulisan atau perbaikan kode kompleks (>500 karakter).
  - **Qwen 2.5 Chat 3B**: Untuk percakapan umum & percakapan non-koding.
- **Real-time SSE Streaming**: Endpoint `/chat` mendukung streaming token secara real-time via Server-Sent Events.
- **Short-Term Memory**: Menyimpan riwayat percakapan secara terstruktur di `chat_history.json`.
- **Public Tunneling (Ngrok)**: Otomatis membuka URL publik via Pyngrok sehingga backend dapat diakses dari luar/Colab/Frontend staging.
- **Terminal CLI Mode**: Dapat dijalankan sebagai aplikasi percakapan interaktif berbasis command-line (`cli.py`).

---

## 📁 Struktur Direktori

```text
chatbot-be/
├── .env                  # Konfigurasi environment (di-ignore oleh git)
├── .env.example          # Template contoh environment
├── .gitignore            # Menjaga file berat (GGUF) & .env agar tidak terpush ke Git
├── app.py                # Server Flask API & SSE Streaming Endpoint
├── cli.py                # Mode percakapan interaktif via terminal (CLI)
├── config.py             # Konfigurasi path, environment, model, & prompt Nox
├── history_manager.py    # Manajemen simpan/muat riwayat chat JSON
├── local_llm/            # Tempat penyimpanan model GGUF & log (di-ignore oleh git)
│   ├── cache/
│   ├── flags/
│   ├── logs/
│   └── models/
├── main.py               # Launcher utama backend (CLI / Server / Download)
├── model_manager.py      # Pengelolaan unduh, loading, unloading, & routing GGUF
└── requirements.txt      # Dependensi pustaka Python
```

---

## 🛠️ Prasyarat & Instalasi

### 1. Prasyarat System
- **Python**: Version 3.10 / 3.11 / 3.12 / 3.14 (64-bit)
- **RAM**: Minimal 8 GB (Disarankan 16 GB+)
- **VRAM/GPU (Opsional)**: NVIDIA GPU dengan support CUDA (Opsional, otomatis menggunakan CPU jika GPU tidak ada).

### 2. Instalasi Pustaka Python
Jalankan perintah berikut pada terminal di dalam folder `chatbot-be`:

```bash
pip install -r requirements.txt
```

Atau jika ingin menginstal dependensi `llama-cpp-python` secara presisi:

```bash
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
pip install flask flask-cors pyngrok huggingface_hub psutil accelerate sentencepiece torch python-dotenv
```

---

## ⚙️ Konfigurasi Environment (`.env`)

Buat file `.env` di folder `chatbot-be` (atau salin dari `.env.example`):

```bash
cp .env.example .env
```

Isi variabel di file `.env`:

```env
# Port & Host Server Flask
PORT=5001
HOST=127.0.0.1
USE_NGROK=false

# Token Autentikasi Ngrok (Dapatkan di https://dashboard.ngrok.com/get-started/your-authtoken)
NGROK_AUTH_TOKEN=your_ngrok_auth_token_here

# Direktori Penyimpanan Model & Log
LOCAL_LLM_DIR=./local_llm
```

---

## Cara Menjalankan Backend

### 1. Menjalankan Server Flask API
Jalankan perintah berikut untuk mengaktifkan API server:

```bash
python main.py
# atau langsung
python app.py
```

- **Local Endpoint**: `http://127.0.0.1:5001`
- **Ngrok Public Endpoint**: Akan ditampilkan pada log terminal setelah server berjalan.

### 2. Menjalankan Mode Interactive CLI (Terminal Chat)
Untuk menguji obrolan langsung di terminal tanpa membuka browser:

```bash
python main.py --cli
# atau
python cli.py
```

Perintah khusus dalam CLI mode:
- `/exit`: Keluar dari aplikasi chat.
- `/clear`: Menghapus memori model dan riwayat obrolan.
- `/sys`: Menampilkan info penggunaan GPU/VRAM/RAM sistem.

### 3. Mengunduh Model GGUF Terlebih Dahulu
Jika ingin mengunduh model GGUF dari HuggingFace tanpa menjalankan server API:

```bash
python main.py --download-models
```

---

## 📡 Dokumentasi Endpoint API

### 1. `POST /chat` (SSE Streaming)
Mengirimkan prompt percakapan ke model LLM.

- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "message": "Buatkan fungsi rekursif fibonacci di Python"
  }
  ```
- **Response**: `text/event-stream`
  ```text
  data: {"text": "Tentu"}

  data: {"text": ", berikut"}

  data: {"text": " kodenya:"}

  data: [DONE]
  ```

### 2. `POST /clear`
Menghapus memori model yang dimuat di RAM/VRAM serta reset file riwayat obrolan.

- **Response**:
  ```json
  {
    "status": "success",
    "message": "Memory cleared"
  }
  ```

### 3. `GET /health`
Menampilkan status kesehatan server dan info hardware sistem.

- **Response**:
  ```json
  {
    "status": "online",
    "active_model": "qwen_coder",
    "vram_used_mb": 0,
    "system": {
      "cuda": false,
      "gpu": "No GPU (CPU Mode)",
      "ram_gb": 15.32,
      "vram_gb": 0
    }
  }
  ```

### 4. `GET /models`
Menampilkan daftar model yang didukung dan model yang sedang aktif dimuat.

- **Response**:
  ```json
  {
    "active_model": "qwen_coder",
    "available_models": [
      "qwen_chat",
      "qwen_coder",
      "deepseek_coder"
    ]
  }
  ```

---

## 🛡️ Catatan Git & Keamanan

File model GGUF (`*.gguf`), file flag (`*.flag`), serta file `.env` **secara otomatis diabaikan oleh `.gitignore`** agar file biner berukuran besar (2GB - 4GB+) dan rahasia token tidak ikut terpush ke repository GitHub.
