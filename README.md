# 🛡️ TruthLens: AI Agent Hoax Detector
### Tugas Besar Kecerdasan Buatan (IF504/IF505)
**Topik: Agentic Uncertainty Reasoning dengan LangGraph, DeepSeek R1, & Fuzzy Logic**

---

## 📋 Deskripsi Proyek
**TruthLens v2.0** telah berevolusi dari sekadar sistem Fuzzy Logic menjadi **Agen AI Otonom**. Sistem ini sekarang menggabungkan penalaran mendalam (*Deep Reasoning*) menggunakan LLM (DeepSeek R1) dengan kemampuan **Pencarian Internet Real-time** dan analisis **Fuzzy Logic** internal.

Sistem tidak hanya melihat "bentuk" teks (kapital/tanda baca), tetapi juga memverifikasi "isi" berita dengan mencari fakta di internet.

### 🧠 Arsitektur Hybrid
Sistem ini menggabungkan dua paradigma AI:
1.  **AI Simbolik (Fuzzy Logic)**: Menangani ketidakpastian linguistik (gaya penulisan clickbait/hoax).
2.  **Generative AI (LangGraph Agent)**: Mengelola alur berpikir (reasoning), pencarian fakta, dan sintesa kesimpulan akhir.

---

## 🌟 Fitur Utama Baru (v2.0)

### 1. 🤖 LangGraph Agent Workflow
Agen bekerja dengan alur berpikir terstruktur (Graph):
-   **Verifier Node**: Mencari kebenaran berita secara otomatis di internet (via Tavily/DuckDuckGo).
-   **Analyst Node**: Memanggil modul *Fuzzy Logic* untuk "mengaudit" gaya bahasa judul berita.
-   **Finalizer Node**: Menggabungkan bukti eksternal (fakta internet) dan internal (skor fuzzy) untuk memberikan vonis akhir.

### 2. 🌍 Internet Search Capability
Agen dapat melakukan "Fact Checking" mandiri. Jika Anda memasukkan berita tentang "Babi Ngepet di Depok", agen akan mencari berita terkait di sumber terpercaya sebelum menjawab.

### 3. 🧠 DeepSeek R1 Integration
Menggunakan model *reasoning* mutakhir (DeepSeek R1 via OpenRouter) untuk memberikan penjelasan yang logis, mendalam, dan transparan.

### 4. 📊 Tetap Mempertahankan Fuzzy Logic
Fitur klasik tetap ada sebagai salah satu "Alat" yang digunakan Agent:
*   **Capslock Ratio**: Analisis bentuk huruf.
*   **Provocative Score**: Analisis kata-kata pemicu emosi.

---

## 🛠️ Teknologi Stack
*   **Orchestration**: `LangGraph`, `LangChain`
*   **LLM**: `DeepSeek R1` (via OpenRouter)
*   **Search**: `Tavily API` / `DuckDuckGo`
*   **Logic**: `scikit-fuzzy`, `Sastrawi`
*   **Interface**: `Streamlit`
*   **Infrastructure**: `Docker`

---

## 🚀 Panduan Instalasi & Penggunaan

### Prasyarat
1.  **Docker Desktop** Installed.
2.  **API Key** (Salah satu atau keduanya):
    *   `OPENROUTER_API_KEY`: Untuk akses model DeepSeek R1 (Wajib).
    *   `TAVILY_API_KEY`: Untuk hasil pencarian internet yang lebih akurat (Opsional).

### Cara Menjalankan

1.  **Setup Environment**
    Salin file contoh konfigurasi:
    ```powershell
    cp .env.example .env
    ```
    Buka file `.env` dan masukkan API Key Anda.

2.  **Jalankan Docker Compose**
    *Karena ada penambahan library baru, lakukan build ulang:*
    ```powershell
    docker-compose down
    docker-compose up --build
    ```

3.  **Akses Aplikasi**
    Buka: **http://localhost:8501**
    *Jika API Key belum diset di `.env`, Anda juga bisa memasukkannya lewat Sidebar di aplikasi.*

---

## 📂 Struktur File Baru

```
TugasKBSistemFuzzy/
├── .env                # [NEW] File rahasia untuk API Key
├── data/
├── src/
│   ├── app.py          # UI Streamlit (Updated for Agent)
│   ├── agent.py        # [NEW] Logika LangGraph & Nodes
│   ├── tools.py        # [NEW] Tool Search & Fuzzy Wrapper
│   ├── nlp_engine.py   # Modul NLP (Tools)
│   └── fuzzy_logic.py  # Modul Fuzzy (Tools)
├── Dockerfile          # Updated dependencies
├── docker-compose.yml  # Supports .env
└── requirements.txt    # Added langgraph, langchain, etc.
```

---

## 🧪 Contoh Skenario Agen

**Input**: "VIRAL!! Meteor Jatuh di Monas Hari Ini??"

**Proses Agen**:
1.  -> **Verifier**: *Searching Google: "Meteor jatuh di Monas hari ini fakta"* -> *Result: "Tidak ada berita valid mengenai meteor di Monas."*
2.  -> **Analyst**: *Fuzzy Check* -> *Capslock 100%, Provokatif Tinggi* -> *Fuzzy Score: 95% (Hoax)*.
3.  -> **Finalizer**: *"Berita ini HOAX. Bukti pencarian nihil, dan gaya penulisannya sangat ciri khas clickbait (Fuzzy Score 95%)."*

---

**Dibuat oleh Kelompok KB - IF504**
*Updated jan 2026 for Agentic AI Course*
