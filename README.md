# 🛡️ TruthLens: AI Hoax Detector
### Tugas Besar Kecerdasan Buatan (IF504/IF505)
**Topik: Uncertainty Reasoning dengan Sistem Fuzzy & NLP**

---

## 📋 Deskripsi Proyek
**TruthLens** adalah agen AI cerdas yang dirancang untuk mendeteksi potensi **Berita Palsu (Hoax)** berdasarkan analisis judul berita. Berbeda dengan pendekatan klasifikasi biner sederhana (Benar/Salah), sistem ini menggunakan **Fuzzy Logic (Logika Samar)** untuk memberikan "Derajat Kebarana" (Degree of Memberships).

Sistem ini menggabungkan:
1.  **Natural Language Processing (NLP)**: Mengekstrak fitur linguistik dari teks Bahasa Indonesia.
2.  **Fuzzy Inference System (FIS)**: Meniru cara berpikir manusia dalam menilai validitas berita berdasarkan indikator visual dan tekstual.

---

## 🌟 Fitur Utama

### 1. Analisis Linguistik Otomatis (NLP Engine)
Sistem secara otomatis menghitung *Crisp Input* dari teks yang dimasukkan:
*   **Capslock Ratio**: Persentase penggunaan huruf kapital yang tidak wajar. (Contoh: "VIRAL!!" = 100% Capslock).
*   **Provocative Score**: Skor berbasis kata kunci *clickbait* (misal: "Gemparkan", "Azab", "Ternyata") dan penggunaan tanda baca berlebihan (!, ?).

### 2. Sistem Penalaran Fuzzy
Menggunakan metode Mamdani dengan aturan inferensi (Rule Base) seperti:
*   *IF Capslock Tinggi AND Provokatif Tinggi THEN Hoax Potensial Tinggi.*
*   *IF Capslock Rendah AND Provokatif Rendah THEN Berita Aman.*

### 3. Visualisasi Data Interaktif
*   **Grafik Fungsi Keanggotaan**: Melihat bagaimana komputer memetakan angka menjadi konsep bahasa ("Rendah", "Sedang", "Tinggi").
*   **Real-time Analysis**: Hasil analisis muncul seketika saat tombol ditekan.

---

## 🛠️ Teknologi yang Digunakan
*   **Bahasa Pemrograman**: Python 3.9
*   **Core Logic**: `scikit-fuzzy` (Logika Fuzzy), `Sastrawi` (Stemming Bahasa Indonesia).
*   **Interface**: `Streamlit` (Modern Web UI).
*   **Environment**: `Docker` & `Docker Compose` (Fully Containerized).

---

## 🚀 Panduan Instalasi & Penggunaan

### Prasyarat
Pastikan Anda telah menginstal **Docker Desktop** di komputer Anda. Tidak perlu menginstal Python secara manual.

### Cara Menjalankan (Langkah Demi Langkah)

1.  **Extract / Buka Folder Proyek**
    Pastikan Anda berada di dalam folder `TugasKBSistemFuzzy`.

2.  **Jalankan Docker Compose**
    Buka terminal (CMD/PowerShell) di folder tersebut, lalu ketik:
    ```powershell
    docker-compose up --build
    ```
    *Tunggu hingga proses build selesai dan muncul pesan bahwa server telah berjalan.*

3.  **Buka Aplikasi**
    Buka browser (Chrome/Edge) dan kunjungi alamat:
    👉 **http://localhost:8501**

### Cara Menggunakan Aplikasi
1.  **Masukkan Judul**: Ketik judul berita yang ingin diuji pada kolom input (Contoh: *"BABI NGEPET TERTANGKAP DI DEPOK!!"*).
2.  **Klik Analisis**: Tekan tombol **"ANALISIS SEKARANG"**.
3.  **Lihat Hasil**:
    *   **Status Cek**: Aman / Mencurigakan / Hoax.
    *   **Metrik**: Lihat berapa skor Capslock dan Provokasi yang terdeteksi.
    *   **Penjelasan**: Baca alasan logis mengapa sistem memberikan label tersebut.

---

## 📂 Struktur File

```
TugasKBSistemFuzzy/
├── data/
│   └── news_samples.csv    # Dataset kecil untuk validasi aturan Fuzzy
├── src/
│   ├── app.py              # Kode utama antarmuka (Streamlit)
│   ├── nlp_engine.py       # Modul pemrosesan teks (NLP)
│   └── fuzzy_logic.py      # Definisi aturan dan fungsi keanggotaan Fuzzy
├── Dockerfile              # Konfigurasi container
├── docker-compose.yml      # Konfigurasi orkestrasi service
├── requirements.txt        # Daftar pustaka Python yang dibutuhkan
└── README.md               # Dokumentasi proyek ini
```

---

## 🧪 Contoh Pengujian

| Input Judul | Prediksi Sistem | Alasan |
| :--- | :--- | :--- |
| "Presiden Resmikan Tol Baru" | **REAL NEWS (Aman)** | Capslock minim, bahasa baku. |
| "VIRAL!! AZAB ANAK DURHAKA BERUBAH JADI BATU??" | **HOAX (Berita Palsu)** | Capslock tinggi, ada kata "Viral", "Azab", tanda tanya ganda. |
| "Awas, Jangan Makan Ini Malam Hari" | **SUSPICIOUS (Perlu Verifikasi)** | Capslock normal, tapi ada kata "Awas" (Clickbait). |

---

**Dibuat oleh Kelompok KB - IF504**
*Semester Ganjil 2025/2026*
