import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from modules.ui_theme import render_workspace_header, render_kpi, render_tag_list, render_section_title
from modules.cluster_info import CLUSTER_METADATA
from modules.icons import icon_svg

def show(df: pd.DataFrame):
    render_workspace_header(
        title="Eksplorasi Tematik Klaster",
        subtitle="Analisis terperinci tiap klaster: jumlah ulasan, rata-rata rating, kata kunci dominan TF-IDF, serta contoh ulasan asli pengguna.",
        category="Academic Dashboard",
        icon="layers"
    )
    
    # 1. Pilihan Klaster
    options = [
        f"Cluster {i}: {CLUSTER_METADATA[i]['name']}" for i in range(10)
    ] + ["Semua Klaster (Ringkasan Komparatif)"]
    
    selected_option = st.selectbox(
        "Pilih Klaster Analisis:",
        options,
        index=0
    )
    
    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    
    # KONDISI A: Seluruh Klaster (Ringkasan Komparatif)
    if selected_option == "Semua Klaster (Ringkasan Komparatif)":
        render_section_title("Ringkasan Komparatif Seluruh 10 Klaster", "Data resmi sesuai Tabel 5 laporan penelitian: ukuran, rating, kata kunci leksikal, dan interpretasi tema.", icon="database")
        
        table_rows = []
        for c_id in range(10):
            meta = CLUSTER_METADATA[c_id]
            c_df = df[df['cluster_semantik_10'] == c_id]
            table_rows.append({
                "Klaster": f"C{c_id}",
                "Nama Klaster": meta['name'],
                "Ulasan": f"{len(c_df):,} ({len(c_df)/len(df)*100:.1f}%)",
                "Rata-rata": f"{c_df['score'].mean():.2f}",
                "Median": f"{c_df['score'].median():.1f}",
                "Rating 1–2 (%)": f"{(c_df['score'] <= 2).mean()*100:.1f}%",
                "Rating 4–5 (%)": f"{(c_df['score'] >= 4).mean()*100:.1f}%",
                "Kata Kunci Dominan": ", ".join(meta['kata_kunci'][:5]),
                "Interpretasi Tema": meta['tema']
            })
            
        summary_table_df = pd.DataFrame(table_rows)
        st.dataframe(
            summary_table_df,
            hide_index=True,
            use_container_width=True
        )
        
        st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
        
        # Grid Kartu 10 Klaster
        render_section_title("Profil Singkat 10 Klaster", "Ringkasan metrik dan kata kunci untuk setiap kelompok tematik.", icon="grid")
        for row_idx in range(0, 10, 2):
            c_col1, c_col2 = st.columns(2)
            for c_col, c_id in zip([c_col1, c_col2], [row_idx, row_idx + 1]):
                meta = CLUSTER_METADATA[c_id]
                c_df = df[df['cluster_semantik_10'] == c_id]
                with c_col:
                    st.markdown(f"""
                    <div class="saas-card" style="border-top: 3px solid {meta['warna']}; height: 100%;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                            <span style="font-weight: 700; font-size: 0.98rem; color: #09090B;">Cluster {c_id}: {meta['name']}</span>
                            <span class="saas-badge" style="background: #F4F4F5; color: #52525B;">
                                {len(c_df):,} ulasan ({len(c_df)/len(df)*100:.1f}%)
                            </span>
                        </div>
                        <div style="font-size: 0.82rem; color: #52525B; margin-bottom: 0.6rem; min-height: 38px; line-height: 1.45;">
                            <b>Tema:</b> {meta['tema']}
                        </div>
                        <div style="display: flex; gap: 1rem; font-size: 0.78rem; color: #71717A; margin-bottom: 0.6rem; font-family: 'JetBrains Mono', monospace;">
                            <span>Skor: <b>{c_df['score'].mean():.2f}</b></span>
                            <span>Negatif: <b>{(c_df['score']<=2).mean()*100:.1f}%</b></span>
                            <span>Positif: <b>{(c_df['score']>=4).mean()*100:.1f}%</b></span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    render_tag_list(meta['kata_kunci'])
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
    
    # 2. KPI Cards Klaster Terpilih (Zero Emojis)
    k_col1, k_col2, k_col3, k_col4 = st.columns(4)
    with k_col1:
        render_kpi("Jumlah Ulasan", f"{n_count:,}", f"{n_pct:.1f}% dari dataset total", "message-square", meta['warna'])
    with k_col2:
        render_kpi("Rata-rata Rating", f"{mean_val:.2f} / 5.0", f"Median: {median_val:.0f}.0", "star", meta['warna'])
    with k_col3:
        render_kpi("Rating Rendah (1–2)", f"{pct_low:.1f}%", f"{int(pct_low*n_count/100):,} ulasan keluhan", "alert-triangle", "#DC2626")
    with k_col4:
        render_kpi("Rating Tinggi (4–5)", f"{pct_high:.1f}%", f"{int(pct_high*n_count/100):,} ulasan kepuasan", "check-circle-2", "#059669")
        
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    
    # 3. Profil Klaster & Kata Kunci
    col_info, col_chart = st.columns([1.3, 1])
    
    with col_info:
        render_section_title(f"Profil & Interpretasi Tema (Cluster {cluster_id})", "Deskripsi analitis mengenai pola ulasan di klaster ini.", icon="info")
        
        st.markdown(f"""
        <div class="saas-card" style="border-top: 3px solid {meta['warna']};">
            <div style="margin-bottom: 0.6rem;">
                <span style="font-size: 0.76rem; color: #71717A; font-weight: 600; text-transform: uppercase;">Nama Klaster</span>
                <div style="font-size: 1.15rem; font-weight: 700; color: #09090B;">{meta['name']}</div>
            </div>
            <div style="margin-bottom: 0.6rem;">
                <span style="font-size: 0.76rem; color: #71717A; font-weight: 600; text-transform: uppercase;">Tema Penafsiran</span>
                <div style="font-size: 0.9rem; color: #27272A; font-style: italic;">{meta['tema']}</div>
            </div>
            <div style="margin-bottom: 0.6rem;">
                <span style="font-size: 0.76rem; color: #71717A; font-weight: 600; text-transform: uppercase;">Kategori Sentimen Dominan</span>
                <div><span class="saas-badge" style="background: #F4F4F5; color: #18181B; margin-top: 0.2rem;">{meta['kategori_sentimen_dominan']}</span></div>
            </div>
            <div>
                <span style="font-size: 0.76rem; color: #71717A; font-weight: 600; text-transform: uppercase;">Uraian Analitis</span>
                <div style="font-size: 0.88rem; color: #3F3F46; line-height: 1.6; margin-top: 0.2rem;">{meta['deskripsi']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Kata Kunci Representatif (Bobot TF-IDF pada Klaster):**")
        render_tag_list(meta['kata_kunci'])
        
        st.caption("""
        Catatan Metodologi: Kata kunci diperoleh dari perhitungan rata-rata bobot TF-IDF (5.000 fitur unigram+bigram, min_df 5) pada ulasan dalam klaster ini, terpisah dari ruang embedding Sentence Transformers.
        """)
        
    with col_chart:
        render_section_title("Distribusi Rating pada Klaster", "Sebaran proporsi skor 1 hingga 5.", icon="bar-chart-3")
        score_counts = cluster_df['score'].value_counts().sort_index().reset_index()
        score_counts.columns = ['Rating', 'Jumlah']
        score_counts['Label'] = score_counts['Rating'].apply(lambda x: f"Skor {x}")
        
        colors = ['#EF4444', '#F97316', '#EAB308', '#22C55E', '#10B981']
        fig_score = go.Figure(data=[
            go.Bar(
                x=score_counts['Label'],
                y=score_counts['Jumlah'],
                text=score_counts['Jumlah'],
                textposition='auto',
                marker=dict(color=colors, line=dict(color='#E4E4E7', width=1))
            )
        ])
        fig_score.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=280,
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color='#71717A')),
            yaxis=dict(title="Jumlah", showgrid=True, gridcolor='#F4F4F5', tickfont=dict(size=11, color='#71717A')),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", size=11)
        )
        st.plotly_chart(fig_score, use_container_width=True)
        
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    
    # 4. Contoh Ulasan Nyata dari Dataset CSV
    render_section_title("Sampel Ulasan Nyata dari Klaster Ini", "Koleksi ulasan autentik dari dataset hasil clustering (bukan data simulasi).", icon="message-square")
    
    samp_col1, samp_col2 = st.columns([1, 2])
    with samp_col1:
        sample_rating_filter = st.selectbox(
            "Filter Rating Sampel:",
            ["Semua Rating Sampel", "Rating Rendah (1-2)", "Rating Tinggi (4-5)"]
        )
    with samp_col2:
        num_samples = st.slider("Jumlah sampel ditampilkan:", min_value=3, max_value=12, value=6, step=3)
        
    sample_pool = cluster_df.copy()
    if sample_rating_filter == "Rating Rendah (1-2)":
        sample_pool = sample_pool[sample_pool['score'] <= 2]
    elif sample_rating_filter == "Rating Tinggi (4-5)":
        sample_pool = sample_pool[sample_pool['score'] >= 4]
        
    if len(sample_pool) > 0:
        samples = sample_pool.sample(n=min(num_samples, len(sample_pool)), random_state=42)
        
        for _, row in samples.iterrows():
            star_color = "#DC2626" if row['score'] <= 2 else ("#059669" if row['score'] >= 4 else "#D97706")
            
            st.markdown(f"""
            <div class="quote-card" style="border-left-color: {meta['warna']};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                    <span style="font-weight: 700; color: {star_color}; font-size: 0.85rem;">
                        Rating {row['score']}.0 / 5.0
                    </span>
                    <span style="font-size: 0.78rem; color: #71717A; font-weight: 600;">{row['app_name']}</span>
                </div>
                <div style="color: #27272A;">"{row['content']}"</div>
                <div class="quote-meta">
                    <span>Karakter: {row['panjang_teks']}</span>
                    <span>•</span>
                    <span>Kata: {row['jumlah_kata']}</span>
                    <span>•</span>
                    <span>Teks Bersih: {row['cleaned_content'][:90]}...</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Tidak ada ulasan pada filter rating ini di klaster terpilih.")
