import streamlit as st
import pandas as pd
import time
import os
from src.agent import graph
from src.fuzzy_logic import FuzzySystem

# Page Configuration for Premium Feel
st.set_page_config(
    page_title="TruthLens - AI Agent Hoax Detector",
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
        background-color: #1f2937; # Dark card bg
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .agent-step {
        border-left: 2px solid #00c0f0;
        padding-left: 10px;
        margin-bottom: 10px;
        color: #a0a0a0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Fuzzy System for Plotting (Local Instance)
@st.cache_resource
def load_fuzzy():
    return FuzzySystem()

fuzzy_viz = load_fuzzy()

# Sidebar
with st.sidebar:
    st.title("🛡️ TruthLens Agent")
    st.caption("v2.0 - LangGraph Enhanced")
    st.markdown("---")
    
    st.warning("🔑 API Keys Required for Agent")
    openrouter_key = st.text_input("OpenRouter API Key (DeepSeek)", type="password", help="Required for reasoning. (Auto-filled from .env if available)")
    tavily_key = st.text_input("Tavily API Key", type="password", help="Required for internet search. (Optional, falls back to DDG but less effective)")
    
    if openrouter_key:
        os.environ["OPENROUTER_API_KEY"] = openrouter_key
    elif os.environ.get("OPENROUTER_API_KEY"):
        st.success("✅ DeepSeek API Key Detected")
        
    if tavily_key:
        os.environ["TAVILY_API_KEY"] = tavily_key
        
    st.markdown("---")
    st.info("**Mode Agen Cerdas**\nMengkombinasikan *Fuzzy Logic* dengan *Pencarian Internet* untuk verifikasi fakta mendalam.")
    st.caption("© 2026 Tugas KB IF504")

# Main Content
col1, col2 = st.columns([2, 1])

show_fuzzy_result = False

with col1:
    st.title("Deteksi Kebenaran Berita")
    st.markdown("##### *Agentic Verification System*")
    
    input_text = st.text_area("Masukkan Judul Berita:", height=100, placeholder="Contoh: MENGEJUTKAN!! Babi Ngepet Ditemukan di Depok...")

    if st.button("🔍 JALANKAN AGEN"):
        if not os.environ.get("OPENROUTER_API_KEY"):
            st.error("⚠️ OpenRouter API Key is missing. Please enter it in the sidebar.")
        elif input_text:
            with st.status('🤖 Agent sedang bekerja...', expanded=True) as status:
                st.write("1️⃣  **Verifier**: Searching Internet for facts...")
                # Run the graph
                try:
                    inputs = {"news_text": input_text}
                    result = graph.invoke(inputs)
                    
                    st.write("2️⃣  **Analyst**: Calculating Fuzzy Logic Score...")
                    # Extract fuzzy data from agent result
                    fuzzy_data = result.get('fuzzy_assessment', {})
                    caps_val = fuzzy_data.get('caps_ratio_percent', 0)
                    prov_val = fuzzy_data.get('provocative_score_raw', 0)
                    
                    # Update local fuzzy instance for visualization
                    score, label = fuzzy_viz.calculate(caps_val, prov_val)
                    show_fuzzy_result = True
                    
                    st.write("3️⃣  **Finalizer**: Synthesizing Verdict...")
                    status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
                    
                    # --- RESULTS DISPLAY ---
                    st.markdown("### Kesimpulan Agen")
                    st.write(result.get('final_verdict'))
                    
                    st.markdown("---")
                    
                    # Detailed Metrics
                    st.markdown("#### Faktor Penentu (Analisis Internal)")
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        st.metric("Capslock Ratio", f"{caps_val:.1f}%")
                    with m2:
                        st.metric("Provocative Score", f"{prov_val:.1f}")
                    with m3:
                        st.metric("Hoax Probability", f"{score:.1f}%")

                    # Search Evidence
                    with st.expander("🌐 Lihat Hasil Pencarian Internet"):
                        st.code(result.get('search_results', 'No results'), language="text")

                except Exception as e:
                     st.error(f"Agent Error: {str(e)}")

        else:
            st.error("Mohon masukkan teks berita terlebih dahulu.")

with col2:
    st.header("📊 Visualisasi Fuzzy")
    if show_fuzzy_result:
        st.success("Grafik Menampilkan Posisi Input")
    else:
        st.info("Grafik Fungsi Keanggotaan (Statis)")
    
    # Show plots
    figs = fuzzy_viz.get_plots(show_result=show_fuzzy_result)
    for fig in figs:
        st.pyplot(fig)

