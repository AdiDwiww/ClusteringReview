import streamlit as st
import pandas as pd
from modules.ui_theme import render_hero_banner

def show(df: pd.DataFrame):
    render_hero_banner(
        title="Tentang Penelitian & Metodologi",
        subtitle="Dokumentasi komprehensif latar belakang, tahapan prapemrosesan, metodologi representasi semantik, hasil utama, keterbatasan, dan rekomendasi praktis.",
        tag="Research Documentation"
    )
    
    # 1. Judul & Informasi Peneliti
    st.markdown("""
    ### 📖 Judul Penelitian
    **"Clustering Ulasan Aplikasi Produktivitas di Google Play Store Menggunakan Sentence Transformers dan K-Means"**
    """)
    
    col_meta1, col_meta2 = st.columns(2)
    with col_meta1:
        st.markdown("""
        - **Kategori Studi:** Data Science / Natural Language Processing (NLP) / Unsupervised Learning
        - **Dataset Sumber:** Ulasan Pengguna Google Play Store (15 Aplikasi Produktivitas)
        - **Ukuran Dataset Mentah:** 12.495 baris × 12 kolom
        - **Ukuran Dataset Bersih:** 11.713 baris × 19 kolom
        """)
    with col_meta2:
        st.markdown("""
        - **Model Representasi Utama:** `paraphrase-multilingual-MiniLM-L12-v2` (384 Dimensi, L2-normalized)
        - **Algoritma Pengelompokan:** K-Means Clustering (`k=10`, `n_init=10`, `random_state=42`)
        - **Metrik Evaluasi Utama:** Silhouette Coefficient (Cosine Distance, subsampel 3.000 titik)
        - **Skor Silhouette Akhir:** **0.0831** (pada k=10; k=2: 0.1280)
        """)
        
    st.markdown("---")
    
    # 2. Latar Belakang & Rumusan Masalah
    st.markdown("### 🎯 1. Latar Belakang & Tujuan Penelitian")
    st.markdown("""
    Ulasan pengguna di toko aplikasi digital seperti Google Play Store merupakan sumber umpan balik berharga bagi pengembang perangkat lunak untuk mengevaluasi kualitas produk, mendeteksi cacat perangkat lunak (bugs), memahami friksi harga, serta memetakan fitur yang diinginkan pengguna.
    
    Namun, volume ulasan yang mencapai puluhan ribu ulasan per aplikasi tidak memungkinkan untuk dibaca dan diklasifikasikan secara manual. Oleh karena itu, diperlukan teknik pengelompokan tanpa supervisi (*unsupervised clustering*) untuk mengelompokkan ulasan secara otomatis ke dalam tema-tema dominan.
    
    **Tujuan Utama Penelitian:**
    1. Membangun pipeline prapemrosesan teks yang efisien untuk ulasan aplikasi produktivitas lintas bahasa.
    2. Membandingkan performa representasi teks leksikal tradisional (TF-IDF) dengan representasi embedding berbasis transformer multibahasa (*Sentence-BERT*).
    3. Mengelompokkan 11.713 ulasan ke dalam klaster semantik menggunakan algoritma K-Means.
    4. Menginterpretasikan tema-tema ulasan aktual dan menganalisis hubungannya secara deskriptif dengan skor rating pengguna.
    """)
    
    # 3. Karakteristik Dataset & Preprocessing
    st.markdown("### 🧹 2. Sumber Data & Tahapan Prapemrosesan (Preprocessing)")
    st.markdown("""
    Dataset awal diperoleh dari hasil scraping ulasan Google Play Store untuk 15 aplikasi produktivitas populer:
    *Habitica, Todoist, Any.do, HabitBull, Business Calendar 2, TickTick, Planner Pro, Microsoft To Do, TimeTune, Forest, Sectograph, Tasks, LifeRPG, HabitNow, dan Artful Agenda.*
    
    Sesuai implementasi pada notebook penelitian (Cell 1–3), prapemrosesan dilakukan melalui tahapan runtut:
    1. **Pemeriksaan Kualitas Awal:** Mengidentifikasi data kosong (*missing values*) dan duplikasi. Kolom `reviewCreatedVersion` memiliki 2.010 data kosong, sedangkan `replyContent` dan `repliedAt` masing-masing memiliki 6.090 data kosong (karena tidak semua ulasan dibalas developer). Kolom inti (`content`, `score`, `appId`) bersih 100%.
    2. **Pembersihan Duplikasi:** Menghapus **688 ulasan duplikat** berdasarkan kemiripan teks isi (`content`).
    3. **Pembersihan Teks (*Text Cleaning*):**
       - Mengubah huruf menjadi huruf kecil (*case folding / lowercase*).
       - Menghapus tautan URL (`http...` / `www...`).
       - Menghapus karakter selain alfabet latin `a-z` dan spasi (menghilangkan emoji, simbol khusus, angka, dan tanda baca).
       - Menormalisasi spasi berlebih menjadi satu spasi tunggal.
    4. **Penyaringan Teks Kosong:** Membuang **94 ulasan** yang menjadi kosong setelah dibersihkan (hanya memuat emoji/simbol), menyisakan **11.713 ulasan final** siap analisis.
    """)
    
    # 4. Metodologi: Sentence Transformers vs TF-IDF & K-Means
    st.markdown("### 🔬 3. Metodologi Representasi & Algoritma Clustering")
    st.markdown("""
    - **Representasi TF-IDF (Term Frequency – Inverse Document Frequency):**
      Diuji sebagai baseline komparatif melalui 3 konfigurasi parameter (Unigram dasar, Uni+Bigram selektif, dan Stopwords kustom). Pendekatan ini menghasilkan matriks berdimensi tinggi yang sangat renggang (*sparse*) dan mengalami kegagalan pemisahan topik di mana satu klaster dominan menyerap lebih dari 56% hingga 65% total ulasan dengan nilai Silhouette score sangat rendah (0.003 – 0.018).
    - **Sentence Transformers (`paraphrase-multilingual-MiniLM-L12-v2`):**
      Model berbasis Siamese BERT architecture yang mentranslasikan kalimat utuh menjadi vektor berdimensi tetap (**384 dimensi**). Dilakukan *L2-normalization* pada vektor keluaran sehingga jarak Euclidean kuadrat berbanding lurus dengan jarak kosinus (*cosine distance*). Mampu menangkap makna semantik, sinonim konteks, dan sifat multibahasa ulasan.
    - **K-Means Clustering:**
      Membagi data ke dalam *k* kelompok dengan meminimalkan varians intra-klaster (*inertia*). Diinisialisasi dengan teknik `k-means++` untuk persebaran awal sentroid yang optimal, dengan parameter `random_state=42`, `n_init=10`, dan `max_iter=300`.
    """)
    
    # 5. Hasil Utama Penelitian
    st.markdown("### 🏆 4. Hasil Utama Penelitian")
    st.markdown("""
    1. **Peningkatan Kualitas Pengelompokan:** Sentence Transformers melipatgandakan nilai Silhouette Score hingga 5–10 kali lebih tinggi dibandingkan representasi leksikal TF-IDF (dari kisaran ~0.01 menjadi ~0.08–0.12).
    2. **Pemetaan 10 Tema Ulasan:**
       - **Masalah Teknis & Keandalan:** Klaster 1 (*crash* dan kegagalan fungsi aplikasi pasca-update) dan Klaster 6 (kegagalan alarm/pengingat waktu).
       - **Krisis Akun & Data:** Klaster 5 (kegagalan sinkronisasi cloud dan login email, berating terendah: 1.90 ★).
       - **Monetisasi & Model Bisnis:** Klaster 2 (ketidakpuasan biaya langganan versi Pro/Premium).
       - **Alur Kerja Fitur:** Klaster 3 (pengelolaan daftar tugas) dan Klaster 9 (integrasi event kalender).
       - **Kepuasan & Penerimaan:** Klaster 4 (kemudahan operasional/UI simpel) dan Klaster 8 (testimoni positif aplikasi terbaik, ukuran terbesar: 17.7%).
    """)
    
    # 6. Keterbatasan Penelitian (Berdasarkan Laporan Resmi)
    st.markdown("### ⚠️ 5. Keterbatasan Penelitian")
    st.warning("""
    Sesuai dokumentasi pada laporan penelitian resmi, temuan penelitian ini memiliki sejumlah batasan metodologis yang penting untuk diperhatikan:
    
    1. **Pemisahan Klaster Lemah secara Geometri:** Seluruh skor Silhouette berada di bawah 0.13, dan pada model terpilih k=10 bernilai 0.0831. Ini menunjukkan bahwa teks ulasan pengguna di dunia nyata membentuk spektrum leksikal-semantik yang kontinu tanpa batas pemisah yang tajam (*dense overlapping cloud*).
    2. **Bukan Klasifikasi Sentimen Resmi:** ID Klaster yang dihasilkan K-Means adalah murni kelompok topik semantik tanpa supervisi (*unsupervised cluster*), bukan label sentimen positif/negatif resmi. Hubungan klaster dengan skor rating bersifat agregasi deskriptif.
    3. **Generalisasi Lintas 15 Aplikasi:** Dataset mencakup ulasan dari 15 aplikasi produktivitas yang berbeda secara bersamaan, sehingga tema yang terbentuk bersifat umum lintas aplikasi (*cross-application patterns*) dan belum tentu merepresentasikan kendala spesifik arsitektur satu aplikasi tunggal.
    4. **Subjektivitas Pelabelan Tema:** Penamaan tema klaster dilakukan melalui penafsiran manual peneliti dengan membaca kata kunci teratas TF-IDF dan sampel ulasan autentik, sehingga tetap mengandung elemen interpretasi kualitatif.
    """)
    
    # 7. Rekomendasi untuk Pengembang Aplikasi
    st.markdown("### 💡 6. Rekomendasi Praktis bagi Pengembang Aplikasi")
    st.success("""
    Berdasarkan data ulasan aktual, rekomendasi prioritas bagi pengembang aplikasi produktivitas meliputi:
    1. **Prioritas Stabilitas Sinkronisasi Cloud (Cluster 5):** Menjamin keandalan sinkronisasi offline-first dan penanganan token akun, karena kegagalan sinkronisasi memicu penurunan rating paling parah (rata-rata 1.90).
    2. **Audit Regresi sebelum Rilis Pembaruan (Cluster 1):** Meningkatkan pengujian kompatibilitas pada berbagai tipe perangkat Android untuk mencegah gelombang ulasan bintang 1 akibat *crash* pasca-update.
    3. **Penyelarasan Izin Sistem Operasi untuk Alarm (Cluster 6):** Menyediakan panduan transparan di dalam aplikasi bagi pengguna untuk menonaktifkan optimasi baterai OS (*battery optimization whitelist*) agar notifikasi pengingat tidak terbunuh sistem.
    4. **Transparansi Model Monetisasi (Cluster 2):** Menjelaskan secara tegas fitur apa saja yang masuk paket gratis vs Pro, serta menghindari pemindahan fitur gratis yang sudah ada ke paket berbayar secara mendadak.
    """)
    
    st.markdown("---")
    st.caption("""
    **Referensi Akademik Terkait:**
    - Arthur, D., & Vassilvitskii, S. (2007). *k-means++: The advantages of careful seeding.* Proceedings of SODA '07.
    - Reimers, N., & Gurevych, I. (2019). *Sentence-BERT: Sentence embeddings using Siamese BERT-networks.* Proceedings of EMNLP-IJCNLP.
    - Reimers, N., & Gurevych, I. (2020). *Making monolingual sentence embeddings multilingual using knowledge distillation.* Proceedings of EMNLP.
    """)
