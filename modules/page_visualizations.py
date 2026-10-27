import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from modules.ui_theme import render_workspace_header, render_section_title
from modules.cluster_info import CLUSTER_METADATA
from modules.data_loader import load_pca_coordinates
from modules.icons import icon_svg

def show(df: pd.DataFrame):
    render_workspace_header(
        title="Visualisasi Multidimensi & Komparasi",
        subtitle="Analisis grafis perbandingan klaster, komparasi performa aplikasi, distribusi skor bertingkat, dan proyeksi reduksi dimensi 2D PCA.",
        category="Data Visualizations",
        icon="bar-chart-3"
    )
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Distribusi Klaster & Rating",
        "Komparasi 15 Aplikasi",
        "Proyeksi Reduksi Dimensi 2D (PCA)",
        "Boxplot Distribusi Skor"
    ])
    
    # ---------------- TAB 1: DISTRIBUSI KLASTER & RATING ----------------
    with tab1:
        render_section_title("Jumlah Ulasan per Klaster", "Ukuran relatif masing-masing kelompok tematik K-Means.", icon="bar-chart-3")
        
        c_counts = df.groupby('cluster_semantik_10').size().reset_index(name='Jumlah Ulasan')
        c_counts['Klaster'] = c_counts['cluster_semantik_10'].apply(
            lambda x: f"C{x}: {CLUSTER_METADATA.get(x, {}).get('name', '')}"
        )
        c_counts['Persentase'] = (c_counts['Jumlah Ulasan'] / len(df) * 100).round(1)
        c_counts['Warna'] = c_counts['cluster_semantik_10'].apply(
            lambda x: CLUSTER_METADATA.get(x, {}).get('warna', '#4F46E5')
        )
        c_counts = c_counts.sort_values('Jumlah Ulasan', ascending=True)
        
        fig_bar_count = go.Figure(data=[
            go.Bar(
                y=c_counts['Klaster'],
                x=c_counts['Jumlah Ulasan'],
                orientation='h',
                text=[f"{n:,} ({p}%)" for n, p in zip(c_counts['Jumlah Ulasan'], c_counts['Persentase'])],
                textposition='outside',
                marker=dict(color=c_counts['Warna'].tolist(), line=dict(color='#E4E4E7', width=1))
            )
        ])
        fig_bar_count.update_layout(
            margin=dict(l=10, r=40, t=10, b=10),
            height=340,
            xaxis=dict(title="Jumlah Ulasan", showgrid=True, gridcolor='#F4F4F5', tickfont=dict(size=11, color='#71717A')),
            yaxis=dict(title="", tickfont=dict(size=11, color='#71717A')),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", size=11)
        )
        st.plotly_chart(fig_bar_count, use_container_width=True)
        
        st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
        
        render_section_title("Komposisi Rating Bertingkat per Klaster", "Proporsi skor rating 1 hingga 5 pada setiap klaster untuk melihat pola keluhan vs kepuasan.", icon="layers")
        
        stacked_data = df.groupby(['cluster_semantik_10', 'score']).size().unstack(fill_value=0)
        stacked_pct = stacked_data.div(stacked_data.sum(axis=1), axis=0) * 100
        
        rating_colors = {
            1: '#EF4444',
            2: '#F97316',
            3: '#EAB308',
            4: '#22C55E',
            5: '#10B981'
        }
        
        fig_stacked = go.Figure()
        cluster_labels = [f"C{i}: {CLUSTER_METADATA[i]['name'][:14]}" for i in range(10)]
        
        for r in range(1, 6):
            fig_stacked.add_trace(go.Bar(
                name=f"Rating {r}",
                x=cluster_labels,
                y=stacked_pct[r].round(1),
                marker_color=rating_colors[r],
                text=[f"{val:.0f}%" if val > 6 else "" for val in stacked_pct[r]],
                textposition='inside',
                hovertemplate="<b>%{x}</b><br>Rating " + str(r) + ": %{y:.1f}%<extra></extra>"
            ))
            
        fig_stacked.update_layout(
            barmode='stack',
            margin=dict(l=10, r=10, t=10, b=60),
            height=360,
            xaxis_tickangle=-25,
            xaxis=dict(tickfont=dict(size=11, color='#71717A')),
            yaxis=dict(title="Persentase (%)", range=[0, 100], showgrid=True, gridcolor='#F4F4F5', tickfont=dict(size=11, color='#71717A')),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11, color='#71717A')),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", size=11)
        )
        st.plotly_chart(fig_stacked, use_container_width=True)
        
    # ---------------- TAB 2: KOMPARASI 15 APLIKASI ----------------
    with tab2:
        render_section_title("Peringkat Rata-rata Rating per Aplikasi", "Perbandingan kepuasan pengguna lintas 15 aplikasi produktivitas.", icon="smartphone")
        
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
                color_continuous_scale='Teal',
                labels={'mean_score': 'Rata-rata Rating', 'app_name': 'Aplikasi'}
            )
            fig_app_bar.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                height=430,
                yaxis=dict(autorange="reversed", tickfont=dict(size=11, color='#71717A')),
                xaxis=dict(showgrid=True, gridcolor='#F4F4F5', tickfont=dict(size=11, color='#71717A')),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", size=11),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_app_bar, use_container_width=True)
            
        with col_app2:
            st.markdown("""
            <div style="font-size: 0.82rem; font-weight: 600; color: #71717A; text-transform: uppercase; margin-bottom: 0.4rem;">
                Tabel Rangkuman Metrik Aplikasi
            </div>
            """, unsafe_allow_html=True)
            app_display = app_stats.copy()
            app_display.columns = ['Nama Aplikasi', 'Total Ulasan', 'Rata-rata', 'Rating 1-2 (%)', 'Rating 4-5 (%)']
            app_display['Total Ulasan'] = app_display['Total Ulasan'].apply(lambda x: f"{x:,}")
            app_display['Rata-rata'] = app_display['Rata-rata'].round(2).apply(lambda x: f"{x:.2f}")
            app_display['Rating 1-2 (%)'] = app_display['Rating 1-2 (%)'].round(1).apply(lambda x: f"{x:.1f}%")
            app_display['Rating 4-5 (%)'] = app_display['Rating 4-5 (%)'].round(1).apply(lambda x: f"{x:.1f}%")
            
            st.dataframe(app_display, hide_index=True, height=430, use_container_width=True)
            
        st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
        
        render_section_title("Sebaran Proporsi Klaster pada Tiap Aplikasi (Heatmap)", "Memetakan jenis topik dan keluhan yang paling dominan muncul pada masing-masing produk.", icon="target")
        
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
            color_continuous_scale="Purples",
            text_auto=True,
            aspect="auto"
        )
        fig_heat.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=440,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", size=10)
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        
    # ---------------- TAB 3: PROYEKSI 2D (PCA) ----------------
    with tab3:
        render_section_title("Proyeksi Ruang Vektor 2D Menggunakan PCA", "Reduksi dimensi dari embedding 384-d menjadi bidang koordinat 2 dimensi.", icon="compass")
        
        info_svg = icon_svg("info", size=16, color="#4F46E5")
        st.markdown(f"""
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-left: 3px solid #4F46E5; border-radius: 8px; padding: 0.9rem 1.1rem; margin-bottom: 1.2rem; font-size: 0.85rem; color: #334155; line-height: 1.55;">
            <div style="font-weight: 600; color: #0F172A; margin-bottom: 0.25rem; display: flex; align-items: center; gap: 0.4rem;">
                {info_svg} Catatan Metodologi Reduksi Dimensi
            </div>
            Vektor representasi semantik asli berukuran <b>384 dimensi</b> (<code>paraphrase-multilingual-MiniLM-L12-v2</code>).
            Proyeksi 2 dimensi menggunakan Principal Component Analysis (PCA) ini mempertahankan sekitar <b>16.4% dari total varians data</b> (PC1: ~8.9%, PC2: ~7.5%).
            Oleh karena itu, proyeksi 2D <b>tidak mewakili seluruh geometri ruang embedding asli</b>, dan tumpang tindih visual (overlap) pada bidang 2D adalah konsekuensi alami dari reduksi dimensi teks ulasan.
        </div>
        """, unsafe_allow_html=True)
        
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
                color_by = st.radio("Pewarnaan Titik:", ["Klaster Semantik (k=10)", "Skor Rating (1-5)"], horizontal=True)
            with p_col2:
                sample_size = st.slider("Jumlah Titik Sampel (Responsivitas Visual):", min_value=1000, max_value=len(df), value=3000, step=1000)
                
            sample_plot = plot_df.sample(n=min(sample_size, len(plot_df)), random_state=42)
            
            if color_by == "Klaster Semantik (k=10)":
                cluster_colors = {str(k): CLUSTER_METADATA[k]['warna'] for k in range(10)}
                fig_pca = px.scatter(
                    sample_plot,
                    x='PC1',
                    y='PC2',
                    color='Cluster',
                    color_discrete_map=cluster_colors,
                    hover_data=['Aplikasi', 'Rating', 'Cuplikan Ulasan', 'Nama Klaster']
                )
            else:
                fig_pca = px.scatter(
                    sample_plot,
                    x='PC1',
                    y='PC2',
                    color='Rating',
                    color_continuous_scale='Tealgrn',
                    hover_data=['Aplikasi', 'Nama Klaster', 'Cuplikan Ulasan']
                )
                
            fig_pca.update_traces(marker=dict(size=4.5, opacity=0.7))
            fig_pca.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", size=11),
                xaxis=dict(showgrid=True, gridcolor='#F4F4F5'),
                yaxis=dict(showgrid=True, gridcolor='#F4F4F5')
            )
            st.plotly_chart(fig_pca, use_container_width=True)
        else:
            st.info("Koordinat PCA sedang disiapkan.")
            
    # ---------------- TAB 4: BOXPLOT DISTRIBUSI SKOR ----------------
    with tab4:
        render_section_title("Distribusi Rating pada Setiap Klaster (Boxplot)", "Replikasi visualisasi Gambar 2 laporan penelitian, menunjukkan rentang kuartil dan median rating per klaster.", icon="bar-chart-3")
        
        df_box = df.copy()
        
        fig_box = px.box(
            df_box,
            x='cluster_semantik_10',
            y='score',
            color='cluster_semantik_10',
            color_discrete_map={k: CLUSTER_METADATA[k]['warna'] for k in range(10)},
            labels={'cluster_semantik_10': 'ID Klaster (0–9)', 'score': 'Rating (1–5)'}
        )
        fig_box.update_layout(
            margin=dict(l=10, r=10, t=10, b=20),
            height=400,
            showlegend=False,
            yaxis=dict(range=[0.5, 5.5], dtick=1, showgrid=True, gridcolor='#F4F4F5', tickfont=dict(size=11, color='#71717A')),
            xaxis=dict(tickfont=dict(size=11, color='#71717A')),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", size=11)
        )
        st.plotly_chart(fig_box, use_container_width=True)
        
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E4E4E7; border-radius: 8px; padding: 1rem; margin-top: 1rem; font-size: 0.85rem; color: #3F3F46; line-height: 1.6;">
            <b>Interpretasi Temuan Boxplot (Laporan Penelitian):</b>
            <ul style="margin: 0.4rem 0 0 0; padding-left: 1.2rem;">
                <li><b>Cluster 4, 7, dan 8:</b> Memiliki median rating <b>4.0</b> dengan kotak kuartil berada di rentang 4 hingga 5.</li>
                <li><b>Cluster 5 (Akun & Sinkronisasi):</b> Memiliki kotak paling padat di dasar skor 1 hingga 2 (median <b>2.0</b>).</li>
                <li><b>Cluster 1, 0, 2, dan 6:</b> Berpusat pada rentang ulasan keluhan rating 1–2 (median <b>2.0</b>).</li>
                <li><b>Cluster 3 (Manajemen Tugas):</b> Memiliki sebaran paling seimbang dengan median <b>3.0</b>.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
