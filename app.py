import streamlit as st
import pandas as pd
from modules.ui_theme import apply_custom_css
from modules.data_loader import load_dataset
from modules import (
    page_overview,
    page_dataset,
    page_cluster_explorer,
    page_visualizations,
    page_test_review,
    page_evaluation,
    page_about
)

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Clustering Ulasan Aplikasi Produktivitas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Terapkan Desain CSS Kustom
apply_custom_css()

# 3. Sidebar Navigasi & Informasi Proyek
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1rem 0;">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
            <span style="font-size: 1.6rem;">📊</span>
            <span style="font-size: 1.15rem; font-weight: 800; color: #0F172A; letter-spacing: -0.01em;">ReviewCluster</span>
        </div>
        <div style="font-size: 0.78rem; color: #64748B; font-weight: 500;">
            Sentence Transformers & K-Means
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Menu Navigasi 7 Halaman
    menu_options = [
        "📊 Dashboard Overview",
        "🔍 Eksplorasi Dataset",
        "🧩 Cluster Explorer",
        "📈 Visualisasi Interaktif",
        "🚀 Uji Ulasan Baru",
        "⚖️ Evaluasi Model",
        "📖 Tentang Penelitian"
    ]
    
    selected_page = st.radio(
        "NAVIGASI UTAMA",
        menu_options,
        index=0,
        label_visibility="visible"
    )
    
    st.markdown("---")
    
    # Ringkasan Proyek di Sidebar
    st.markdown("""
    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.85rem; font-size: 0.8rem; color: #475569;">
        <div style="font-weight: 700; color: #0F172A; margin-bottom: 0.4rem;">📌 Parameter Riset</div>
        <div>• <b>Dataset:</b> 11.713 Ulasan</div>
        <div>• <b>Aplikasi:</b> 15 Aplikasi</div>
        <div>• <b>Model:</b> MiniLM-L12 (384d)</div>
        <div>• <b>Klaster:</b> K-Means (k=10)</div>
        <div>• <b>Silhouette:</b> 0.0831 (k=10)</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.caption("Proyek Penelitian Data Science • Streamlit v1.66+")

# 4. Pemuatan Data dengan Penanganan Error Kuat
try:
    df = load_dataset("hasil_clustering_semantik_k10.csv")
except FileNotFoundError:
    st.error("""
    ❌ **File Dataset Tidak Ditemukan**
    Pastikan file `hasil_clustering_semantik_k10.csv` berada di folder utama proyek.
    """)
    st.stop()
except Exception as e:
    st.error(f"""
    ❌ **Terjadi Kesalahan Saat Memuat Dataset**
    Keterangan error: {str(e)}
    """)
    st.stop()

# 5. Routing Halaman
if selected_page == "📊 Dashboard Overview":
    page_overview.show(df)
elif selected_page == "🔍 Eksplorasi Dataset":
    page_dataset.show(df)
elif selected_page == "🧩 Cluster Explorer":
    page_cluster_explorer.show(df)
elif selected_page == "📈 Visualisasi Interaktif":
    page_visualizations.show(df)
elif selected_page == "🚀 Uji Ulasan Baru":
    page_test_review.show(df)
elif selected_page == "⚖️ Evaluasi Model":
    page_evaluation.show(df)
elif selected_page == "📖 Tentang Penelitian":
    page_about.show(df)

# 6. Footer Konsisten
st.markdown("""
<div style="margin-top: 3.5rem; padding-top: 1.25rem; border-top: 1px solid #E2E8F0; text-align: center; font-size: 0.8rem; color: #94A3B8;">
    Clustering Ulasan Aplikasi Produktivitas di Google Play Store • Sentence Transformers & K-Means (k=10)
</div>
""", unsafe_allow_html=True)
