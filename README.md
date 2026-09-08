<div align="center">
  <img src="docs/assets/nox_ai_hero_banner.jpg" alt="Nox AI Hero Banner" width="100%" style="border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); margin-bottom: 20px;">

  # 🌟 Nox AI - Advanced Local Coding Assistant

  **Solusi lengkap (Fullstack) untuk asisten pemrograman AI cerdas, aman, dan privasi-terjaga yang berjalan sepenuhnya di perangkat lokal Anda.**

  [![Backend: Flask](https://img.shields.io/badge/Backend-Flask%20%7C%20Python-blue?style=for-the-badge&logo=flask)](./chatbot-be)
  [![Frontend: Next.js](https://img.shields.io/badge/Frontend-Next.js%20%7C%20React-black?style=for-the-badge&logo=next.js)](./chatbot-ai)
  [![AI: Llama.cpp](https://img.shields.io/badge/AI-Llama.cpp%20%7C%20GGUF-orange?style=for-the-badge&logo=c%2B%2B)](https://github.com/abetlen/llama-cpp-python)
</div>

<br>

## 📖 Deskripsi Proyek

**Nox AI** adalah sistem *fullstack chatbot* yang dirancang khusus untuk menjadi asisten pemrograman (*coding assistant*). Tidak seperti asisten AI konvensional yang mengirimkan kode sumber Anda ke server pihak ketiga, Nox AI menjalankan model GGUF tingkat lanjut (seperti Qwen 2.5 Coder dan DeepSeek Coder) secara **100% lokal**. 

Hal ini menjamin privasi kode sumber Anda, mengurangi latensi, dan memberikan kemampuan pemrograman yang tajam bahkan tanpa koneksi internet.

---

## ✨ Fitur Unggulan

- 🔒 **Privacy-First (100% Local)**: Tidak ada baris kode Anda yang dikirim ke server eksternal. Semua pemrosesan data dilakukan di mesin lokal.
- 🧠 **Intelligent Model Routing**: Nox AI secara otomatis mendeteksi seberapa kompleks pertanyaan Anda dan mengalihkannya ke model yang paling efisien:
  - `Qwen 2.5 Chat 3B` untuk percakapan umum.
  - `Qwen 2.5 Coder 3B` untuk perbaikan kode dan algoritma.
  - `DeepSeek Coder 1.3B` untuk analisis skrip yang panjang.
- ⚡ **Real-time SSE Streaming**: Nikmati respons instan dari AI seperti mengetik secara real-time.
- 🎨 **Modern UI/UX**: Frontend dibangun dengan Next.js dan TailwindCSS yang menghadirkan tampilan *sleek*, *dark-mode*, dan interaktif.
- 🌐 **Ngrok Integration**: Backend memiliki dukungan terintegrasi dengan Ngrok jika Anda perlu membagikan endpoint AI ke luar atau untuk pengujian tim.

---

## 🏗️ Arsitektur Proyek (Monorepo)

Proyek ini dibagi menjadi dua bagian utama: Frontend dan Backend.

```text
fullstack-chatbot/
├── chatbot-ai/      # 🖥️ FRONTEND (Next.js, React, TailwindCSS)
│   ├── app/         # Routing dan komponen utama aplikasi Next.js
│   ├── components/  # Komponen UI chat yang reusable
│   └── public/      # Aset statis web
│
├── chatbot-be/      # ⚙️ BACKEND (Python Flask, Llama.cpp)
│   ├── app.py       # API Endpoint Server (SSE)
│   ├── local_llm/   # Tempat penyimpanan model AI (GGUF)
│   ├── cli.py       # Mode chat langsung via terminal
│   └── config.py    # Konfigurasi sistem dan enviroment
│
├── docs/            # Dokumentasi & Aset gambar
└── README.md        # Dokumentasi utama (File ini)
```

---

## 🚀 Cara Memulai (Getting Started)

### 1. Menyiapkan Backend (`chatbot-be`)

Backend Nox AI bertanggung jawab untuk memuat dan memproses model AI GGUF. 

1. Masuk ke direktori backend:
   ```bash
   cd chatbot-be
   ```
2. Buat Virtual Environment (opsional namun disarankan) dan install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
3. Konfigurasi Environment:
   ```bash
   cp .env.example .env
   ```
   *(Sesuaikan isi `.env` sesuai kebutuhan, misalnya mematikan Ngrok dengan `USE_NGROK=false`)*
4. Jalankan Server API:
   ```bash
   python main.py
   ```
   > Server secara default akan berjalan di `http://127.0.0.1:5001`.

*(Untuk dokumentasi lengkap tentang endpoint backend, silakan merujuk ke [README Backend](./chatbot-be/README.md)).*

<br>

### 2. Menyiapkan Frontend (`chatbot-ai`)

Frontend menyediakan antarmuka interaktif bagi pengguna untuk berkomunikasi dengan Nox AI.

1. Buka terminal baru dan masuk ke direktori frontend:
   ```bash
   cd chatbot-ai
   ```
2. Install dependencies (Pastikan Anda sudah menginstal Node.js):
   ```bash
   npm install
   ```
3. Konfigurasi Endpoint:
   Pastikan aplikasi React mengarah ke `http://127.0.0.1:5001` sesuai dengan port yang terbuka di Backend.
4. Jalankan Development Server:
   ```bash
   npm run dev
   ```
5. Buka [http://localhost:3000](http://localhost:3000) di browser favorit Anda dan mulailah berdiskusi dengan Nox AI!

---

## 🛠️ Teknologi yang Digunakan

**Frontend:**
- [Next.js 15](https://nextjs.org/) (React Framework)
- [Tailwind CSS](https://tailwindcss.com/) (Styling)

**Backend:**
- [Python 3](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/) (Web API)
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) (AI Inference)
- [HuggingFace Hub](https://huggingface.co/) (Model Source)

---

## 📜 Lisensi & Kontribusi

Proyek ini dibangun untuk tujuan edukasi dan peningkatan produktivitas developer. Kontribusi dari komunitas sangat diapresiasi! Jangan ragu untuk membuat *Pull Request* atau melaporkan *Issue* jika menemukan bug.

<div align="center">
  <p>Dibuat dengan ❤️ untuk para developer.</p>
</div>
