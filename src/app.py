import streamlit as st
import pandas as pd
import time
from nlp_engine import NLPEngine
from fuzzy_logic import FuzzySystem

# Page Configuration for Premium Feel
st.set_page_config(
    page_title="TruthLens - AI Hoax Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for 2026 Aesthetic
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #ff4b4b 0%, #ff914d 100%);
        border: none;
        color: white;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #ff914d 0%, #ff4b4b 100%);
        transform: scale(1.02);
    }
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        background: -webkit-linear-gradient(eee, #333);
        -webkit-background-clip: text;
        color: #fff;
    }
    .metric-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Engines
@st.cache_resource
def load_engines():
    return NLPEngine(), FuzzySystem()

nlp, fuzzy = load_engines()

# Sidebar
with st.sidebar:
    st.title("🛡️ TruthLens v1.0")
    st.markdown("---")
    st.info("**Sistem Cerdas Deteksi Hoax**\nMenggunakan *Fuzzy Logic* untuk meniru penalaran manusia dalam menilai berita.")
    
    st.markdown("### ⚙️ Parameter Fuzzy")
    st.markdown("- **Capslock Ratio**: Seberapa banyak huruf besar?")
    st.markdown("- **Provocative Score**: Kata-kata bombastis & tanda baca.")
    
    st.markdown("---")
    st.caption("© 2026 Tugas KB IF504")

# Main Content
col1, col2 = st.columns([2, 1])

show_fuzzy_result = False

with col1:
    st.title("Deteksi Kebenaran Berita")
    st.markdown("##### *Uncertainty Reasoning System*")
    
    input_text = st.text_area("Masukkan Judul Berita:", height=100, placeholder="Contoh: MENGEJUTKAN!! Babi Ngepet Ditemukan di Depok...")

    if st.button("🔍 ANALISIS SEKARANG"):
        if input_text:
            with st.spinner('Memproses Linguistik & Kalkulasi Fuzzy...'):
                # 1. NLP Analysis
                nlp_result = nlp.analyze(input_text)
                
                # 2. Fuzzy Inference
                score, label = fuzzy.calculate(nlp_result['caps_ratio'], nlp_result['provocative_score'])
                show_fuzzy_result = True
                
                time.sleep(0.8) # Simulate processing for UX
                
                # Display Result
                st.markdown("### Hasil Analisis")
                
                # Result Banner
                if score > 60:
                    st.error(f"⚠️ {label}")
                elif score > 40:
                    st.warning(f"🤔 {label}")
                else:
                    st.success(f"✅ {label}")
                
                # Detailed Metrics
                st.markdown("#### Faktor Penentu (Crisp Inputs)")
                m1, m2, m3 = st.columns(3)
                
                with m1:
                    st.metric("Capslock Ratio", f"{nlp_result['caps_ratio']:.1f}%")
                with m2:
                    st.metric("Provocative Score", f"{nlp_result['provocative_score']:.1f}")
                with m3:
                    st.metric("Hoax Probability", f"{score:.1f}%")

                # Explanation
                st.markdown("---")
                st.markdown("#### 🧠 Logika Keputusan")
                st.write(f"Sistem mendeteksi **{nlp_result['caps_ratio']:.1f}%** huruf kapital dan skor provokasi **{nlp_result['provocative_score']}**. Berdasarkan aturan fuzzy, jika kedua nilai ini tinggi, kemungkinan hoax meningkat.")

        else:
            st.error("Mohon masukkan teks berita terlebih dahulu.")

with col2:
    st.header("📊 Visualisasi Fuzzy")
    if show_fuzzy_result:
        st.success("Grafik Menampilkan Posisi Input")
    else:
        st.info("Grafik Fungsi Keanggotaan (Statis)")
    
    # Show plots
    figs = fuzzy.get_plots(show_result=show_fuzzy_result)
    for fig in figs:
        st.pyplot(fig)
        
    st.markdown("---")
    st.markdown("#### 📂 Dataset Kalibrasi")
    try:
        df = pd.read_csv("data/news_samples.csv")
        st.dataframe(df.head(5), hide_index=True)
        st.caption(f"Total Database: {len(df)} entri")
    except:
        st.error("Dataset not found.")

