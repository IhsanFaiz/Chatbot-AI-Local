<div align="center">
  <img src="docs/assets/nox_ai_hero_banner.jpg" alt="Nox AI Hero Banner" style="max-width: 800px; width: 100%; height: auto; border-radius: 14px; box-shadow: 0 8px 24px rgba(0,0,0,0.25); margin-bottom: 24px;">

  # 🌟 Nox AI — Advanced Local Coding Assistant

  **A full-stack, privacy-focused intelligent AI coding assistant running 100% locally on your machine.**

  [![Backend: Flask](https://img.shields.io/badge/Backend-Flask%20%7C%20Python-blue?style=for-the-badge&logo=flask)](./chatbot-be)
  [![Frontend: Next.js](https://img.shields.io/badge/Frontend-Next.js%20%7C%20React-black?style=for-the-badge&logo=next.js)](./chatbot-ai)
  [![AI Engine: Llama.cpp](https://img.shields.io/badge/AI%20Engine-Llama.cpp%20%7C%20GGUF-orange?style=for-the-badge&logo=c%2B%2B)](https://github.com/abetlen/llama-cpp-python)
  [![Privacy: 100% Offline](https://img.shields.io/badge/Privacy-100%25%20Local-green?style=for-the-badge)](#-key-features)
</div>

<br>

## 📖 Overview

**Nox AI** is a full-stack chatbot platform engineered specifically as an intelligent coding assistant. Unlike conventional cloud-based AI solutions that transmit your sensitive codebase to third-party servers, Nox AI executes GGUF quantized models (such as *Qwen 2.5 Coder* and *DeepSeek Coder*) **entirely on your local hardware**.

This approach guarantees absolute privacy for your source code, minimizes inference latency, and provides powerful developer capabilities even without an active internet connection.

---

## ✨ Key Features

- 🔒 **Privacy-First (100% Local)**: Zero code telemetry. All data processing and LLM inferences take place locally on your computer.
- 🧠 **Intelligent Model Routing**: Automatically detects prompt complexity and selects the optimal model for the task:
  - `Qwen 2.5 Chat 3B` — General conversations and explanations.
  - `Qwen 2.5 Coder 3B` — Code generation, algorithm optimization, and debugging.
  - `DeepSeek Coder 1.3B` — Rapid script analysis and lightweight tasks.
- ⚡ **Real-Time SSE Streaming**: Instant response generation using Server-Sent Events for a smooth, interactive typing experience.
- 🎨 **Modern & Responsive UI**: Designed with Next.js and Tailwind CSS, offering a clean dark-mode interface, inline code highlighting, and auto-scroll capabilities.
- 🌐 **Built-in Ngrok Support**: Optional integrated tunneling support for sharing local endpoints securely during remote testing.

---

## 🏗️ Repository Architecture

This project is structured as a clean monorepo containing distinct frontend and backend applications:

```text
fullstack-chatbot/
├── chatbot-ai/      # 🖥️ FRONTEND (Next.js 15, React 19, Tailwind CSS)
│   ├── app/         # App router pages and global styles
│   ├── components/  # Modular chat components (ChatInput, ChatMessage, etc.)
│   └── public/      # Static web assets
│
├── chatbot-be/      # ⚙️ BACKEND (Python 3, Flask, Llama.cpp)
│   ├── app.py       # Flask REST & SSE Streaming API Server
│   ├── local_llm/   # GGUF AI model storage directory
│   ├── cli.py       # Standalone interactive terminal chat mode
│   └── config.py    # Global configuration and environment settings
│
├── docs/            # Project documentation and assets
└── README.md        # Primary project documentation (This file)
```

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following software installed on your system:
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
4. Setup environment variables:
   ```bash
   cp .env.example .env
   ```
   *(Optionally edit `.env` to configure ports or toggle Ngrok with `USE_NGROK=false`)*
5. Start the backend API server:
   ```bash
   python app.py
   ```
   > The API server will run locally at `http://127.0.0.1:5001`.

*(For detailed endpoint documentation, see the [Backend README](./chatbot-be/README.md)).*

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
4. Open [http://localhost:3000](http://localhost:3000) in your web browser to interact with Nox AI!

---

## 🛠️ Tech Stack

| Domain | Technology | Description |
| :--- | :--- | :--- |
| **Frontend Framework** | [Next.js 15](https://nextjs.org/) | React framework with App Router |
| **UI & Styling** | [Tailwind CSS](https://tailwindcss.com/) | Modern utility-first CSS framework |
| **Backend API** | [Flask](https://flask.palletsprojects.com/) | Lightweight Python Web API with SSE support |
| **AI Engine** | [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) | High-performance C++ GGUF inference binding |
| **Model Weights** | [Hugging Face](https://huggingface.co/) | Quantized open-weight GGUF coding models |

---

## 📜 License & Contributions

This project is open-source and built for developers who value privacy and AI productivity. Community contributions, feature suggestions, and bug reports are warmly welcome!

<div align="center">
  <sub>Built with ❤️ for privacy-conscious software engineers.</sub>
</div>
