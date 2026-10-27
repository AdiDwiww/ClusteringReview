import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.ui_theme import render_hero_banner, render_kpi, render_keyword_tags
from modules.cluster_info import CLUSTER_METADATA

def show(df: pd.DataFrame):
    render_hero_banner(
        title="Eksplorasi Tematik Klaster Ulasan (k=10)",
        subtitle="Analisis mendalam per klaster: statistik rating, kata kunci dominan TF-IDF, interpretasi tema, dan sampel ulasan nyata.",
        tag="Cluster Explorer"
    )
    
    # 1. Pilihan Klaster
    options = ["Semua Klaster (Ringkasan Komparatif)"] + [
        f"Cluster {i}: {CLUSTER_METADATA[i]['name']}" for i in range(10)
    ]
    
    selected_option = st.selectbox(
        "Pilih Klaster untuk Ditinjau:",
        options,
        index=0
    )
    
    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    
    # KONDISI A: Seluruh Klaster (Ringkasan Komparatif)
    if selected_option == "Semua Klaster (Ringkasan Komparatif)":
        st.markdown("### 📋 Ringkasan Komparatif Seluruh 10 Klaster")
        st.caption("Berdasarkan Tabel 5 Laporan Penelitian: perbandingan ukuran ulasan, rating, kata kunci TF-IDF, dan interpretasi tema.")
        
        # Buat tabel ringkasan
        table_rows = []
        for c_id in range(10):
            meta = CLUSTER_METADATA[c_id]
            c_df = df[df['cluster_semantik_10'] == c_id]
            table_rows.append({
                "ID": f"C{c_id}",
                "Nama Klaster": meta['name'],
                "Jumlah Ulasan": f"{len(c_df):,} ({len(c_df)/len(df)*100:.1f}%)",
                "Rata-rata Rating": f"{c_df['score'].mean():.2f} ★",
                "Median": f"{c_df['score'].median():.1f}",
                "Rating 1–2 (%)": f"{(c_df['score'] <= 2).mean()*100:.1f}%",
                "Rating 4–5 (%)": f"{(c_df['score'] >= 4).mean()*100:.1f}%",
                "Kata Kunci Dominan": ", ".join(meta['kata_kunci'][:5]),
                "Interpretasi Tema": meta['tema']
            })
            
        summary_table_df = pd.DataFrame(table_rows)
        st.dataframe(
            summary_table_df,
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
        
        # Grid Kartu 10 Klaster
        st.markdown("### 🗂️ Kartu Informasi 10 Klaster")
        for row_idx in range(0, 10, 2):
            c_col1, c_col2 = st.columns(2)
            for c_col, c_id in zip([c_col1, c_col2], [row_idx, row_idx + 1]):
                meta = CLUSTER_METADATA[c_id]
                c_df = df[df['cluster_semantik_10'] == c_id]
                with c_col:
                    with st.container():
                        st.markdown(f"""
                        <div style="background: white; border: 1px solid #E2E8F0; border-top: 4px solid {meta['warna']}; border-radius: 12px; padding: 1.1rem; margin-bottom: 1rem; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                <span style="font-weight: 800; font-size: 1.05rem; color: #0F172A;">Cluster {c_id}: {meta['name']}</span>
                                <span style="background: {meta['warna']}20; color: {meta['warna']}; font-weight: 700; font-size: 0.78rem; padding: 0.15rem 0.5rem; border-radius: 9999px;">
                                    {len(c_df):,} ulasan ({len(c_df)/len(df)*100:.1f}%)
                                </span>
                            </div>
                            <div style="font-size: 0.85rem; color: #475569; margin-bottom: 0.6rem; min-height: 40px;">
                                <b>Tema:</b> {meta['tema']}
                            </div>
                            <div style="display: flex; gap: 1rem; font-size: 0.82rem; color: #64748B; margin-bottom: 0.6rem;">
                                <span>⭐ Rata-rata: <b>{c_df['score'].mean():.2f}</b></span>
                                <span>🔻 1–2: <b>{(c_df['score']<=2).mean()*100:.1f}%</b></span>
                                <span>🔺 4–5: <b>{(c_df['score']>=4).mean()*100:.1f}%</b></span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        render_keyword_tags(meta['kata_kunci'])
        return

    # KONDISI B: Klaster Spesifik Terpilih (0 - 9)
    cluster_id = int(selected_option.split(":")[0].replace("Cluster", "").strip())
    meta = CLUSTER_METADATA[cluster_id]
    cluster_df = df[df['cluster_semantik_10'] == cluster_id]
    
    n_count = len(cluster_df)
    n_pct = (n_count / len(df)) * 100
    mean_val = cluster_df['score'].mean()
    median_val = cluster_df['score'].median()
    pct_low = (cluster_df['score'] <= 2).mean() * 100
    pct_high = (cluster_df['score'] >= 4).mean() * 100
    
    # 2. KPI Cards Klaster Terpilih
    k_col1, k_col2, k_col3, k_col4 = st.columns(4)
    with k_col1:
        render_kpi("Jumlah Ulasan", f"{n_count:,}", f"{n_pct:.1f}% dari dataset total", meta['warna'])
    with k_col2:
        render_kpi("Rata-rata Rating", f"{mean_val:.2f} ★", f"Median: {median_val:.0f}.0 ★", meta['warna'])
    with k_col3:
        render_kpi("Rating Rendah (1–2)", f"{pct_low:.1f}%", f"{int(pct_low*n_count/100):,} ulasan negatif", "#EF4444")
    with k_col4:
        render_kpi("Rating Tinggi (4–5)", f"{pct_high:.1f}%", f"{int(pct_high*n_count/100):,} ulasan positif", "#10B981")
        
    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
    
    # 3. Profil Klaster & Kata Kunci
    col_info, col_chart = st.columns([1.3, 1])
    
    with col_info:
        st.markdown(f"### 🏷️ Profil & Interpretasi Tema (Cluster {cluster_id})")
        st.markdown(f"**Nama Klaster:** {meta['name']}")
        st.markdown(f"**Tema Penafsiran:** *{meta['tema']}*")
        st.markdown(f"**Kecenderungan Sentimen:** `{meta['kategori_sentimen_dominan']}`")
        st.markdown(f"**Uraian Analitis:**\n{meta['deskripsi']}")
        
        st.markdown("**Kata Kunci Representatif (Bobot TF-IDF pada Klaster):**")
        render_keyword_tags(meta['kata_kunci'])
        
        st.caption("""
        *Catatan Metodologi: Kata kunci diperoleh dari perhitungan rata-rata bobot TF-IDF (5.000 fitur unigram+bigram, min_df 5) pada ulasan dalam klaster ini, terpisah dari ruang embedding Sentence Transformers.*
        """)
        
    with col_chart:
        st.markdown("### 📊 Sebaran Rating pada Klaster Ini")
        score_counts = cluster_df['score'].value_counts().sort_index().reset_index()
        score_counts.columns = ['Rating', 'Jumlah']
        score_counts['Label'] = score_counts['Rating'].apply(lambda x: f"★ {x}")
        
        colors = ['#EF4444', '#F97316', '#FBBF24', '#34D399', '#10B981']
        fig_score = go.Figure(data=[
            go.Bar(
                x=score_counts['Label'],
                y=score_counts['Jumlah'],
                text=score_counts['Jumlah'],
                textposition='auto',
                marker=dict(color=colors)
            )
        ])
        fig_score.update_layout(
            margin=dict(l=10, r=10, t=20, b=20),
            height=280,
            xaxis_title="Rating Bintang",
            yaxis_title="Jumlah",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_score, use_container_width=True)
        
    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
    
    # 4. Contoh Ulasan Nyata dari Dataset CSV
    st.markdown("### 💬 Contoh Ulasan Nyata dari Klaster Ini")
    st.caption("Sampel ulasan autentik dari dataset hasil clustering (bukan data simulasi):")
    
    # Filter contoh berdasarkan rating dalam klaster
    samp_col1, samp_col2 = st.columns([1, 2])
    with samp_col1:
        sample_rating_filter = st.selectbox(
            "Filter Rating Sampel:",
            ["Semua Rating Sampel", "Rating Rendah (1-2)", "Rating Tinggi (4-5)"]
        )
    with samp_col2:
        num_samples = st.slider("Jumlah sampel yang ditampilkan:", min_value=3, max_value=12, value=6, step=3)
        
    sample_pool = cluster_df.copy()
    if sample_rating_filter == "Rating Rendah (1-2)":
        sample_pool = sample_pool[sample_pool['score'] <= 2]
    elif sample_rating_filter == "Rating Tinggi (4-5)":
        sample_pool = sample_pool[sample_pool['score'] >= 4]
        
    if len(sample_pool) > 0:
        samples = sample_pool.sample(n=min(num_samples, len(sample_pool)), random_state=42)
        
        for _, row in samples.iterrows():
            score_stars = "★" * int(row['score']) + "☆" * (5 - int(row['score']))
            star_color = "#EF4444" if row['score'] <= 2 else ("#10B981" if row['score'] >= 4 else "#F59E0B")
            
            st.markdown(f"""
            <div class="review-quote" style="border-left-color: {meta['warna']};">
                <div style="font-weight: 700; color: {star_color}; margin-bottom: 0.25rem;">
                    {score_stars} ({row['score']}.0) — {row['app_name']}
                </div>
                <div>"{row['content']}"</div>
                <div class="review-quote-meta">
                    Karakter: {row['panjang_teks']} | Kata: {row['jumlah_kata']} | Teks Bersih: <i>{row['cleaned_content'][:100]}...</i>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Tidak ada sampel ulasan untuk filter rating ini pada klaster terpilih.")
