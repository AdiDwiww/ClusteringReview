import streamlit as st
import pandas as pd
from modules.ui_theme import apply_custom_css
from modules.data_loader import load_dataset
from modules.icons import icon_svg
from modules import (
    page_overview,
    page_cluster_explorer,
    page_evaluation,
    page_about
)

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Clustering Review Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Terapkan Desain CSS Kustom
apply_custom_css()

# 3. Sidebar Navigasi & Branding Workspace AI SaaS
with st.sidebar:
    # Workspace Brand Header
    logo_svg = icon_svg("brain-circuit", size=22, color="#4F46E5", stroke_width=2.2)
    st.markdown(f"""
    <div style="padding: 0.25rem 0 1.25rem 0; border-bottom: 1px solid #E4E4E7; margin-bottom: 1.25rem;">
        <div style="display: flex; align-items: center; gap: 0.65rem;">
            <div style="width: 36px; height: 36px; border-radius: 8px; background: #EEF2FF; border: 1px solid #C7D2FE; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                {logo_svg}
            </div>
            <div>
                <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.05rem; font-weight: 700; color: #09090B; letter-spacing: -0.02em; line-height: 1.2;">
                    Clustering Review
                </div>
                <div style="font-size: 0.72rem; color: #71717A; font-weight: 500;">
                    Academic Dashboard
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Menu Navigasi 4 Halaman Utama (Tanpa Emoji)
    menu_options = [
        "Overview",
        "Eksplorasi Cluster",
        "Evaluasi Model",
        "Tentang Penelitian"
    ]
    
    st.markdown("""
    <div style="font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #A1A1AA; margin-bottom: 0.5rem; padding-left: 0.25rem;">
        Workspace Menu
    </div>
    """, unsafe_allow_html=True)
    
    selected_page = st.radio(
        "Workspace Menu",
        menu_options,
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    
    # Ringkasan Proyek di Sidebar
    server_icon = icon_svg("cpu", size=13, color="#71717A")
    db_icon = icon_svg("database", size=13, color="#71717A")
    layers_icon = icon_svg("layers", size=13, color="#71717A")
    target_icon = icon_svg("target", size=13, color="#71717A")
    
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E4E4E7; border-radius: 10px; padding: 0.85rem; font-size: 0.78rem; color: #52525B; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
        <div style="font-weight: 700; color: #09090B; font-size: 0.8rem; margin-bottom: 0.6rem; display: flex; align-items: center; justify-content: space-between;">
            <span>System Pipeline</span>
            <span style="display: inline-flex; align-items: center; gap: 0.25rem; font-size: 0.7rem; color: #059669; font-weight: 600;">
                <span style="width: 6px; height: 6px; border-radius: 50%; background: #10B981; display: inline-block;"></span> Active
            </span>
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.4rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #71717A; display: flex; align-items: center; gap: 0.35rem;">{db_icon} Dataset:</span>
                <span style="font-weight: 600; color: #09090B; font-family: 'JetBrains Mono', monospace;">11.713 baris</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #71717A; display: flex; align-items: center; gap: 0.35rem;">{server_icon} Model:</span>
                <span style="font-weight: 600; color: #09090B;">MiniLM-L12</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #71717A; display: flex; align-items: center; gap: 0.35rem;">{layers_icon} Klaster:</span>
                <span style="font-weight: 600; color: #09090B; font-family: 'JetBrains Mono', monospace;">k = 10</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #71717A; display: flex; align-items: center; gap: 0.35rem;">{target_icon} Silhouette:</span>
                <span style="font-weight: 600; color: #4F46E5; font-family: 'JetBrains Mono', monospace;">0.0831</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# 4. Pemuatan Data dengan Penanganan Error Kuat
try:
    df = load_dataset("hasil_clustering_semantik_k10.csv")
except FileNotFoundError:
    alert_icon = icon_svg("alert-triangle", size=18, color="#DC2626")
    st.markdown(f"""
    <div style="background: #FEF2F2; border: 1px solid #FCA5A5; border-radius: 8px; padding: 1rem; color: #991B1B;">
        <div style="font-weight: 700; margin-bottom: 0.25rem;">File Dataset Tidak Ditemukan</div>
        <div style="font-size: 0.85rem;">Pastikan file <code>hasil_clustering_semantik_k10.csv</code> berada di folder utama proyek.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()
except Exception as e:
    st.markdown(f"""
    <div style="background: #FEF2F2; border: 1px solid #FCA5A5; border-radius: 8px; padding: 1rem; color: #991B1B;">
        <div style="font-weight: 700; margin-bottom: 0.25rem;">Kesalahan Saat Memuat Dataset</div>
        <div style="font-size: 0.85rem;">{str(e)}</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# 5. Routing 4 Halaman Utama
if selected_page == "Overview":
    page_overview.show(df)
elif selected_page == "Eksplorasi Cluster":
    page_cluster_explorer.show(df)
elif selected_page == "Evaluasi Model":
    page_evaluation.show(df)
elif selected_page == "Tentang Penelitian":
    page_about.show(df)

# 6. Footer Konsisten Minimalis
st.markdown("""
<div style="margin-top: 3.5rem; padding: 1.5rem 0; border-top: 1px solid #E4E4E7; text-align: center; font-size: 0.78rem; color: #71717A;">
    <span>Sentence Transformers (384d) &amp; K-Means (k=10)</span>
</div>
""", unsafe_allow_html=True)
