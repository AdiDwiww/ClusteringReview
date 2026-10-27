import streamlit as st
import pandas as pd
import plotly.express as px
from modules.ui_theme import render_hero_banner, render_kpi
from modules.cluster_info import CLUSTER_METADATA

def show(df: pd.DataFrame):
    render_hero_banner(
        title="Eksplorasi Dataset Ulasan",
        subtitle="Filter interaktif, pencarian kata kunci, statistik teks ulasan, dan navigasi data ber-paginasi.",
        tag="Data Explorer"
    )
    
    # 1. Filter Kontrol di Sidebar atau Top Box
    with st.expander("🔍 Filter Dataset & Opsi Pencarian", expanded=True):
        f_col1, f_col2, f_col3, f_col4 = st.columns([1.5, 1, 1, 1.2])
        
        with f_col1:
            search_query = st.text_input(
                "Cari Kata/Frasa dalam Ulasan:",
                placeholder="Contoh: crash, login, widget, sync, best...",
                help="Mencari kata kunci pada kolom teks ulasan asli maupun teks bersih."
            )
            
        with f_col2:
            app_options = ["Semua Aplikasi"] + sorted(df['app_name'].unique().tolist())
            selected_app = st.selectbox("Filter Aplikasi:", app_options)
            
        with f_col3:
            rating_options = ["Semua Rating", "1 Bintang", "2 Bintang", "3 Bintang", "4 Bintang", "5 Bintang", "Rating Rendah (1-2)", "Rating Tinggi (4-5)"]
            selected_rating = st.selectbox("Filter Rating:", rating_options)
            
        with f_col4:
            cluster_choices = ["Semua Klaster"] + [
                f"Cluster {i}: {CLUSTER_METADATA.get(i, {}).get('name', '')[:20]}"
                for i in range(10)
            ]
            selected_cluster = st.selectbox("Filter Klaster:", cluster_choices)
            
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
        if selected_rating == "1 Bintang":
            filtered_df = filtered_df[filtered_df['score'] == 1]
        elif selected_rating == "2 Bintang":
            filtered_df = filtered_df[filtered_df['score'] == 2]
        elif selected_rating == "3 Bintang":
            filtered_df = filtered_df[filtered_df['score'] == 3]
        elif selected_rating == "4 Bintang":
            filtered_df = filtered_df[filtered_df['score'] == 4]
        elif selected_rating == "5 Bintang":
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
        render_kpi("Hasil Filter", f"{total_filtered:,}", f"Dari {len(df):,} total ulasan", "#3B82F6")
    with kpi_c2:
        avg_filtered_score = filtered_df['score'].mean() if total_filtered > 0 else 0
        render_kpi("Rata-rata Rating", f"{avg_filtered_score:.2f} ★", "Pada data terfilter", "#10B981")
    with kpi_c3:
        avg_chars = filtered_df['panjang_teks'].mean() if total_filtered > 0 else 0
        render_kpi("Rata-rata Karakter", f"{avg_chars:.0f} chars", "Panjang teks ulasan", "#8B5CF6")
    with kpi_c4:
        avg_words = filtered_df['jumlah_kata'].mean() if total_filtered > 0 else 0
        render_kpi("Rata-rata Kata", f"{avg_words:.1f} kata", "Per ulasan terfilter", "#F59E0B")
        
    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    
    if total_filtered == 0:
        st.warning("⚠️ Tidak ada ulasan yang sesuai dengan kombinasi filter dan pencarian di atas. Silakan sesuaikan kriteria filter Anda.")
        return
        
    # 3. Distribusi Panjang Ulasan
    with st.expander("📈 Distribusi Panjang Teks Ulasan", expanded=False):
        fig_hist = px.histogram(
            filtered_df,
            x='jumlah_kata',
            nbins=40,
            color_discrete_sequence=['#4F46E5'],
            labels={'jumlah_kata': 'Jumlah Kata per Ulasan', 'count': 'Jumlah Ulasan'},
            title="Distribusi Jumlah Kata pada Ulasan Terfilter"
        )
        fig_hist.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=280,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
    # 4. Tabel Data dengan Paginasi
    st.markdown("### 📋 Tabel Data Ulasan")
    
    page_size_options = [10, 25, 50, 100]
    col_p1, col_p2 = st.columns([1, 2])
    with col_p1:
        page_size = st.selectbox("Jumlah baris per halaman:", page_size_options, index=0)
        
    total_pages = max(1, (total_filtered + page_size - 1) // page_size)
    
    with col_p2:
        current_page = st.number_input(
            f"Halaman (1 s/d {total_pages}):",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1
        )
        
    start_idx = (current_page - 1) * page_size
    end_idx = min(start_idx + page_size, total_filtered)
    
    # Kolom untuk ditampilkan
    display_cols = [
        'app_name', 'score', 'cluster_semantik_10', 'cluster_name',
        'content', 'panjang_teks', 'jumlah_kata', 'at'
    ]
    # Filter kolom yang ada
    valid_cols = [c for c in display_cols if c in filtered_df.columns]
    
    page_data = filtered_df.iloc[start_idx:end_idx][valid_cols].copy()
    page_data.rename(columns={
        'app_name': 'Aplikasi',
        'score': 'Rating',
        'cluster_semantik_10': 'ID Klaster',
        'cluster_name': 'Tema Klaster',
        'content': 'Teks Ulasan',
        'panjang_teks': 'Karakter',
        'jumlah_kata': 'Kata',
        'at': 'Tanggal'
    }, inplace=True)
    
    st.caption(f"Menampilkan baris **{start_idx + 1}** sampai **{end_idx}** dari **{total_filtered:,}** ulasan.")
    st.dataframe(
        page_data,
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    # Tombol Ekspor CSV Hasil Filter
    csv_export = filtered_df[valid_cols].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Unduh Data Terfilter (CSV)",
        data=csv_export,
        file_name="ulasan_terfilter.csv",
        mime="text/csv"
    )
