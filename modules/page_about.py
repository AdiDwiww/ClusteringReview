import streamlit as st
import pandas as pd
from modules.ui_theme import render_workspace_header, render_section_title
from modules.icons import icon_svg

def show(df: pd.DataFrame):
    render_workspace_header(
        title="Dokumentasi & Metodologi Penelitian",
        subtitle="Spesifikasi ilmiah, tahapan prapemrosesan teks, arsitektur embedding transformer, hasil utama, keterbatasan, dan rekomendasi industri.",
        category="Research Documentation",
        icon="book-open"
    )
    
    # 1. Judul & Spesifikasi Penelitian
    st.markdown("""
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.15rem; font-weight: 700; color: #09090B; margin-bottom: 0.8rem;">
        Clustering Ulasan Aplikasi Produktivitas di Google Play Store Menggunakan Sentence Transformers dan K-Means
    </div>
    """, unsafe_allow_html=True)
    
    col_meta1, col_meta2 = st.columns(2)
    with col_meta1:
        st.markdown("""
        <div class="saas-card" style="height: 100%;">
            <div style="font-size: 0.76rem; font-weight: 700; color: #71717A; text-transform: uppercase; margin-bottom: 0.6rem;">
                Karakteristik Korpus Data
            </div>
            <ul style="font-size: 0.84rem; color: #3F3F46; line-height: 1.7; padding-left: 1.1rem; margin: 0;">
                <li><b>Domain Riset:</b> Natural Language Processing (NLP) / Unsupervised Learning</li>
                <li><b>Sumber Data:</b> Google Play Store (15 Aplikasi Produktivitas Populer)</li>
                <li><b>Dataset Mentah:</b> 12.495 baris × 12 kolom</li>
                <li><b>Dataset Bersih Final:</b> 11.713 baris × 19 kolom</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_meta2:
        st.markdown("""
        <div class="saas-card" style="height: 100%;">
            <div style="font-size: 0.76rem; font-weight: 700; color: #71717A; text-transform: uppercase; margin-bottom: 0.6rem;">
                Arsitektur Model & Metrik
            </div>
            <ul style="font-size: 0.84rem; color: #3F3F46; line-height: 1.7; padding-left: 1.1rem; margin: 0;">
                <li><b>Model Embedding:</b> <code>paraphrase-multilingual-MiniLM-L12-v2</code> (384d, L2-norm)</li>
                <li><b>Algoritma:</b> K-Means Clustering (k=10, k-means++, random_state=42, n_init=10)</li>
                <li><b>Metrik Evaluasi:</b> Silhouette Coefficient (Cosine Distance, subsampel 3.000 titik)</li>
                <li><b>Skor Evaluasi:</b> k=10: 0.0831 (k=2: 0.1280)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    
    # 2. Latar Belakang & Tujuan
    render_section_title("1. Latar Belakang & Tujuan Penelitian", "Motivasi penelitian dan perumusan masalah analisis ulasan pengguna.", icon="target")
    st.markdown("""
    Ulasan pengguna pada toko aplikasi digital seperti Google Play Store menyediakan umpan balik berharga bagi pengembang untuk mengevaluasi keandalan sistem, mendeteksi cacat perangkat lunak (*bug*), memahami resistensi biaya langganan, dan memprioritaskan fitur baru.
    
    Namun, volume ulasan yang mencapai puluhan ribu ulasan per aplikasi tidak memungkinkan untuk dibaca dan diklasifikasikan secara manual. Oleh sebab itu, diperlukan metode pengelompokan tanpa supervisi (*unsupervised clustering*) untuk memetakan tema-tema ulasan secara otomatis dan objektif.
    
    <b>Tujuan Utama Penelitian:</b>
    1. Membangun pipeline prapemrosesan teks yang efisien untuk ulasan aplikasi produktivitas lintas bahasa.
    2. Menguji keterbatasan representasi leksikal tradisional (TF-IDF) terhadap representasi embedding semantik modern (*Sentence-BERT*).
    3. Mengelompokkan 11.713 ulasan ke dalam 10 klaster temantik K-Means.
    4. Menganalisis korelasi deskriptif antara tema klaster dengan kecenderungan skor rating pengguna.
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    
    # 3. Prapemrosesan Teks
    render_section_title("2. Karakteristik Dataset & Prapemrosesan (Preprocessing)", "Implementasi tahapan pembersihan data sesuai sel 1–3 pada notebook riset.", icon="database")
    st.markdown("""
    Dataset mencakup 15 aplikasi produktivitas: <i>Habitica, Todoist, Any.do, HabitBull, Business Calendar 2, TickTick, Planner Pro, Microsoft To Do, TimeTune, Forest, Sectograph, Tasks, LifeRPG, HabitNow, dan Artful Agenda</i>.
    
    Tahapan prapemrosesan data:
    1. <b>Pemeriksaan Data Kosong:</b> Kolom <code>reviewCreatedVersion</code> memiliki 2.010 data kosong; <code>replyContent</code> dan <code>repliedAt</code> memiliki 6.090 data kosong. Kolom inti (<code>content</code>, <code>score</code>, <code>appId</code>) berstatus 100% lengkap.
    2. <b>Pembersihan Duplikasi:</b> Menghapus <b>688 ulasan duplikat</b> berdasarkan kemiripan teks isi ulasan (<code>content</code>).
    3. <b>Pembersihan Teks (Text Cleaning):</b>
       - Mengubah seluruh teks ke huruf kecil (<i>case folding</i>).
       - Menghapus tautan URL web (<code>http/www</code>).
       - Menghapus karakter selain alfabet latin <code>a-z</code> dan spasi (menyaring emoji, angka, dan simbol tanda baca).
       - Menormalisasi spasi ganda menjadi spasi tunggal.
    4. <b>Penyaringan Teks Kosong:</b> Membuang <b>94 ulasan</b> yang kosong setelah simbol/emoji dibersihkan, menghasilkan <b>11.713 ulasan final</b>.
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    
    # 4. Metodologi
    render_section_title("3. Metodologi Representasi & Algoritma", "Perbandingan matematis antara TF-IDF dan Sentence Transformers.", icon="cpu")
    st.markdown("""
    - <b>TF-IDF (Term Frequency – Inverse Document Frequency):</b> Diuji melalui 3 konfigurasi leksikal. Menghasilkan matriks renggang berdimensi tinggi yang gagal memisahkan topik secara proporsional, di mana satu klaster raksasa menyerap 56% hingga 65% total ulasan dengan skor Silhouette rendah (0.003 – 0.018).
    - <b>Sentence Transformers (paraphrase-multilingual-MiniLM-L12-v2):</b> Mentransformasikan kalimat utuh menjadi vektor padat berdimensi 384 dengan normalisasi L2. Menggunakan arsitektur Siamese BERT yang dilatih dengan knowledge distillation untuk menangkap makna semantik kalimat secara multibahasa.
    - <b>K-Means Clustering:</b> Mengelompokkan vektor embedding dengan meminimalkan varians intra-klaster (inersia) menggunakan inisialisasi <code>k-means++</code>, parameter <code>n_init=10</code>, dan <code>random_state=42</code>.
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    
    # 5. Keterbatasan Penelitian
    render_section_title("4. Keterbatasan Metodologis Penelitian", "Batasan formal yang tercantum dalam laporan penelitian resmi.", icon="alert-triangle")
    
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E4E4E7; border-left: 3px solid #D97706; border-radius: 8px; padding: 1.1rem; font-size: 0.85rem; color: #3F3F46; line-height: 1.65;">
        <ol style="margin: 0; padding-left: 1.2rem;">
            <li style="margin-bottom: 0.5rem;">
                <b>Pemisahan Geometri Lemah:</b> Seluruh skor Silhouette berada di bawah 0.13 (k=10 bernilai 0.0831). Hal ini membuktikan bahwa teks ulasan pengguna nyata membentuk awan semantik kontinu yang saling bertumpang tindih tanpa batas partisi yang tajam.
            </li>
            <li style="margin-bottom: 0.5rem;">
                <b>Bukan Model Klasifikasi Sentimen:</b> ID klaster yang dihasilkan K-Means adalah murni kelompok topik semantik tanpa supervisi (*unsupervised*), bukan label sentimen resmi.
            </li>
            <li style="margin-bottom: 0.5rem;">
                <b>Generalisasi Lintas 15 Aplikasi:</b> Korpus data mencakup ulasan dari 15 aplikasi berbeda secara simultan, sehingga tema yang terbentuk merepresentasikan tren industri secara agregat dan bukan spesifik arsitektur satu produk saja.
            </li>
            <li>
                <b>Subjektivitas Interpretasi:</b> Pelabelan nama tema dilakukan secara kualitatif oleh peneliti berdasarkan interpretasi kata kunci TF-IDF teratas dan sampel ulasan autentik.
            </li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    
    # 6. Rekomendasi
    render_section_title("5. Rekomendasi Praktis bagi Pengembang Produk", "Insight yang dapat ditindaklanjuti oleh tim engineering dan product management.", icon="check-circle-2")
    
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E4E4E7; border-left: 3px solid #059669; border-radius: 8px; padding: 1.1rem; font-size: 0.85rem; color: #3F3F46; line-height: 1.65;">
        <ol style="margin: 0; padding-left: 1.2rem;">
            <li style="margin-bottom: 0.5rem;">
                <b>Prioritas Keandalan Sinkronisasi Akun (Cluster 5):</b> Kegagalan sinkronisasi cloud menimbulkan sentimen paling negatif (rata-rata rating 1.90) karena risiko hilangnya data tugas harian pengguna.
            </li>
            <li style="margin-bottom: 0.5rem;">
                <b>Audit Regresi Pasca Pembaruan (Cluster 1):</b> Pengujian kompatibilitas rilis update harus diperketat untuk mencegah lonjakan ulasan bintang 1 akibat *crash* mendadak.
            </li>
            <li style="margin-bottom: 0.5rem;">
                <b>Edukasi Izin Sistem Operasi untuk Pengingat (Cluster 6):</b> Sediakan panduan in-app mengenai optimasi baterai OS agar alarm pengingat tidak terbunuh di latar belakang.
            </li>
            <li>
                <b>Transparansi Kebijakan Fitur Pro (Cluster 2):</b> Hindari pemindahan fitur gratis yang sudah ada ke dalam skema berbayar secara sepihak untuk meminimalkan friksi pengguna.
            </li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    st.caption("""
    Referensi Literatur:
    Arthur, D., & Vassilvitskii, S. (2007). k-means++: The advantages of careful seeding. SODA '07.
    Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese BERT-networks. EMNLP-IJCNLP.
    Reimers, N., & Gurevych, I. (2020). Making monolingual sentence embeddings multilingual using knowledge distillation. EMNLP.
    """)
