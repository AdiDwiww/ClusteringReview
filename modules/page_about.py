import streamlit as st
import pandas as pd
from modules.ui_theme import render_workspace_header, render_section_title
from modules.icons import icon_svg

def show(df: pd.DataFrame):
    render_workspace_header(
        title="Dokumentasi & Metodologi Penelitian",
        subtitle="Spesifikasi ilmiah, sumber data, prapemrosesan teks, arsitektur Sentence Transformers, K-Means, kesimpulan, dan keterbatasan metodologis.",
        category="Academic Dashboard",
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
    
    # 2. Sumber Dataset & Karakteristik Korpus
    render_section_title("1. Sumber Dataset & Karakteristik Korpus", "Distribusi aplikasi dan latar belakang pengumpulan data.", icon="database")
    st.markdown("""
    Data ulasan dikumpulkan dari toko aplikasi resmi <b>Google Play Store</b> mencakup <b>15 aplikasi produktivitas populer</b>:
    <i>Habitica, Todoist, Any.do, HabitBull, Business Calendar 2, TickTick, Planner Pro, Microsoft To Do, TimeTune, Forest, Sectograph, Tasks, LifeRPG, HabitNow, dan Artful Agenda</i>.
    
    Total data mentah hasil *scraping* berjumlah <b>12.495 ulasan</b> dengan 12 fitur metadata (antara lain <code>content</code>, <code>score</code>, <code>appId</code>, <code>at</code>, <code>thumbsUpCount</code>, <code>reviewCreatedVersion</code>, dll).
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    
    # 3. Prapemrosesan Teks (Preprocessing)
    render_section_title("2. Tahapan Prapemrosesan Data (Preprocessing)", "Pipeline pembersihan data terstandarisasi untuk memastikan integritas representasi vektor.", icon="sliders-horizontal")
    st.markdown("""
    Tahapan prapemrosesan teks dilaksanakan secara berurutan sesuai implementasi notebook penelitian:
    1. <b>Pemeriksaan Nilai Hilang (Missing Values):</b> Kolom <code>reviewCreatedVersion</code> memiliki 2.010 data kosong; <code>replyContent</code> dan <code>repliedAt</code> memiliki 6.090 data kosong. Kolom primer untuk analisis (<code>content</code>, <code>score</code>, <code>appId</code>) berstatus 100% lengkap tanpa data kosong.
    2. <b>Pembersihan Duplikasi:</b> Menghapus <b>688 ulasan duplikat</b> berdasarkan kemiripan teks isi ulasan (<code>content</code>), mengurangi data dari 12.495 menjadi 11.807 baris.
    3. <b>Pembersihan Teks (Text Cleaning):</b>
       - Mengubah seluruh karakter ke huruf kecil (<i>case folding</i>).
       - Menghapus tautan web (<i>URL regex: http/www</i>).
       - Menghapus karakter selain alfabet latin <code>a-z</code> dan spasi (menyaring emoji, angka, tanda baca, dan karakter non-alfabet).
       - Menormalisasi spasi ganda atau spasi berlebih menjadi spasi tunggal yang rapi.
    4. <b>Penyaringan Teks Kosong Pasca Pembersihan:</b> Membuang <b>94 ulasan</b> yang menjadi string kosong setelah pembersihan emoji/simbol, menghasilkan korpus akhir berkategori valid sebanyak <b>11.713 ulasan</b>.
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    
    # 4. Sentence Transformers & K-Means
    render_section_title("3. Sentence Transformers & Algoritma K-Means", "Metodologi transformasi semantik dan optimasi pengelompokan tanpa supervisi.", icon="cpu")
    st.markdown("""
    - <b>Sentence Transformers (paraphrase-multilingual-MiniLM-L12-v2):</b>
      Mengekstraksi representasi semantik ulasan ke dalam ruang vektor padat berdimensi <b>384</b>. Menggunakan arsitektur <i>Siamese BERT-networks</i> yang dilatih melalui teknik <i>knowledge distillation</i>, model ini mampu memahami sinonim, konteks kalimat utuh, serta menangani ulasan berbahasa Indonesia maupun Inggris secara simultan tanpa distorsi matriks renggang. Setiap vektor dinormalisasi menggunakan norma Euclidean (L2-norm) sehingga jarak Euclidean berbanding lurus dengan jarak kosinus.
    - <b>Algoritma K-Means Clustering:</b>
      Mengelompokkan 11.713 vektor embedding ke dalam <b>k = 10 klaster</b> dengan meminimalkan inersia (<i>within-cluster sum-of-squares</i>). Menggunakan inisialisasi titik pusat <code>k-means++</code> untuk mempercepat konvergensi dan mencegah jebakan lokal minimum, dengan parameter <code>n_init=10</code>, <code>max_iter=300</code>, dan seed reproduktibilitas <code>random_state=42</code>.
    - <b>Ekstraksi Kata Kunci Leksikal (TF-IDF):</b>
      Guna mempermudah interpretasi manusia terhadap setiap klaster, diekstraksi kata kunci representatif menggunakan rata-rata bobot TF-IDF (5.000 fitur unigram+bigram, min_df=5) yang dihitung secara independen pada teks ulasan masing-masing klaster.
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    
    # 5. Kesimpulan Penelitian
    render_section_title("4. Kesimpulan Penelitian & Rekomendasi Industri", "Sintesis temuan utama dan implikasi manajerial bagi pengembang aplikasi.", icon="check-circle-2")
    
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.markdown("""
        <div class="saas-card" style="border-left: 3px solid #4F46E5; height: 100%;">
            <div style="font-weight: 700; color: #09090B; font-size: 0.95rem; margin-bottom: 0.5rem;">
                Kesimpulan Metodologis & Analitis
            </div>
            <ul style="font-size: 0.84rem; color: #3F3F46; line-height: 1.6; padding-left: 1.15rem; margin: 0;">
                <li style="margin-bottom: 0.45rem;">
                    <b>Keunggulan Semantik:</b> Representasi Sentence Transformers berhasil memecahkan kelemahan fatal TF-IDF (yang sebelumnya terjebak dalam satu klaster dominan >60%), menghasilkan pembagian klaster yang jauh lebih proporsional (klaster terbesar hanya 17.7%).
                </li>
                <li style="margin-bottom: 0.45rem;">
                    <b>Resolusi Operasional pada k=10:</b> Pemilihan k=10 terbukti optimal dalam membedakan berbagai jenis masalah teknis dan aspek produk yang sebelumnya tercampur jika menggunakan k=2.
                </li>
                <li>
                    <b>Korelasi Topik & Rating:</b> Terdapat korelasi kuat antara topik ulasan dan sentimen kepuasan. Masalah integritas data pengguna (sinkronisasi akun C5) menjadi penyebab rating terendah (1.90 / 5.0).
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_k2:
        st.markdown("""
        <div class="saas-card" style="border-left: 3px solid #059669; height: 100%;">
            <div style="font-weight: 700; color: #09090B; font-size: 0.95rem; margin-bottom: 0.5rem;">
                Rekomendasi Tindakan bagi Pengembang
            </div>
            <ul style="font-size: 0.84rem; color: #3F3F46; line-height: 1.6; padding-left: 1.15rem; margin: 0;">
                <li style="margin-bottom: 0.45rem;">
                    <b>Prioritas Stabilitas Sinkronisasi Cloud (Cluster 5):</b> Kegagalan sinkronisasi memicu resistensi pengguna paling tinggi. Diperlukan penanganan offline-first dan audit berkala pada gateway login.
                </li>
                <li style="margin-bottom: 0.45rem;">
                    <b>Uji Regresi Pembaruan Versi (Cluster 1):</b> Hindari rilis pembaruan yang memicu crash aplikasi, karena cluster masalah teknis menyerap 14.2% total ulasan dengan rating 2.11.
                </li>
                <li>
                    <b>Transparansi Kebijakan Fitur Pro (Cluster 2):</b> Hindari mengunci fitur dasar yang sebelumnya gratis menjadi berbayar secara sepihak untuk mencegah gelombang ulasan bintang 1.
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    
    # 6. Keterbatasan Penelitian
    render_section_title("5. Keterbatasan Penelitian", "Batasan metodologis formal yang harus diperhatikan dalam menafsirkan temuan.", icon="alert-triangle")
    
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E4E4E7; border-left: 3px solid #D97706; border-radius: 8px; padding: 1.1rem; font-size: 0.85rem; color: #3F3F46; line-height: 1.65;">
        <ol style="margin: 0; padding-left: 1.2rem;">
            <li style="margin-bottom: 0.5rem;">
                <b>Pemisahan Geometri Lemah (Awan Semantik Kontinu):</b> Seluruh skor Silhouette berada pada rentang di bawah 0.13 (k=10 bernilai 0.0831). Hal ini mencerminkan karakteristik alami teks ulasan pengguna nyata yang membentuk awan semantik kontinu tanpa batas partisi ruang yang terpisah secara tegas.
            </li>
            <li style="margin-bottom: 0.5rem;">
                <b>Sifat Unsupervised (Bukan Klasifikasi Sentimen):</b> ID klaster yang dihasilkan K-Means murni kelompok kemiripan topik semantik tanpa supervisi, bukan label sentimen formal (positif/negatif kaku).
            </li>
            <li style="margin-bottom: 0.5rem;">
                <b>Generalisasi Agregat Lintas 15 Aplikasi:</b> Korpus data mencakup ulasan dari 15 aplikasi berbeda secara gabungan, sehingga klaster mencerminkan dinamika industri aplikasi produktivitas secara makro, bukan arsitektur internal satu aplikasi spesifik.
            </li>
            <li>
                <b>Subjektivitas Interpretasi Kualitatif:</b> Pelabelan nama klaster dan penafsiran tema dilakukan secara kualitatif oleh peneliti berdasarkan inspeksi kata kunci TF-IDF teratas dan sampel ulasan autentik.
            </li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    st.caption("""
    Referensi Literatur Utama:
    • Arthur, D., & Vassilvitskii, S. (2007). k-means++: The advantages of careful seeding. SODA '07.
    • Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese BERT-networks. EMNLP-IJCNLP.
    • Reimers, N., & Gurevych, I. (2020). Making monolingual sentence embeddings multilingual using knowledge distillation. EMNLP.
    """)
