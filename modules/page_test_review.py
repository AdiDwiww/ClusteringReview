import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from modules.ui_theme import render_workspace_header, render_tag_list, render_section_title
from modules.cluster_info import CLUSTER_METADATA
from modules.data_loader import clean_text
from modules.icons import icon_svg

@st.cache_resource(show_spinner=False)
def load_prediction_pipeline():
    """
    Memuat model SentenceTransformer dan model K-Means hasil rekonstruksi identik (100% match).
    Menggunakan caching resource agar tidak dimuat ulang pada setiap interaksi.
    """
    model_path = "models/kmeans_model.joblib"
    if not os.path.exists(model_path):
        return None, None, "File model K-Means (models/kmeans_model.joblib) tidak ditemukan."
        
    try:
        from sentence_transformers import SentenceTransformer
        embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        kmeans_model = joblib.load(model_path)
        return embedding_model, kmeans_model, None
    except Exception as e:
        return None, None, f"Gagal memuat komponen model: {str(e)}"

def show(df: pd.DataFrame):
    render_workspace_header(
        title="Uji Inferensi Ulasan Baru",
        subtitle="Prediksi penempatan klaster untuk teks ulasan baru menggunakan Sentence Transformers (384d) dan model K-Means final.",
        category="Model Inference",
        icon="sparkles"
    )
    
    # 1. Verifikasi Ketersediaan Komponen Model
    model_path = "models/kmeans_model.joblib"
    if not os.path.exists(model_path):
        alert_icon = icon_svg("alert-triangle", size=18, color="#DC2626")
        st.markdown(f"""
        <div style="background: #FEF2F2; border: 1px solid #FCA5A5; border-radius: 8px; padding: 1rem; color: #991B1B;">
            <div style="font-weight: 700; margin-bottom: 0.25rem; display: flex; align-items: center; gap: 0.4rem;">
                {alert_icon} Fitur Prediksi Dinonaktifkan Sementara
            </div>
            <div style="font-size: 0.85rem;">File model K-Means final tidak ditemukan di direktori <code>models/</code>. Sistem tidak akan membuat prediksi tiruan berbasis pencocokan kata manual demi menjaga integritas penelitian.</div>
        </div>
        """, unsafe_allow_html=True)
        return
        
    with st.spinner("Memeriksa kesiapan model Sentence Transformers & K-Means..."):
        embedder, kmeans, load_err = load_prediction_pipeline()
        
    if load_err or embedder is None or kmeans is None:
        alert_icon = icon_svg("alert-triangle", size=18, color="#DC2626")
        st.markdown(f"""
        <div style="background: #FEF2F2; border: 1px solid #FCA5A5; border-radius: 8px; padding: 1rem; color: #991B1B;">
            <div style="font-weight: 700; margin-bottom: 0.25rem; display: flex; align-items: center; gap: 0.4rem;">
                {alert_icon} Komponen Inferensi Belum Siap
            </div>
            <div style="font-size: 0.85rem;">{load_err}</div>
        </div>
        """, unsafe_allow_html=True)
        return
        
    check_icon = icon_svg("check-circle-2", size=15, color="#059669")
    st.markdown(f"""
    <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; padding: 0.75rem 1rem; font-size: 0.82rem; color: #166534; display: flex; align-items: center; gap: 0.45rem; margin-bottom: 1.25rem;">
        {check_icon} <span><b>Pipeline Siap:</b> Menggunakan <code>paraphrase-multilingual-MiniLM-L12-v2</code> (384-d, L2-normalized) dan K-Means final (k=10, random_state=42).</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Input Ulasan Pengguna
    render_section_title("Formulir Input Teks Ulasan", "Mendukung ulasan dalam bahasa Indonesia maupun bahasa Inggris.", icon="message-square")
    
    example_prompts = {
        "Pilih contoh teks preset...": "",
        "Keluhan Teknis / Crash": "Aplikasi sering crash tiba-tiba setelah update versi terbaru dan data tidak tersimpan.",
        "Monetisasi & Versi Pro": "Too expensive for the pro subscription, free version is way too limited now.",
        "Masalah Notifikasi & Alarm": "Pengingat dan alarm sering tidak berbunyi tepat waktu saat HP dalam keadaan standby.",
        "Masalah Akun & Sinkronisasi": "Failed to sync my notes with Google account, all my tasks are gone!",
        "Pujian Kemudahan Aplikasi": "Very easy to use, simple interface and really helps my daily productivity. Love it!",
        "Manajemen Tugas & Fitur": "Please add subtasks feature and calendar integration for daily checklist."
    }
    
    selected_example = st.selectbox("Coba Contoh Ulasan:", list(example_prompts.keys()))
    
    initial_text = example_prompts[selected_example] if selected_example != "Pilih contoh teks preset..." else ""
    
    user_review = st.text_area(
        "Teks Ulasan Pengguna:",
        value=initial_text,
        height=110,
        placeholder="Ketik ulasan baru di sini..."
    )
    
    btn_predict = st.button("Jalankan Prediksi Klaster", type="primary", use_container_width=True)
    
    if btn_predict:
        if not user_review.strip():
            st.warning("Silakan masukkan teks ulasan terlebih dahulu.")
            return
            
        with st.spinner("Memproses teks dan menghitung kedekatan sentroid..."):
            cleaned_text = clean_text(user_review)
            
            if not cleaned_text.strip():
                st.error("Teks ulasan tidak memuat karakter alfabet yang valid setelah dibersihkan dari simbol/tanda baca.")
                return
                
            review_vector = embedder.encode(
                [cleaned_text],
                normalize_embeddings=True
            )
            
            predicted_cluster = int(kmeans.predict(review_vector)[0])
            meta = CLUSTER_METADATA.get(predicted_cluster, {})
            
            centroid = kmeans.cluster_centers_[predicted_cluster]
            euclidean_dist = float(np.linalg.norm(review_vector[0] - centroid))
            norm_centroid = centroid / np.linalg.norm(centroid)
            cosine_sim = float(np.dot(review_vector[0], norm_centroid))
            
        # Tampilkan Hasil Prediksi
        st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
        render_section_title("Hasil Prediksi Tematik", "Klasifikasi klaster berdasarkan sentroid terdekat pada ruang vektor semantik.", icon="target")
        
        st.markdown(f"""
        <div class="saas-card" style="border-top: 4px solid {meta['warna']};">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.8rem;">
                <div>
                    <span class="saas-badge" style="background: #F4F4F5; color: #18181B; margin-bottom: 0.35rem;">
                        PREDIKSI: CLUSTER {predicted_cluster}
                    </span>
                    <h3 style="margin: 0.35rem 0 0.15rem 0; color: #09090B; font-weight: 700; font-size: 1.35rem;">{meta['name']}</h3>
                </div>
                <div style="text-align: right; background: #FAFAFA; border: 1px solid #E4E4E7; border-radius: 8px; padding: 0.4rem 0.8rem;">
                    <div style="font-size: 0.7rem; color: #71717A; font-weight: 600; text-transform: uppercase;">Kemiripan Sentroid</div>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #09090B; font-family: 'JetBrains Mono', monospace;">
                        {cosine_sim:.4f} <span style="font-size: 0.72rem; font-weight: 500; color: #71717A;">(Cosine)</span>
                    </div>
                </div>
            </div>
            <div style="font-size: 0.9rem; color: #3F3F46; line-height: 1.6; margin-bottom: 0.9rem;">
                <div><b>Tema Penafsiran:</b> <i>{meta['tema']}</i></div>
                <div style="margin-top: 0.25rem;"><b>Deskripsi Klaster:</b> {meta['deskripsi']}</div>
            </div>
            <div style="display: flex; gap: 1.5rem; flex-wrap: wrap; font-size: 0.8rem; color: #52525B; padding-top: 0.75rem; border-top: 1px solid #F4F4F5; font-family: 'JetBrains Mono', monospace;">
                <span>Ukuran: <b>{meta['n_ulasan']:,}</b> ({meta['persentase']}%)</span>
                <span>Rata-rata Historis: <b>{meta['rata_rata_rating']} / 5.0</b></span>
                <span>Rating Rendah (1-2): <b>{meta['pct_rating_1_2']}%</b></span>
                <span>Rating Tinggi (4-5): <b>{meta['pct_rating_4_5']}%</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Detail Metrik Kedekatan
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("""
            <div style="font-size: 0.82rem; font-weight: 600; color: #71717A; text-transform: uppercase; margin-bottom: 0.35rem;">
                Kata Kunci Representatif Klaster
            </div>
            """, unsafe_allow_html=True)
            render_tag_list(meta['kata_kunci'])
        with col_m2:
            st.markdown("""
            <div style="font-size: 0.82rem; font-weight: 600; color: #71717A; text-transform: uppercase; margin-bottom: 0.35rem;">
                Jarak Geometris ke Pusat Klaster
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"Jarak Euclidean ke Sentroid: `{euclidean_dist:.4f}`")
            st.caption(f"Cosine Similarity ke Sentroid: `{cosine_sim:.4f}`")
            st.caption("Nilai di atas merupakan ukuran kedekatan jarak spasial dalam ruang vektor berdimensi 384, bukan probabilitas kelas.")
            
        st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
        
        # 5. Ulasan Serupa dari Klaster Tersebut
        render_section_title("Sampel Ulasan Serupa dari Dataset Asli", f"Ulasan riil dari dataset yang berada di dalam Cluster {predicted_cluster}.", icon="message-square")
        
        cluster_samples = df[df['cluster_semantik_10'] == predicted_cluster].sample(
            n=min(3, (df['cluster_semantik_10'] == predicted_cluster).sum()),
            random_state=123
        )
        
        for _, s_row in cluster_samples.iterrows():
            st.markdown(f"""
            <div class="quote-card" style="border-left-color: {meta['warna']};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                    <span style="font-weight: 700; color: #09090B; font-size: 0.82rem;">Rating {s_row['score']}.0 / 5.0</span>
                    <span style="font-size: 0.78rem; color: #71717A;">{s_row['app_name']}</span>
                </div>
                <div style="color: #27272A; font-size: 0.88rem;">"{s_row['content']}"</div>
            </div>
            """, unsafe_allow_html=True)
