import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from modules.ui_theme import render_hero_banner, render_kpi
from modules.cluster_info import EVAL_EMBEDDING_DATA, TFIDF_EXPERIMENTS

def show(df: pd.DataFrame):
    render_hero_banner(
        title="Evaluasi Kinerja Model & Pemilihan Klaster",
        subtitle="Analisis Silhouette Score, perbandingan representasi leksikal TF-IDF vs semantik Sentence Transformers, dan justifikasi pemilihan k=10.",
        tag="Model Evaluation"
    )
    
    # 1. Metrik Utama Evaluasi
    e_col1, e_col2, e_col3, e_col4 = st.columns(4)
    with e_col1:
        render_kpi("Total Data Ulasan", "11.713", "Sampel evaluasi: 3.000 titik", "#3B82F6")
    with e_col2:
        render_kpi("Silhouette k=10 (Final)", "0.0831", "Inertia: 7.016,81 (Dipilih)", "#10B981")
    with e_col3:
        render_kpi("Silhouette k=2 (Tertinggi)", "0.1280", "Inertia: 8.282,58", "#8B5CF6")
    with e_col4:
        render_kpi("Dimensi Vektor", "384 dense", "paraphrase-multilingual", "#F59E0B")
        
    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
    
    # 2. Grafik Silhouette Score (Sesuai Gambar 3 Laporan)
    st.markdown("### 📈 Grafik Evaluasi Silhouette Score terhadap Jumlah Klaster (k)")
    st.caption("Perbandingan kurva Silhouette Score pada representasi Sentence Transformers (k=2 s/d 10) dan garis pembanding representasi TF-IDF.")
    
    eval_df = pd.DataFrame(EVAL_EMBEDDING_DATA)
    
    fig_eval = go.Figure()
    
    # Trace Sentence Transformers
    fig_eval.add_trace(go.Scatter(
        x=eval_df['k'],
        y=eval_df['silhouette'],
        mode='lines+markers+text',
        name='Sentence Transformers (MiniLM-L12)',
        line=dict(color='#2563EB', width=3),
        marker=dict(size=9, color='#1E40AF'),
        text=[f"{val:.4f}" for val in eval_df['silhouette']],
        textposition='top right',
        hovertemplate="<b>Sentence Transformers</b><br>k: %{x}<br>Silhouette: %{y:.4f}<extra></extra>"
    ))
    
    # Sorot k=2 (tertinggi) dan k=10 (terpilih)
    fig_eval.add_trace(go.Scatter(
        x=[2],
        y=[0.1280],
        mode='markers',
        name='k=2 (Skor Tertinggi)',
        marker=dict(size=14, color='#10B981', symbol='star')
    ))
    
    fig_eval.add_trace(go.Scatter(
        x=[10],
        y=[0.0831],
        mode='markers',
        name='k=10 (Model Final Terpilih)',
        marker=dict(size=14, color='#EF4444', symbol='diamond')
    ))
    
    # Garis acuan TF-IDF tertinggi (~0.0148)
    fig_eval.add_hline(
        y=0.0148,
        line_dash="dot",
        line_color="#DC2626",
        annotation_text="Batas Atas TF-IDF Konfigurasi C (0.0148)",
        annotation_position="bottom right"
    )
    
    fig_eval.update_layout(
        margin=dict(l=20, r=20, t=30, b=40),
        height=400,
        xaxis=dict(title="Jumlah Klaster (k)", dtick=1, range=[1.5, 10.5]),
        yaxis=dict(title="Silhouette Score (Cosine)", range=[0, 0.15]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_eval, use_container_width=True)
    
    # 3. Tabel Detail Hasil Evaluasi (Tabel 6 Laporan)
    st.markdown("### 📋 Tabel Evaluasi K-Means pada Embedding Semantik (Tabel 6 Laporan)")
    
    display_eval_table = eval_df.copy()
    display_eval_table['Status'] = display_eval_table.apply(
        lambda row: "⭐ Skor Tertinggi" if row['is_best_silhouette'] else ("🎯 Konfigurasi Final Terpilih" if row['is_selected'] else "-"),
        axis=1
    )
    display_eval_table = display_eval_table[[
        'k', 'silhouette', 'inertia', 'cluster_terbesar', 'cluster_terkecil', 'Status'
    ]]
    display_eval_table.columns = [
        'Jumlah Klaster (k)', 'Silhouette Score (Cosine)', 'Inertia',
        'Ukuran Klaster Terbesar', 'Ukuran Klaster Terkecil', 'Keterangan'
    ]
    display_eval_table['Silhouette Score (Cosine)'] = display_eval_table['Silhouette Score (Cosine)'].apply(lambda x: f"{x:.4f}")
    display_eval_table['Inertia'] = display_eval_table['Inertia'].apply(lambda x: f"{x:,.2f}")
    display_eval_table['Ukuran Klaster Terbesar'] = display_eval_table['Ukuran Klaster Terbesar'].apply(lambda x: f"{x:,}")
    display_eval_table['Ukuran Klaster Terkecil'] = display_eval_table['Ukuran Klaster Terkecil'].apply(lambda x: f"{x:,}")
    
    st.dataframe(display_eval_table, use_container_width=True, hide_index=True)
    
    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
    
    # 4. Pembahasan Ilmiah: Mengapa Memilih k=10 daripada k=2?
    st.markdown("### 🧠 Mengapa Memilih k=10 jika Silhouette Score Tertinggi Ada pada k=2?")
    
    col_j1, col_j2 = st.columns(2)
    with col_j1:
        st.info("""
        **1. Karakteristik Skor pada k=2 (0.1280):**
        - Secara metrik geometri Silhouette, membagi dataset menjadi hanya 2 kelompok menghasilkan pemisahan jarak yang paling tegas.
        - Namun, 2 klaster hanya membelah data menjadi kelompok sangat makro (misal: "Ulasan Positif" vs "Ulasan Negatif/Keluhan").
        - **Kelemahan k=2:** Tidak memberikan nilai tambah praktis bagi tim pengembang aplikasi karena tema-tema spesifik (seperti bug notifikasi, crash update, masalah sinkronisasi kalender, dan friksi langganan) tercampur baur menjadi satu.
        """)
    with col_j2:
        st.success("""
        **2. Justifikasi Pemilihan k=10 (0.0831):**
        - Nilai k=10 dipilih sebagai **kompromi metodologis yang disengaja** antara keterpisahan klaster yang wajar dan kedalaman eksplorasi tematik.
        - Pada k=10, skor Silhouette (0.0831) sedikit meningkat kembali setelah titik terendah pada k=5 (0.0753).
        - Yang terpenting, k=10 berhasil memecah topik ke dalam tema operasional yang jelas:
          *(1) Penilaian umum, (2) Masalah teknis/crash, (3) Model langganan, (4) Fitur task list, (5) Kemudahan pemakaian, (6) Akun/login/sinkronisasi, (7) Notifikasi/alarm, (8) Pujian singkat, (9) Testimoni umum, dan (10) Sinkronisasi kalender/iklan.*
        """)
        
    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
    
    # 5. Komparasi Eksperimen TF-IDF vs Sentence Transformers (Tabel 4 Laporan)
    st.markdown("### 🔬 Komparasi Eksperimen Representasi Teks: TF-IDF vs Sentence Transformers")
    st.caption("Penelitian melakukan 3 konfigurasi eksperimen TF-IDF sebelum beralih ke representasi embedding semantik modern.")
    
    for exp in TFIDF_EXPERIMENTS:
        is_final = "Sentence Transformers" in exp['konfigurasi']
        border_col = "#10B981" if is_final else "#CBD5E1"
        badge_bg = "#DCFCE7" if is_final else "#F1F5F9"
        badge_text = "#15803D" if is_final else "#475569"
        
        st.markdown(f"""
        <div style="background: white; border: 1px solid {border_col}; border-left: 5px solid {border_col}; border-radius: 10px; padding: 1.1rem; margin-bottom: 0.9rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                <span style="font-weight: 700; font-size: 1.05rem; color: #0F172A;">{exp['konfigurasi']}</span>
                <span style="background: {badge_bg}; color: {badge_text}; font-weight: 700; font-size: 0.75rem; padding: 0.2rem 0.55rem; border-radius: 6px;">
                    Matriks: {exp['matriks']}
                </span>
            </div>
            <div style="font-size: 0.85rem; color: #475569; margin-bottom: 0.4rem;">
                <b>Parameter Fitur:</b> {exp['fitur']} | <b>Rentang k:</b> {exp['k_diuji']}
            </div>
            <div style="font-size: 0.85rem; color: #334155; margin-bottom: 0.4rem;">
                <b>Hasil Evaluasi:</b> Silhouette: <code>{exp['silhouette_range']}</code> | Klaster Terbesar: <code>{exp['cluster_terbesar']}</code>
            </div>
            <div style="font-size: 0.82rem; color: #64748B; font-style: italic;">
                💡 {exp['catatan']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.caption("""
    *Kesimpulan Evaluasi: Pendekatan berbasis leksikal (TF-IDF) mengalami masalah 'curse of dimensionality' dan dominasi klaster raksasa (>60%) akibat keterbatasan menangani sinonim dan variasi sintaksis. Sentence Transformers mentransformasi teks ke dalam ruang semantik berdimensi padat (384), menghasilkan peningkatan Silhouette 5-10x lipat dan persebaran klaster yang proporsional.*
    """)
