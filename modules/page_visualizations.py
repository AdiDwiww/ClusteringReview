import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from modules.ui_theme import render_hero_banner
from modules.cluster_info import CLUSTER_METADATA, APP_NAME_MAP
from modules.data_loader import load_pca_coordinates

def show(df: pd.DataFrame):
    render_hero_banner(
        title="Visualisasi Interaktif & Analisis Multidimensi",
        subtitle="Eksplorasi grafis komparasi klaster, perbandingan rating aplikasi, distribusi skor bertingkat, dan proyeksi reduksi dimensi 2D PCA.",
        tag="Interactive Visualizations"
    )
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Distribusi Klaster & Rating",
        "📱 Komparasi 15 Aplikasi",
        "🎯 Proyeksi Reduksi Dimensi 2D (PCA)",
        "📦 Boxplot Distribusi Skor"
    ])
    
    # ---------------- TAB 1: DISTRIBUSI KLASTER & RATING ----------------
    with tab1:
        st.markdown("### 1. Bar Chart: Jumlah Ulasan per Klaster")
        
        c_counts = df.groupby('cluster_semantik_10').size().reset_index(name='Jumlah Ulasan')
        c_counts['Klaster'] = c_counts['cluster_semantik_10'].apply(
            lambda x: f"C{x}: {CLUSTER_METADATA.get(x, {}).get('name', '')}"
        )
        c_counts['Persentase'] = (c_counts['Jumlah Ulasan'] / len(df) * 100).round(1)
        c_counts['Warna'] = c_counts['cluster_semantik_10'].apply(
            lambda x: CLUSTER_METADATA.get(x, {}).get('warna', '#3B82F6')
        )
        c_counts = c_counts.sort_values('Jumlah Ulasan', ascending=True)
        
        fig_bar_count = go.Figure(data=[
            go.Bar(
                y=c_counts['Klaster'],
                x=c_counts['Jumlah Ulasan'],
                orientation='h',
                text=[f"{n:,} ({p}%)" for n, p in zip(c_counts['Jumlah Ulasan'], c_counts['Persentase'])],
                textposition='outside',
                marker=dict(color=c_counts['Warna'].tolist())
            )
        ])
        fig_bar_count.update_layout(
            margin=dict(l=10, r=40, t=10, b=10),
            height=360,
            xaxis_title="Jumlah Ulasan",
            yaxis_title="",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_bar_count, use_container_width=True)
        
        st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
        
        st.markdown("### 2. Stacked Bar Chart: Komposisi Rating per Klaster")
        st.caption("Memvisualisasikan proporsi rating 1 hingga 5 pada setiap klaster untuk melihat struktur kepuasan vs keluhan.")
        
        stacked_data = df.groupby(['cluster_semantik_10', 'score']).size().unstack(fill_value=0)
        # Hitung persentase baris
        stacked_pct = stacked_data.div(stacked_data.sum(axis=1), axis=0) * 100
        
        rating_colors = {
            1: '#EF4444', # Merah
            2: '#F97316', # Oranye
            3: '#FBBF24', # Kuning
            4: '#34D399', # Hijau Muda
            5: '#10B981'  # Hijau Tua
        }
        
        fig_stacked = go.Figure()
        cluster_labels = [f"C{i} - {CLUSTER_METADATA[i]['name'][:15]}" for i in range(10)]
        
        for r in range(1, 6):
            fig_stacked.add_trace(go.Bar(
                name=f"Rating {r} ★",
                x=cluster_labels,
                y=stacked_pct[r].round(1),
                marker_color=rating_colors[r],
                text=[f"{val:.0f}%" if val > 5 else "" for val in stacked_pct[r]],
                textposition='inside',
                hovertemplate="<b>%{x}</b><br>Rating " + str(r) + "★: %{y:.1f}%<extra></extra>"
            ))
            
        fig_stacked.update_layout(
            barmode='stack',
            margin=dict(l=10, r=10, t=20, b=50),
            height=380,
            xaxis_tickangle=-25,
            yaxis=dict(title="Persentase (%)", range=[0, 100]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_stacked, use_container_width=True)
        
    # ---------------- TAB 2: KOMPARASI 15 APLIKASI ----------------
    with tab2:
        st.markdown("### 📱 Perbandingan Jumlah Ulasan & Rata-rata Rating antar Aplikasi")
        
        app_stats = df.groupby('app_name').agg(
            total_ulasan=('content', 'count'),
            mean_score=('score', 'mean'),
            pct_low=('score', lambda x: (x <= 2).mean() * 100),
            pct_high=('score', lambda x: (x >= 4).mean() * 100)
        ).reset_index().sort_values('mean_score', ascending=False)
        
        col_app1, col_app2 = st.columns([1.2, 1])
        
        with col_app1:
            fig_app_bar = px.bar(
                app_stats,
                x='mean_score',
                y='app_name',
                orientation='h',
                color='mean_score',
                color_continuous_scale='RdYlGn',
                labels={'mean_score': 'Rata-rata Rating', 'app_name': 'Aplikasi'},
                title="Peringkat Rata-rata Rating per Aplikasi"
            )
            fig_app_bar.update_layout(
                margin=dict(l=10, r=10, t=40, b=10),
                height=450,
                yaxis=dict(autorange="reversed"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_app_bar, use_container_width=True)
            
        with col_app2:
            st.markdown("#### Detail Tabel Ulasan per Aplikasi")
            app_display = app_stats.copy()
            app_display.columns = ['Nama Aplikasi', 'Total Ulasan', 'Rata-rata', 'Rating 1-2 (%)', 'Rating 4-5 (%)']
            app_display['Total Ulasan'] = app_display['Total Ulasan'].apply(lambda x: f"{x:,}")
            app_display['Rata-rata'] = app_display['Rata-rata'].round(2).apply(lambda x: f"{x:.2f} ★")
            app_display['Rating 1-2 (%)'] = app_display['Rating 1-2 (%)'].round(1).apply(lambda x: f"{x:.1f}%")
            app_display['Rating 4-5 (%)'] = app_display['Rating 4-5 (%)'].round(1).apply(lambda x: f"{x:.1f}%")
            
            st.dataframe(app_display, use_container_width=True, hide_index=True, height=450)
            
        st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
        
        # Heatmap Sebaran Klaster per Aplikasi
        st.markdown("### 🔥 Sebaran Proporsi Klaster pada Masing-masing Aplikasi")
        st.caption("Menganalisis jenis keluhan atau pujian apa yang paling dominan muncul pada tiap aplikasi.")
        
        app_cluster_cross = pd.crosstab(
            df['app_name'], 
            df['cluster_semantik_10'], 
            normalize='index'
        ) * 100
        app_cluster_cross.columns = [f"C{c}" for c in app_cluster_cross.columns]
        
        fig_heat = px.imshow(
            app_cluster_cross.round(1),
            labels=dict(x="Klaster Semantik", y="Aplikasi", color="% Ulasan"),
            x=app_cluster_cross.columns.tolist(),
            y=app_cluster_cross.index.tolist(),
            color_continuous_scale="Viridis",
            text_auto=True,
            aspect="auto"
        )
        fig_heat.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=460,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        
    # ---------------- TAB 3: PROYEKSI 2D (PCA) ----------------
    with tab3:
        st.markdown("### 🎯 Visualisasi Proyeksi 2D Menggunakan PCA")
        
        st.warning("""
        **Penting (Catatan Metodologi Reduksi Dimensi):**
        Vektor representasi semantik asli berukuran **384 dimensi** (`paraphrase-multilingual-MiniLM-L12-v2`).
        Proyeksi 2 dimensi menggunakan Principal Component Analysis (PCA) ini hanya mempertahankan sekitar **16.4% dari total varians data** (PC1: ~8.9%, PC2: ~7.5%).
        Oleh karena itu, proyeksi 2D **tidak mewakili seluruh geometri ruang embedding asli**, dan adanya tumpang tindih visual (overlap) pada bidang 2D adalah konsekuensi alami dari reduksi dimensi leksikal-semantik.
        """)
        
        pca_coords = load_pca_coordinates()
        
        if pca_coords is not None and len(pca_coords) == len(df):
            plot_df = pd.DataFrame({
                'PC1': pca_coords[:, 0],
                'PC2': pca_coords[:, 1],
                'Cluster': df['cluster_semantik_10'].astype(str),
                'Nama Klaster': df['cluster_semantik_10'].apply(lambda x: f"C{x}: {CLUSTER_METADATA.get(x, {}).get('name', '')}"),
                'Rating': df['score'],
                'Aplikasi': df['app_name'],
                'Cuplikan Ulasan': df['content'].apply(lambda x: str(x)[:80] + "...")
            })
            
            p_col1, p_col2 = st.columns([1, 2])
            with p_col1:
                color_by = st.radio("Warnai Titik Berdasarkan:", ["Klaster Semantik (k=10)", "Rating Skor (1-5)"], horizontal=True)
            with p_col2:
                sample_size = st.slider("Jumlah Titik Sampel (untuk responsivitas grafik):", min_value=1000, max_value=len(df), value=3000, step=1000)
                
            sample_plot = plot_df.sample(n=min(sample_size, len(plot_df)), random_state=42)
            
            if color_by == "Klaster Semantik (k=10)":
                cluster_colors = {str(k): CLUSTER_METADATA[k]['warna'] for k in range(10)}
                fig_pca = px.scatter(
                    sample_plot,
                    x='PC1',
                    y='PC2',
                    color='Cluster',
                    color_discrete_map=cluster_colors,
                    hover_data=['Aplikasi', 'Rating', 'Cuplikan Ulasan', 'Nama Klaster'],
                    title=f"Scatter Plot 2D PCA ({len(sample_plot):,} Sampel Ulasan)"
                )
            else:
                fig_pca = px.scatter(
                    sample_plot,
                    x='PC1',
                    y='PC2',
                    color='Rating',
                    color_continuous_scale='RdYlGn',
                    hover_data=['Aplikasi', 'Nama Klaster', 'Cuplikan Ulasan'],
                    title=f"Scatter Plot 2D PCA Berdasarkan Rating ({len(sample_plot):,} Sampel Ulasan)"
                )
                
            fig_pca.update_traces(marker=dict(size=5, opacity=0.7))
            fig_pca.update_layout(
                margin=dict(l=10, r=10, t=40, b=10),
                height=520,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_pca, use_container_width=True)
        else:
            st.info("Koordinat PCA belum tersedia atau sedang diproses. Silakan jalankan script rekonstruksi.")
            
    # ---------------- TAB 4: BOXPLOT DISTRIBUSI SKOR ----------------
    with tab4:
        st.markdown("### 📦 Boxplot Rating pada Setiap Klaster (Sesuai Gambar 2 Laporan)")
        st.caption("Visualisasi replikasi dari sel terakhir notebook dan Gambar 2 laporan penelitian, menunjukkan rentang kuartil dan median rating per klaster.")
        
        df_box = df.copy()
        df_box['Klaster'] = df_box['cluster_semantik_10'].apply(
            lambda x: f"C{x}\n{CLUSTER_METADATA.get(x, {}).get('name', '')[:12]}"
        )
        
        fig_box = px.box(
            df_box,
            x='cluster_semantik_10',
            y='score',
            color='cluster_semantik_10',
            color_discrete_map={k: CLUSTER_METADATA[k]['warna'] for k in range(10)},
            labels={'cluster_semantik_10': 'ID Klaster (0–9)', 'score': 'Rating (1–5)'},
            title="Sebaran Rating pada Setiap Klaster (Boxplot)"
        )
        fig_box.update_layout(
            margin=dict(l=10, r=10, t=40, b=20),
            height=420,
            showlegend=False,
            yaxis=dict(range=[0.5, 5.5], dtick=1),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_box, use_container_width=True)
        
        st.markdown("""
        **Interpretasi Boxplot (Tinjauan Penelitian):**
        - **Cluster 4, 7, dan 8:** Memiliki median rating **4.0** dengan batas kotak kuartil (interquartile range) berkisar antara rating 4 dan 5.
        - **Cluster 5 (Akun & Sinkronisasi):** Memiliki kotak paling padat di dasar rating 1 hingga 2 (median **2.0**), menegaskan keluhan akut.
        - **Cluster 1, 0, 2, dan 6:** Semuanya berpusat pada rentang rating 1–2 (median **2.0**).
        - **Cluster 3 (Manajemen Tugas):** Memiliki sebaran paling merata dengan median **3.0** (mencakup saran fitur dan review netral).
        """)
