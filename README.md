<div align="center">
  <img src="docs/assets/nox_ai_for_banner.jpg" alt="Nox AI Banner" style="max-width: 800px; width: 100%; height: auto; border-radius: 14px; box-shadow: 0 8px 24px rgba(0,0,0,0.25); margin-bottom: 24px;">

  # 🌟 Nox AI — Local AI Coding Assistant

  **A local chatbot interface for running open-source AI coding models directly on your machine.**

  [![Backend: Flask](https://img.shields.io/badge/Backend-Flask%20%7C%20Python-blue?style=for-the-badge&logo=flask)](./chatbot-be)
  [![Frontend: Next.js](https://img.shields.io/badge/Frontend-Next.js%20%7C%20React-black?style=for-the-badge&logo=next.js)](./chatbot-ai)
  [![AI Engine: Llama.cpp](https://img.shields.io/badge/AI%20Engine-Llama.cpp%20%7C%20GGUF-orange?style=for-the-badge&logo=c%2B%2B)](https://github.com/abetlen/llama-cpp-python)
</div>

<br>

## 📖 Overview

**Nox AI** is a full-stack chatbot application that allows you to run quantized GGUF models locally. It provides a web interface to interact with models like *Qwen 2.5 Coder* and *DeepSeek Coder* without needing to send your code to external APIs. 

By running the models locally, you can keep your source code on your machine and use the assistant even when offline.

---

## 💻 System Requirements

Running local AI models requires decent hardware. Since this project uses `llama-cpp-python`, performance will depend on your CPU and whether you can offload processing to a GPU.

### Minimum Requirements (for 1.3B - 3B models)
- **OS**: Windows, macOS, or Linux
- **RAM**: 8 GB system memory
- **Storage**: ~5-10 GB of free space (for downloading GGUF model files)

### Recommended Requirements (for better inference speed)
- **RAM**: 16 GB or higher
- **GPU**: A dedicated GPU with at least 4GB VRAM (NVIDIA, AMD, or Apple Silicon) is highly recommended. You can offload model layers to the GPU to significantly speed up token generation.

---

## ✨ Key Features

- 🔒 **Local Execution**: Runs entirely on your own hardware. No external server calls are made for inference.
- 🧠 **Model Selection**: Switch between different models (like Qwen or DeepSeek) depending on the task and your hardware capabilities.
- ⚡ **Streaming Responses**: Uses Server-Sent Events (SSE) to stream text back to the UI as it generates.
- 🎨 **Web UI**: A straightforward, responsive interface built with Next.js and Tailwind CSS, featuring dark mode and code highlighting.
- 🌐 **Ngrok Support**: Optional integrated tunneling if you need to access your local backend remotely.

---

## 🏗️ Repository Architecture

The project is a monorepo containing a frontend and a backend:

```text
fullstack-chatbot/
├── chatbot-ai/      # 🖥️ FRONTEND (Next.js 15, React 19, Tailwind CSS)
│   ├── app/         # App router pages
│   ├── components/  # UI components
│   └── public/      # Static assets
│
├── chatbot-be/      # ⚙️ BACKEND (Python 3, Flask, Llama.cpp)
│   ├── app.py       # Flask REST & SSE API
│   ├── local_llm/   # Directory for GGUF model files
│   ├── cli.py       # Terminal chat mode
│   └── config.py    # Configuration and environment variables
│
├── docs/            # Documentation and assets
└── README.md        # This file
```

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:
- **Python** (v3.10 or higher)
- **Node.js** (v18 or higher) and `npm`

---

### 1. Setting Up the Backend (`chatbot-be`)

1. Navigate to the backend directory:
   ```bash
   cd chatbot-be
   ```
2. Create and activate a Virtual Environment (recommended):
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   > **Note**: For GPU acceleration with `llama-cpp-python`, you may need to install it with specific build flags (e.g., `CMAKE_ARGS="-DGGML_CUDA=on"` for NVIDIA). Check the [llama-cpp-python documentation](https://github.com/abetlen/llama-cpp-python) for details.
4. Setup environment variables:
   ```bash
   cp .env.example .env
   ```
   *(Edit `.env` to configure ports or toggle Ngrok with `USE_NGROK=false`)*
5. Start the backend API server:
   ```bash
   python app.py
   ```
   > The API server will run locally at `http://127.0.0.1:5001`.

*(For more details, see the [Backend README](./chatbot-be/README.md)).*

<br>

### 2. Setting Up the Frontend (`chatbot-ai`)

1. Open a new terminal tab and navigate to the frontend directory:
   ```bash
   cd chatbot-ai
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Open [http://localhost:3000](http://localhost:3000) in your web browser to start using the app.

---

## 🛠️ Tech Stack

| Domain | Technology |
| :--- | :--- |
| **Frontend Framework** | [Next.js 15](https://nextjs.org/) |
| **UI & Styling** | [Tailwind CSS](https://tailwindcss.com/) |
| **Backend API** | [Flask](https://flask.palletsprojects.com/) |
| **AI Engine** | [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) |
| **Model Weights** | [Hugging Face](https://huggingface.co/) |

---

## 📜 License & Contributions

This is an open-source project. Feel free to submit issues or pull requests if you have suggestions or improvements!

<div align="center">
  <sub>Built for developers running local AI.</sub>
</div>
