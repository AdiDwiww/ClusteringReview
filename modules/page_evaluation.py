import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from modules.ui_theme import render_workspace_header, render_kpi, render_section_title
from modules.cluster_info import EVAL_EMBEDDING_DATA, TFIDF_EXPERIMENTS
from modules.icons import icon_svg

def show(df: pd.DataFrame):
    render_workspace_header(
        title="Evaluasi Kinerja & Pemilihan Klaster",
        subtitle="Analisis koefisien Silhouette, komparasi representasi leksikal TF-IDF vs semantik Sentence Transformers, dan dasar pemilihan k=10.",
        category="Model Evaluation",
        icon="activity"
    )
    
    # 1. Metrik Utama Evaluasi (Zero Emojis)
    e_col1, e_col2, e_col3, e_col4 = st.columns(4)
    with e_col1:
        render_kpi("Total Data Evaluasi", "11.713", "Sampel evaluasi: 3.000 titik", "database", "#4F46E5")
    with e_col2:
        render_kpi("Silhouette k=10 (Final)", "0.0831", "Inertia: 7.016,81 (Dipilih)", "target", "#059669")
    with e_col3:
        render_kpi("Silhouette k=2 (Puncak)", "0.1280", "Inertia: 8.282,58", "trending-up", "#7C3AED")
    with e_col4:
        render_kpi("Dimensi Vektor", "384 dense", "paraphrase-multilingual", "cpu", "#D97706")
        
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    
    # 2. Grafik Silhouette Score (Sesuai Gambar 3 Laporan)
    render_section_title("Evaluasi Silhouette Score terhadap Jumlah Klaster (k)", "Kurva Silhouette Score pada representasi Sentence Transformers (k=2 s/d 10) terhadap batas atas representasi TF-IDF.", icon="bar-chart-3")
    
    eval_df = pd.DataFrame(EVAL_EMBEDDING_DATA)
    
    fig_eval = go.Figure()
    
    fig_eval.add_trace(go.Scatter(
        x=eval_df['k'],
        y=eval_df['silhouette'],
        mode='lines+markers+text',
        name='Sentence Transformers (MiniLM-L12)',
        line=dict(color='#4F46E5', width=2.5),
        marker=dict(size=8, color='#3730A3'),
        text=[f"{val:.4f}" for val in eval_df['silhouette']],
        textposition='top right',
        textfont=dict(size=10, family="JetBrains Mono"),
        hovertemplate="<b>Sentence Transformers</b><br>k: %{x}<br>Silhouette: %{y:.4f}<extra></extra>"
    ))
    
    fig_eval.add_trace(go.Scatter(
        x=[2],
        y=[0.1280],
        mode='markers',
        name='k=2 (Nilai Tertinggi)',
        marker=dict(size=12, color='#059669', symbol='circle')
    ))
    
    fig_eval.add_trace(go.Scatter(
        x=[10],
        y=[0.0831],
        mode='markers',
        name='k=10 (Konfigurasi Terpilih)',
        marker=dict(size=12, color='#DC2626', symbol='diamond')
    ))
    
    fig_eval.add_hline(
        y=0.0148,
        line_dash="dot",
        line_color="#71717A",
        annotation_text="Batas Atas TF-IDF Konfigurasi C (0.0148)",
        annotation_position="bottom right",
        annotation_font=dict(size=10, color="#71717A")
    )
    
    fig_eval.update_layout(
        margin=dict(l=10, r=10, t=20, b=30),
        height=380,
        xaxis=dict(title="Jumlah Klaster (k)", dtick=1, range=[1.5, 10.5], showgrid=True, gridcolor='#F4F4F5', tickfont=dict(size=11, color='#71717A')),
        yaxis=dict(title="Silhouette Score (Cosine)", range=[0, 0.15], showgrid=True, gridcolor='#F4F4F5', tickfont=dict(size=11, color='#71717A')),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11, color='#71717A')),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", size=11)
    )
    st.plotly_chart(fig_eval, use_container_width=True)
    
    # 3. Tabel Detail Hasil Evaluasi (Tabel 6 Laporan)
    render_section_title("Tabel Evaluasi K-Means pada Embedding Semantik", "Data kuantitatif evaluasi K-Means dari keluaran notebook dan Tabel 6 laporan penelitian.", icon="database")
    
    display_eval_table = eval_df.copy()
    display_eval_table['Status'] = display_eval_table.apply(
        lambda row: "Skor Tertinggi" if row['is_best_silhouette'] else ("Model Final Terpilih" if row['is_selected'] else "-"),
        axis=1
    )
    display_eval_table = display_eval_table[[
        'k', 'silhouette', 'inertia', 'cluster_terbesar', 'cluster_terkecil', 'Status'
    ]]
    display_eval_table.columns = [
        'Jumlah Klaster (k)', 'Silhouette (Cosine)', 'Inertia',
        'Ukuran Klaster Terbesar', 'Ukuran Klaster Terkecil', 'Keterangan'
    ]
    display_eval_table['Silhouette (Cosine)'] = display_eval_table['Silhouette (Cosine)'].apply(lambda x: f"{x:.4f}")
    display_eval_table['Inertia'] = display_eval_table['Inertia'].apply(lambda x: f"{x:,.2f}")
    display_eval_table['Ukuran Klaster Terbesar'] = display_eval_table['Ukuran Klaster Terbesar'].apply(lambda x: f"{x:,}")
    display_eval_table['Ukuran Klaster Terkecil'] = display_eval_table['Ukuran Klaster Terkecil'].apply(lambda x: f"{x:,}")
    
    st.dataframe(display_eval_table, hide_index=True, use_container_width=True)
    
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    
    # 4. Pembahasan Ilmiah: Mengapa Memilih k=10 daripada k=2?
    render_section_title("Justifikasi Pemilihan k=10 terhadap k=2", "Penjelasan pertimbangan metodologis antara keterpisahan geometris dan kedalaman analitis.", icon="info")
    
    col_j1, col_j2 = st.columns(2)
    with col_j1:
        st.markdown("""
        <div class="saas-card" style="height: 100%;">
            <div style="font-weight: 700; color: #09090B; font-size: 0.95rem; margin-bottom: 0.5rem;">
                Karakteristik Skor pada k = 2 (0.1280)
            </div>
            <ul style="font-size: 0.85rem; color: #3F3F46; line-height: 1.6; padding-left: 1.15rem; margin: 0;">
                <li style="margin-bottom: 0.45rem;">
                    Secara metrik geometri Silhouette, pembagian dataset menjadi 2 kelompok menghasilkan rasio jarak antar-klaster tertinggi.
                </li>
                <li style="margin-bottom: 0.45rem;">
                    Namun, 2 klaster hanya membelah data secara biner/makro (ulasan positif umum vs ulasan negatif teknis).
                </li>
                <li>
                    <b>Keterbatasan:</b> Pengelompokan ini tidak memberikan insight operasional yang dapat ditindaklanjuti oleh pengembang produk karena masalah spesifik (seperti sinkronisasi akun, bug pembaruan, dan notifikasi alarm) tercampur menjadi satu.
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_j2:
        st.markdown("""
        <div class="saas-card" style="height: 100%;">
            <div style="font-weight: 700; color: #09090B; font-size: 0.95rem; margin-bottom: 0.5rem;">
                Justifikasi Pemilihan k = 10 (0.0831)
            </div>
            <ul style="font-size: 0.85rem; color: #3F3F46; line-height: 1.6; padding-left: 1.15rem; margin: 0;">
                <li style="margin-bottom: 0.45rem;">
                    Dipilih sebagai <b>kompromi metodologis yang disengaja</b> antara keterpisahan klaster yang wajar dan resolusi tema yang detail.
                </li>
                <li style="margin-bottom: 0.45rem;">
                    Pada k=10, kurva Silhouette (0.0831) mengalami rebound positif setelah titik terendah pada k=5 (0.0753).
                </li>
                <li>
                    <b>Hasil:</b> Berhasil mengidentifikasi 10 tema terarah: masalah teknis/crash, friksi versi pro, manajemen tugas, kemudahan pemakaian, krisis akun/sync, alarm/pengingat, ulasan apresiasi singkat, kepuasan umum, dan sinkronisasi agenda kalender.
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    
    # 5. Komparasi Eksperimen TF-IDF vs Sentence Transformers
    render_section_title("Komparasi Eksperimen: TF-IDF vs Sentence Transformers", "Perbandingan hasil 3 konfigurasi leksikal terhadap representasi embedding semantik (Tabel 4 Laporan).", icon="layers")
    
    for exp in TFIDF_EXPERIMENTS:
        is_final = "Sentence Transformers" in exp['konfigurasi']
        border_col = "#4F46E5" if is_final else "#E4E4E7"
        badge_bg = "#EEF2FF" if is_final else "#F4F4F5"
        badge_text = "#4338CA" if is_final else "#52525B"
        
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid {border_col}; border-left: 3px solid {border_col}; border-radius: 8px; padding: 1rem 1.15rem; margin-bottom: 0.8rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                <span style="font-weight: 700; font-size: 0.95rem; color: #09090B;">{exp['konfigurasi']}</span>
                <span style="background: {badge_bg}; color: {badge_text}; font-weight: 600; font-size: 0.74rem; padding: 0.15rem 0.5rem; border-radius: 4px; font-family: 'JetBrains Mono', monospace;">
                    {exp['matriks']}
                </span>
            </div>
            <div style="font-size: 0.82rem; color: #52525B; margin-bottom: 0.3rem;">
                <b>Parameter:</b> {exp['fitur']} | <b>Rentang k:</b> {exp['k_diuji']}
            </div>
            <div style="font-size: 0.82rem; color: #27272A; margin-bottom: 0.3rem; font-family: 'JetBrains Mono', monospace;">
                Silhouette: <b>{exp['silhouette_range']}</b> | Klaster Terbesar: <b>{exp['cluster_terbesar']}</b>
            </div>
            <div style="font-size: 0.8rem; color: #71717A; line-height: 1.5;">
                {exp['catatan']}
            </div>
        </div>
        """, unsafe_allow_html=True)
