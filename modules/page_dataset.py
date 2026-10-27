import streamlit as st
import pandas as pd
import plotly.express as px
from modules.ui_theme import render_workspace_header, render_kpi, render_section_title
from modules.cluster_info import CLUSTER_METADATA
from modules.icons import icon_svg

def show(df: pd.DataFrame):
    render_workspace_header(
        title="Eksplorasi Dataset Ulasan",
        subtitle="Penyaringan dinamis, pencarian kata kunci, analisis distribusi panjang teks, dan navigasi data ber-paginasi.",
        category="Data Exploration",
        icon="database"
    )
    
    # 1. Filter Kontrol
    filter_icon = icon_svg("sliders-horizontal", size=14, color="#4F46E5")
    with st.expander(f"Parameter Filter & Pencarian", expanded=True):
        f_col1, f_col2, f_col3, f_col4 = st.columns([1.5, 1, 1, 1.2])
        
        with f_col1:
            search_query = st.text_input(
                "Pencarian Teks Ulasan:",
                placeholder="Ketik kata kunci: misal 'crash', 'sync', 'widget', 'login'...",
                help="Mencari kata kunci pada kolom ulasan asli maupun teks yang telah diprapemroses."
            )
            
        with f_col2:
            app_options = ["Semua Aplikasi"] + sorted(df['app_name'].unique().tolist())
            selected_app = st.selectbox("Aplikasi:", app_options)
            
        with f_col3:
            rating_options = [
                "Semua Rating",
                "Skor 1", "Skor 2", "Skor 3", "Skor 4", "Skor 5",
                "Rating Rendah (1-2)", "Rating Tinggi (4-5)"
            ]
            selected_rating = st.selectbox("Rating:", rating_options)
            
        with f_col4:
            cluster_choices = ["Semua Klaster"] + [
                f"Cluster {i}: {CLUSTER_METADATA.get(i, {}).get('name', '')[:20]}"
                for i in range(10)
            ]
            selected_cluster = st.selectbox("Klaster Tematik:", cluster_choices)
            
    # Terapkan Filter
    filtered_df = df.copy()
    
    if search_query.strip():
        q = search_query.strip().lower()
        filtered_df = filtered_df[
            filtered_df['content'].str.lower().str.contains(q, na=False) |
            filtered_df['cleaned_content'].str.lower().str.contains(q, na=False)
        ]
        
    if selected_app != "Semua Aplikasi":
        filtered_df = filtered_df[filtered_df['app_name'] == selected_app]
        
    if selected_rating != "Semua Rating":
        if selected_rating == "Skor 1":
            filtered_df = filtered_df[filtered_df['score'] == 1]
        elif selected_rating == "Skor 2":
            filtered_df = filtered_df[filtered_df['score'] == 2]
        elif selected_rating == "Skor 3":
            filtered_df = filtered_df[filtered_df['score'] == 3]
        elif selected_rating == "Skor 4":
            filtered_df = filtered_df[filtered_df['score'] == 4]
        elif selected_rating == "Skor 5":
            filtered_df = filtered_df[filtered_df['score'] == 5]
        elif selected_rating == "Rating Rendah (1-2)":
            filtered_df = filtered_df[filtered_df['score'] <= 2]
        elif selected_rating == "Rating Tinggi (4-5)":
            filtered_df = filtered_df[filtered_df['score'] >= 4]
            
    if selected_cluster != "Semua Klaster":
        cluster_id = int(selected_cluster.split(":")[0].replace("Cluster", "").strip())
        filtered_df = filtered_df[filtered_df['cluster_semantik_10'] == cluster_id]
        
    # 2. Statistik Singkat Hasil Filter
    total_filtered = len(filtered_df)
    
    kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)
    with kpi_c1:
        render_kpi("Hasil Filter", f"{total_filtered:,}", f"Dari {len(df):,} total ulasan", "filter", "#4F46E5")
    with kpi_c2:
        avg_filtered_score = filtered_df['score'].mean() if total_filtered > 0 else 0
        render_kpi("Rata-rata Rating", f"{avg_filtered_score:.2f} / 5.0", "Pada data terfilter", "star", "#D97706")
    with kpi_c3:
        avg_chars = filtered_df['panjang_teks'].mean() if total_filtered > 0 else 0
        render_kpi("Rata-rata Karakter", f"{avg_chars:.0f} chars", "Panjang teks ulasan", "message-square", "#0D9488")
    with kpi_c4:
        avg_words = filtered_df['jumlah_kata'].mean() if total_filtered > 0 else 0
        render_kpi("Rata-rata Kata", f"{avg_words:.1f} kata", "Per ulasan terfilter", "activity", "#7C3AED")
        
    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    
    if total_filtered == 0:
        alert_svg = icon_svg("alert-circle", size=16, color="#D97706")
        st.markdown(f"""
        <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 8px; padding: 1rem; color: #92400E; display: flex; align-items: center; gap: 0.5rem;">
            {alert_svg} <span>Tidak ditemukan ulasan yang memenuhi kombinasi kriteria filter di atas. Silakan sesuaikan kembali kata kunci atau opsi filter Anda.</span>
        </div>
        """, unsafe_allow_html=True)
        return
        
    # 3. Distribusi Panjang Ulasan
    with st.expander("Distribusi Panjang Teks Ulasan (Histogram Kata)", expanded=False):
        fig_hist = px.histogram(
            filtered_df,
            x='jumlah_kata',
            nbins=40,
            color_discrete_sequence=['#4F46E5'],
            labels={'jumlah_kata': 'Jumlah Kata per Ulasan', 'count': 'Jumlah Ulasan'}
        )
        fig_hist.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=250,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", size=11),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#F4F4F5')
        )
        st.plotly_chart(fig_hist, width='stretch')
        
    # 4. Tabel Data dengan Paginasi
    render_section_title("Tabel Data Ulasan", f"Menampilkan catatan ulasan terverifikasi dengan fitur paginasi.", icon="database")
    
    page_size_options = [10, 25, 50, 100]
    col_p1, col_p2 = st.columns([1, 2])
    with col_p1:
        page_size = st.selectbox("Baris per halaman:", page_size_options, index=0)
        
    total_pages = max(1, (total_filtered + page_size - 1) // page_size)
    
    with col_p2:
        current_page = st.number_input(
            f"Nomor Halaman (1 s/d {total_pages}):",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1
        )
        
    start_idx = (current_page - 1) * page_size
    end_idx = min(start_idx + page_size, total_filtered)
    
    display_cols = [
        'app_name', 'score', 'cluster_semantik_10', 'cluster_name',
        'content', 'panjang_teks', 'jumlah_kata', 'at'
    ]
    valid_cols = [c for c in display_cols if c in filtered_df.columns]
    
    page_data = filtered_df.iloc[start_idx:end_idx][valid_cols].copy()
    page_data.rename(columns={
        'app_name': 'Aplikasi',
        'score': 'Rating',
        'cluster_semantik_10': 'Klaster',
        'cluster_name': 'Tema Klaster',
        'content': 'Teks Ulasan',
        'panjang_teks': 'Karakter',
        'jumlah_kata': 'Kata',
        'at': 'Waktu'
    }, inplace=True)
    
    st.caption(f"Menampilkan baris **{start_idx + 1}** sampai **{end_idx}** dari **{total_filtered:,}** ulasan.")
    st.dataframe(
        page_data,
        width='stretch',
        hide_index=True,
        height=380
    )
    
    # Tombol Ekspor CSV Hasil Filter
    csv_export = filtered_df[valid_cols].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Unduh Data Terfilter (CSV)",
        data=csv_export,
        file_name="ulasan_terfilter.csv",
        mime="text/csv"
    )
