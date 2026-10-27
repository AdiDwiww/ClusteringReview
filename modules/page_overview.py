import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.ui_theme import render_hero_banner, render_kpi
from modules.cluster_info import CLUSTER_METADATA

def show(df: pd.DataFrame):
    render_hero_banner(
        title="Ringkasan Eksekutif & Dashboard Utama",
        subtitle="Analisis clustering semantik ulasan 15 aplikasi produktivitas Google Play Store menggunakan Sentence Transformers & K-Means (k=10).",
        tag="Dashboard Overview"
    )
    
    # 1. KPI Cards
    total_reviews = len(df)
    total_apps = df['appId'].nunique()
    total_clusters = df['cluster_semantik_10'].nunique()
    avg_rating = df['score'].mean()
    pct_negative = (df['score'] <= 2).mean() * 100
    pct_positive = (df['score'] >= 4).mean() * 100
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi("Total Ulasan Bersih", f"{total_reviews:,}", "11.713 ulasan valid", "#3B82F6")
    with col2:
        render_kpi("Aplikasi Dianalisis", f"{total_apps}", "Kategori produktivitas", "#10B981")
    with col3:
        render_kpi("Jumlah Klaster", f"{total_clusters}", "Model final k=10", "#8B5CF6")
    with col4:
        render_kpi("Rata-rata Rating", f"{avg_rating:.2f} / 5.0", f"Positif: {pct_positive:.1f}% | Negatif: {pct_negative:.1f}%", "#F59E0B")
        
    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
    
    # 2. Charts Row 1: Distribusi Rating & Proporsi Cluster
    col_chart1, col_chart2 = st.columns([1, 1])
    
    with col_chart1:
        st.markdown("### 📊 Distribusi Rating Keseluruhan (1–5)")
        rating_counts = df['score'].value_counts().sort_index().reset_index()
        rating_counts.columns = ['Rating', 'Jumlah']
        rating_counts['Persentase'] = (rating_counts['Jumlah'] / total_reviews * 100).round(1)
        rating_counts['Label'] = rating_counts['Rating'].apply(lambda x: f"★ {x}")
        
        # Color scale from red (1) to green (5)
        colors_rating = ['#EF4444', '#F97316', '#FBBF24', '#34D399', '#10B981']
        
        fig_rating = go.Figure(data=[
            go.Bar(
                x=rating_counts['Label'],
                y=rating_counts['Jumlah'],
                text=[f"{count:,}<br>({pct}%)" for count, pct in zip(rating_counts['Jumlah'], rating_counts['Persentase'])],
                textposition='auto',
                marker=dict(
                    color=colors_rating,
                    line=dict(color='#CBD5E1', width=1)
                ),
                hovertemplate="<b>Rating %{x}</b><br>Jumlah: %{y:,} ulasan<br>Persentase: %{text}<extra></extra>"
            )
        ])
        fig_rating.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height=340,
            xaxis_title="Skor Bintang",
            yaxis_title="Jumlah Ulasan",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Plus Jakarta Sans, Inter", size=12)
        )
        st.plotly_chart(fig_rating, use_container_width=True)
        
    with col_chart2:
        st.markdown("### 🧩 Proporsi Ulasan per Klaster (k=10)")
        cluster_summary = df.groupby('cluster_semantik_10').size().reset_index(name='Jumlah')
        cluster_summary['Klaster'] = cluster_summary['cluster_semantik_10'].apply(
            lambda x: f"C{x}: {CLUSTER_METADATA.get(x, {}).get('name', f'Cluster {x}')[:18]}..."
        )
        cluster_summary['Warna'] = cluster_summary['cluster_semantik_10'].apply(
            lambda x: CLUSTER_METADATA.get(x, {}).get('warna', '#6B7280')
        )
        
        fig_donut = go.Figure(data=[
            go.Pie(
                labels=cluster_summary['Klaster'],
                values=cluster_summary['Jumlah'],
                hole=0.45,
                marker=dict(colors=cluster_summary['Warna'].tolist()),
                textinfo='percent+label',
                hovertemplate="<b>%{label}</b><br>Jumlah: %{value:,} ulasan<br>Proporsi: %{percent}<extra></extra>"
            )
        ])
        fig_donut.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=340,
            showlegend=False,
            font=dict(family="Plus Jakarta Sans, Inter", size=11)
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        
    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
    
    # 3. Charts Row 2: Rata-rata Rating per Klaster & Tabel Ringkasan
    st.markdown("### ⚖️ Perbandingan Rata-rata Rating per Klaster")
    st.caption("Memetakan klaster mana yang didominasi keluhan pengguna (rating rendah) dan klaster mana yang memuat kepuasan (rating tinggi).")
    
    cluster_stats = df.groupby('cluster_semantik_10').agg(
        n=('content', 'count'),
        mean_score=('score', 'mean'),
        median_score=('score', 'median'),
        pct_1_2=('score', lambda x: (x <= 2).mean() * 100),
        pct_4_5=('score', lambda x: (x >= 4).mean() * 100)
    ).reset_index()
    
    cluster_stats['Nama Klaster'] = cluster_stats['cluster_semantik_10'].apply(
        lambda x: f"C{x} - {CLUSTER_METADATA.get(x, {}).get('name', f'Cluster {x}')}"
    )
    cluster_stats['Tema Singkat'] = cluster_stats['cluster_semantik_10'].apply(
        lambda x: CLUSTER_METADATA.get(x, {}).get('tema', '')
    )
    cluster_stats['Warna'] = cluster_stats['cluster_semantik_10'].apply(
        lambda x: CLUSTER_METADATA.get(x, {}).get('warna', '#3B82F6')
    )
    cluster_stats = cluster_stats.sort_values('mean_score')
    
    fig_bar_avg = go.Figure(data=[
        go.Bar(
            x=cluster_stats['Nama Klaster'],
            y=cluster_stats['mean_score'].round(2),
            text=[f"{v:.2f} ★" for v in cluster_stats['mean_score']],
            textposition='outside',
            marker=dict(
                color=cluster_stats['Warna'].tolist(),
                line=dict(color='#CBD5E1', width=1)
            ),
            hovertemplate="<b>%{x}</b><br>Rata-rata Rating: %{y:.2f} / 5.0<extra></extra>"
        )
    ])
    fig_bar_avg.add_hline(
        y=avg_rating, 
        line_dash="dash", 
        line_color="#64748B", 
        annotation_text=f"Rata-rata Global ({avg_rating:.2f})",
        annotation_position="bottom right"
    )
    fig_bar_avg.update_layout(
        margin=dict(l=20, r=20, t=30, b=80),
        height=380,
        xaxis_tickangle=-30,
        yaxis=dict(range=[0, 5.2], title="Rata-rata Rating"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Plus Jakarta Sans, Inter", size=11)
    )
    st.plotly_chart(fig_bar_avg, use_container_width=True)
    
    # 4. Ringkasan Insight Nyata Berdasarkan Data Aktual
    st.markdown("### 💡 Ringkasan Insight Analitis Aktual")
    
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        st.info("""
        **1. Klaster Keluhan Kritis (Prioritas Penanganan Developer):**
        - **Cluster 5 (Akun & Sinkronisasi):** Memiliki rata-rata rating terendah (**1.90 / 5.0**) dengan **76.0%** ulasan berating 1–2. Masalah sinkronisasi cloud dan login email menimbulkan resistensi terbesar karena risiko kehilangan data tugas.
        - **Cluster 1 (Masalah Teknis & Bug):** Klaster keluhan terbesar (**1.658 ulasan, 14.2%**) dengan rata-rata rating **2.11**, dipicu oleh crash dan malfungsi setelah aplikasi diperbarui.
        - **Cluster 6 (Notifikasi & Pengingat):** Rata-rata **2.41**; kegagalan alarm tepat waktu merusak proposisi nilai utama aplikasi produktivitas.
        """)
    with col_in2:
        st.success("""
        **2. Klaster Kepuasan & Keunggulan Produk:**
        - **Cluster 8 (Pujian Umum & Rekomendasi):** Merupakan klaster terbesar dalam penelitian (**2.079 ulasan, 17.7%**) dengan rata-rata rating tertinggi (**4.20**; 81.7% rating bintang 4–5).
        - **Cluster 4 (Kemudahan Penggunaan):** Sebanyak **1.207 ulasan (10.3%)** berating rata-rata **4.18**, menegaskan bahwa antarmuka simpel dan kemudahan operasional menjadi pendorong loyalitas pengguna terkuat.
        - **Cluster 3 (Manajemen Tugas):** Rata-rata **3.02** memuat feedback konstruktif dan permintaan fitur integrasi agenda.
        """)
