import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from modules.ui_theme import render_hero_banner, render_keyword_tags
from modules.cluster_info import CLUSTER_METADATA
from modules.data_loader import clean_text

@st.cache_resource(show_spinner=False)
def load_prediction_pipeline():
    """
    Memuat model SentenceTransformer dan model K-Means hasil rekonstruksi identik (100% match).
    Menggunakan caching resource agar tidak dimuat ulang pada setiap interaksi.
    """
    model_path = "models/kmeans_model.joblib"
    if not os.path.exists(model_path):
        return None, None, "File model K-Means (`models/kmeans_model.joblib`) tidak ditemukan."
        
    try:
        from sentence_transformers import SentenceTransformer
        # Muat model embedding paraphrase-multilingual-MiniLM-L12-v2
        embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        # Muat model K-Means
        kmeans_model = joblib.load(model_path)
        return embedding_model, kmeans_model, None
    except Exception as e:
        return None, None, f"Gagal memuat komponen model: {str(e)}"

def show(df: pd.DataFrame):
    render_hero_banner(
        title="Uji Prediksi Klaster Ulasan Baru",
        subtitle="Prediksi penempatan klaster untuk teks ulasan baru menggunakan Sentence Transformers dan K-Means final.",
        tag="Model Inference"
    )
    
    # 1. Verifikasi Ketersediaan Komponen Model
    model_path = "models/kmeans_model.joblib"
    if not os.path.exists(model_path):
        st.error("""
        ⛔ **Fitur Prediksi Dinonaktifkan Sementara**
        File model K-Means final tidak ditemukan di direktori `models/`.
        Sesuai integritas metodologi penelitian, sistem tidak akan membuat prediksi tiruan (palsu) berbasis pencocokan kata manual.
        Dashboard utama (Overview, Data Explorer, Visualisasi, Evaluasi) tetap berfungsi normal.
        """)
        return
        
    with st.spinner("Memeriksa kesiapan model Sentence Transformers & K-Means..."):
        embedder, kmeans, load_err = load_prediction_pipeline()
        
    if load_err or embedder is None or kmeans is None:
        st.error(f"""
        ⚠️ **Komponen Inferensi Belum Dapat Dimuat**
        Keterangan: {load_err}
        
        Silakan pastikan dependensi `sentence-transformers` dan `torch` terinstal dengan baik di lingkungan server.
        """)
        return
        
    st.success("✅ **Model Final Siap:** Menggunakan `paraphrase-multilingual-MiniLM-L12-v2` (384-d L2-normalized) dan K-Means final identik (k=10, random_state=42).")
    
    # 2. Input Ulasan Pengguna
    st.markdown("### 📝 Masukkan Teks Ulasan untuk Diuji")
    st.caption("Ulasan dapat berbahasa Indonesia maupun bahasa Inggris (model embedding mendukung lebih dari 50 bahasa).")
    
    # Contoh input cepat
    example_prompts = {
        "Pilih contoh teks...": "",
        "Contoh 1 (Keluhan Teknis / Crash)": "Aplikasi sering crash tiba-tiba setelah update versi terbaru dan data tidak tersimpan.",
        "Contoh 2 (Monetisasi / Versi Pro)": "Too expensive for the pro subscription, free version is way too limited now.",
        "Contoh 3 (Masalah Notifikasi & Alarm)": "Pengingat dan alarm sering tidak berbunyi tepat waktu saat HP dalam keadaan standby.",
        "Contoh 4 (Masalah Akun & Sinkronisasi)": "Failed to sync my notes with Google account, all my tasks are gone!",
        "Contoh 5 (Pujian Kemudahan Aplikasi)": "Very easy to use, simple interface and really helps my daily productivity. Love it!",
        "Contoh 6 (Manajemen Tugas / Fitur)": "Please add subtasks feature and calendar integration for daily checklist."
    }
    
    selected_example = st.selectbox("Coba Contoh Ulasan:", list(example_prompts.keys()))
    
    initial_text = example_prompts[selected_example] if selected_example != "Pilih contoh teks..." else ""
    
    user_review = st.text_area(
        "Teks Ulasan:",
        value=initial_text,
        height=110,
        placeholder="Ketik ulasan di sini... Contoh: 'Aplikasi ini sangat membantu mengatur jadwal harian, tapi kadang notifikasinya telat.'"
    )
    
    btn_predict = st.button("🚀 Prediksi Klaster Tematik", type="primary", use_container_width=True)
    
    if btn_predict:
        if not user_review.strip():
            st.warning("Silakan masukkan teks ulasan terlebih dahulu.")
            return
            
        with st.spinner("Memproses teks, membuat embedding semantik, dan memprediksi klaster..."):
            # 1. Preprocessing identik dengan notebook
            cleaned_text = clean_text(user_review)
            
            if not cleaned_text.strip():
                st.error("Teks ulasan tidak memuat karakter alfabet yang valid setelah dibersihkan dari simbol/tanda baca.")
                return
                
            # 2. Encode ulasan menggunakan SentenceTransformer (L2 normalized)
            review_vector = embedder.encode(
                [cleaned_text],
                normalize_embeddings=True
            )
            
            # 3. Prediksi klaster dengan K-Means
            predicted_cluster = int(kmeans.predict(review_vector)[0])
            meta = CLUSTER_METADATA.get(predicted_cluster, {})
            
            # 4. Hitung jarak Euclidean dan Cosine Similarity ke sentroid klaster
            centroid = kmeans.cluster_centers_[predicted_cluster]
            euclidean_dist = float(np.linalg.norm(review_vector[0] - centroid))
            # Karena vektor dan sentroid ternormalisasi, cosine sim = dot product
            norm_centroid = centroid / np.linalg.norm(centroid)
            cosine_sim = float(np.dot(review_vector[0], norm_centroid))
            
        # Tampilkan Hasil Prediksi
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("### 🎯 Hasil Prediksi Klaster")
        
        st.markdown(f"""
        <div style="background: white; border: 1px solid #E2E8F0; border-top: 5px solid {meta['warna']}; border-radius: 14px; padding: 1.4rem; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 1.25rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.8rem;">
                <div>
                    <span style="background: {meta['warna']}20; color: {meta['warna']}; font-weight: 800; font-size: 0.82rem; padding: 0.25rem 0.65rem; border-radius: 9999px;">
                        HASIL: CLUSTER {predicted_cluster}
                    </span>
                    <h3 style="margin: 0.5rem 0 0.2rem 0; color: #0F172A; font-weight: 800; font-size: 1.4rem;">{meta['name']}</h3>
                </div>
                <div style="text-align: right; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.4rem 0.8rem;">
                    <div style="font-size: 0.75rem; color: #64748B; font-weight: 600;">KEMIRIPAN SENTROID</div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: #0F172A;">{cosine_sim:.4f} <span style="font-size: 0.75rem; font-weight: 500; color: #64748B;">(Cosine)</span></div>
                </div>
            </div>
            <div style="font-size: 0.95rem; color: #334155; line-height: 1.6; margin-bottom: 0.9rem;">
                <b>Tema Penafsiran:</b> <i>{meta['tema']}</i><br>
                <b>Deskripsi Klaster:</b> {meta['deskripsi']}
            </div>
            <div style="display: flex; gap: 1.5rem; flex-wrap: wrap; font-size: 0.85rem; color: #475569; padding-top: 0.75rem; border-top: 1px solid #F1F5F9;">
                <span>📊 <b>Ukuran Klaster:</b> {meta['n_ulasan']:,} ulasan ({meta['persentase']}%)</span>
                <span>⭐ <b>Rata-rata Rating Historis:</b> {meta['rata_rata_rating']} ★</span>
                <span>🔻 <b>Rating Rendah:</b> {meta['pct_rating_1_2']}%</span>
                <span>🔺 <b>Rating Tinggi:</b> {meta['pct_rating_4_5']}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Detail Metrik Kedekatan
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("**Kata Kunci Representatif Klaster Ini:**")
            render_keyword_tags(meta['kata_kunci'])
        with col_m2:
            st.markdown("**Jarak ke Pusat Klaster (Metrik Eksak):**")
            st.caption(f"- Jarak Euclidean ke Sentroid: `{euclidean_dist:.4f}`")
            st.caption(f"- Cosine Similarity ke Sentroid: `{cosine_sim:.4f}`")
            st.caption("*Catatan: Nilai di atas adalah ukuran kedekatan jarak geometris dalam ruang vektor, bukan nilai probabilitas kelas.*")
            
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        # 5. Ulasan Serupa dari Klaster Tersebut
        st.markdown("### 🔍 Contoh Ulasan Serupa dari Dataset Asli")
        st.caption(f"Contoh ulasan riil dari dataset yang tergolong ke dalam Cluster {predicted_cluster}:")
        
        cluster_samples = df[df['cluster_semantik_10'] == predicted_cluster].sample(n=min(3, (df['cluster_semantik_10'] == predicted_cluster).sum()), random_state=123)
        
        for _, s_row in cluster_samples.iterrows():
            st.markdown(f"""
            <div class="review-quote" style="border-left-color: {meta['warna']};">
                <div style="font-weight: 700; color: #0F172A; margin-bottom: 0.2rem;">
                    Rating {s_row['score']} ★ — {s_row['app_name']}
                </div>
                <div>"{s_row['content']}"</div>
            </div>
            """, unsafe_allow_html=True)
