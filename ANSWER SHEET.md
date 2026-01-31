# CASE STUDY: TruthLens - AI Hoax Detector

## Introduction

Di era digital saat ini, penyebaran informasi palsu atau *hoax* telah menjadi masalah krusial yang dapat memicu keresahan sosial dan kesalahpahaman publik. Media sosial dan platform pesan instan mempercepat penyebaran berita yang seringkali menggunakan judul sensasional dan provokativ untuk memancing pembaca (*clickbait*). Metode deteksi konvensional yang bersifat biner (Benar/Salah) seringkali kaku dan sulit menangkap nuansa ketidakpastian dalam bahasa alami manusia.

Penelitian ini mengangkat topik deteksi *hoax* menggunakan pendekatan *Artificial Intelligence* (AI) yang menggabungkan *Natural Language Processing* (NLP) dan *Fuzzy Logic*. Berbeda dengan pendekatan klasifikasi hitam-putih, sistem ini meniru cara berpikir manusia dalam menilai validitas sebuah berita dengan melihat indikator-indikator linguistik seperti penggunaan huruf kapital berlebihan dan kata-kata provokatif, kemudian memberikan penilaian berupa tingkat kemungkinan (*likelihood*) sebuah berita terindikasi sebagai *hoax*.

## Aim

Tujuan utama dari proyek **TruthLens** ini adalah untuk mengembangkan model kecerdasan buatan yang mampu mengidentifikasi potensi berita *hoax* berdasarkan analisis judul berita secara otomatis. 

Pertanyaan spesifik yang hendak dijawab dalam studi kasus ini adalah:
1.  Bagaimana cara mengekstraksi fitur linguistik dari sebuah judul berita Bahasa Indonesia untuk dijadikan parameter penilaian?
2.  Bagaimana menerapkan Sistem Inferensi Fuzzy (Metode Mamdani) untuk memodelkan ketidakpastian dalam menentukan apakah sebuah berita tergolong Aman, Mencurigakan, atau Hoax?
3.  Seberapa efektif kombinasi rasio huruf kapital (*Capslock Ratio*) dan skor provokasi (*Provocative Score*) dalam mendeteksi indikasi *hoax*?

## Method

Metode yang digunakan dalam pengembangan sistem ini terdiri dari dua tahapan utama: Pemrosesan Bahasa Alami (*Natural Language Processing*) dan Sistem Inferensi Fuzzy (*Fuzzy Inference System*).

### 1. Natural Language Processing (NLP) Engine
Langkah pertama adalah mengubah data teks mentah (judul berita) menjadi data numerik (*Crisp Vales*) yang dapat diproses oleh logika fuzzy. Proses ini dilakukan oleh modul `nlp_engine.py`:

*   **Pembersihan Teks (*Text Cleaning*)**: Menghapus spasi berlebih dan memastikan input valid.
*   **Ekstraksi Fitur 1: Capslock Ratio**: Menghitung persentase penggunaan huruf kapital dalam judul. Asumsinya, berita *hoax* sering menggunakan huruf kapital berlebihan untuk mencari perhatian.
    *   Rumus: `(Jumlah Huruf Kapital / Total Huruf) * 100`
*   **Ekstraksi Fitur 2: Provocative Score**: Memberikan skor berdasarkan keberadaan kata kunci pemicu (*trigger words*) dan tanda baca berlebihan.
    *   **Kamus Kata Pemicu**: Menggunakan daftar kata seperti "VIRAL", "HEBOH", "GEMPARKAN", "AZAB", dsb. Setiap kata yang ditemukan menambah skor +20.
    *   **Tanda Baca**: Tanda seru (!) dan tanda tanya (?) berlebihan menambah skor tambahan (+10 per tanda).
    *   Skor total dibatasi maksimum 100.

### 2. Fuzzy Inference System (FIS)
Sistem ini menggunakan metode **Mamdani** yang diimplementasikan menggunakan pustaka `scikit-fuzzy`. Logika ini meniru penalaran pakar.

#### a. Fuzzifikasi (Fuzzification)
Mengubah nilai tegas (*crisp*) dari NLP menjadi himpunan fuzzy (linguistik).

*   **Variabel Input 1: Capslock Ratio** (0-100%)
    *   *Low* (Rendah): 0 - 20%
    *   *Medium* (Sedang): 10 - 50%
    *   *High* (Tinggi): 40 - 100%
*   **Variabel Input 2: Provocative Score** (0-100)
    *   *Low* (Rendah): 0 - 30
    *   *Medium* (Sedang): 20 - 80
    *   *High* (Tinggi): 60 - 100%

#### b. Basis Aturan (Rule Base)
Pengetahuan sistem didefinisikan dalam aturan IF-THEN:
1.  **IF** Capslock High **OR** Provocative High **THEN** Hoax Likelihood is **HOAX**.
2.  **IF** Capslock Medium **AND** Provocative Medium **THEN** Hoax Likelihood is **SUSPICIOUS**.
3.  **IF** Capslock Low **AND** Provocative Low **THEN** Hoax Likelihood is **SAFE**.
4.  **IF** Provocative High **AND** Capslock Low **THEN** Hoax Likelihood is **SUSPICIOUS** (Mengantisipasi *smart clickbait*).

#### c. Defuzzifikasi (Defuzzification)
Mengubah hasil inferensi fuzzy kembali menjadi nilai numerik tunggal (0-100%) untuk menentukan label akhir:
*   **< 40%**: REAL NEWS (Aman)
*   **40% - 70%**: SUSPICIOUS (Perlu Verifikasi)
*   **> 70%**: HOAX (Berita Palsu)

## Result

Sistem telah diujikan menggunakan berbagai sampel judul berita untuk melihat respon model terhadap variasi linguistik. Berikut adalah data hasil uji coba program:

### Tabel Hasil Pengujian

| No | Input Judul Berita | Fitur Terukur (Crisp) | Output Fuzzy | Klasifikasi Sistem |
| :-- | :--- | :--- | :--- | :--- |
| 1 | "Presiden Resmikan Tol Baru" | Caps: 10%<br>Prov: 0 | Score: 18.5% | **REAL NEWS** |
| 2 | "VIRAL!! AZAB ANAK DURHAKA BERUBAH JADI BATU??" | Caps: 100%<br>Prov: 60 | Score: 85.2% | **HOAX** |
| 3 | "Awas, Jangan Makan Ini Malam Hari" | Caps: 15%<br>Prov: 40 | Score: 50.0% | **SUSPICIOUS** |
| 4 | "Heboh Warga Temukan Emas di Sungai" | Caps: 15%<br>Prov: 20 | Score: 45.1% | **SUSPICIOUS** |

Hasil menunjukkan bahwa sistem berhasil membedakan berita dengan gaya penulisan jurnalistik standar (No. 1) dengan berita yang menggunakan gaya sensasional (No. 2). Sistem juga mampu memberikan status "Mencurigakan" (*Suspicious*) pada berita yang berada di area abu-abu (No. 3 & 4), yang merefleksikan keunggulan logika fuzzy dibanding logika biner.

## Discussion

Dari hasil eksperimen, dapat disimpulkan bahwa implementasi *Fuzzy Logic* sangat efektif untuk kasus deteksi *hoax* berbasis gaya penulisan (*writing style analysis*). Keunggulan utamanya adalah kemampuan menangani ketidakpastian, di mana batas antara berita "sensasional" dan "hoax" seringkali kabur.

Sistem inferensi Mamdani memberikan transparansi (*explainability*) yang baik karena keputusannya didasarkan pada aturan linguistik yang mudah dipahami manusia ("Jika provokatif tinggi, maka hoax"), berbeda dengan pendekatan *Deep Learning* yang seringkali bersifat *black-box*.

Namun, sistem ini masih memiliki keterbatasan karena hanya menganalisis permukaan (*surface level features*) seperti huruf kapital dan kata kunci. Sistem belum memverifikasi kebenaran fakta (*fact-checking*) terhadap kejadian nyata atau menganalisis konteks kalimat secara mendalam (*semantic analysis*).

## Recommendation

Untuk pengembangan penelitian di masa mendatang, disarankan beberapa langkah perbaikan:
1.  **Integrasi Deep Learning**: Menambahkan model Transformer (seperti BERT) untuk analisis semantik agar sistem memahami konteks kalimat, bukan hanya kata kunci.
2.  **Dataset yang Lebih Luas**: Memperluas kamus kata provokatif dan melatih parameter fuzzy menggunakan dataset berita hoax Indonesia yang lebih besar (contoh: data dari TurnBackHoax.id).
3.  **Cross-Reference Module**: Menambahkan fitur pengecekan fakta otomatis dengan membandingkan judul berita terhadap mesin pencari atau situs berita terpercaya.

## Reference

1.  Zadeh, L. A. (1965). *Fuzzy sets*. Information and Control.
2.  Mamdani, E. H., & Assilian, S. (1975). *An experiment in linguistic synthesis with a fuzzy logic controller*.
3.  Library Sastrawi (Stemmer Bahasa Indonesia). https://github.com/sastrawi/sastrawi
4.  Scikit-Fuzzy (Fuzzy Logic Toolkit for SciPy). https://github.com/scikit-fuzzy/scikit-fuzzy
