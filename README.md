# Clustering Ulasan Aplikasi Produktivitas di Google Play Store
### Menggunakan Sentence Transformers dan K-Means

Aplikasi web Data Science interaktif yang dibangun dengan **Streamlit** untuk mengeksplorasi, memvisualisasikan, dan menguji hasil clustering semantik ulasan pengguna dari 15 aplikasi produktivitas populer di Google Play Store.

Proyek ini merepresentasikan implementasi penuh dari penelitian:
> *"Clustering Ulasan Aplikasi Produktivitas di Google Play Store Menggunakan Sentence Transformers dan K-Means"*

---

## 🌟 Fitur Utama Dashboard

Aplikasi memiliki antarmuka modern, profesional, dan responsif berbahasa Indonesia dengan 7 halaman navigasi terstruktur:

1. **📊 Dashboard Overview:**
   - Ringkasan KPI: Total ulasan bersih (11.713), 15 aplikasi, 10 klaster, dan rata-rata rating (3.04 ★).
   - Distribusi skor rating bintang 1 hingga 5.
   - Donut chart proporsi ukuran setiap klaster.
   - Grafik batang komparasi rata-rata rating per klaster terhadap garis rata-rata global.
   - Ringkasan insight analitis aktual (klaster keluhan kritis vs klaster kepuasan pengguna).

2. **🔍 Eksplorasi Dataset:**
   - Filter dinamis berdasarkan nama aplikasi, rentang rating, dan klaster.
   - Mesin pencari teks ulasan langsung (*real-time keyword search*).
   - Statistik panjang ulasan (jumlah karakter dan jumlah kata).
   - Tabel data interaktif dengan navigasi paginasi (*pagination*) dan tombol unduh CSV terfilter.

3. **🧩 Cluster Explorer:**
   - Navigasi komparatif 10 klaster atau peninjauan mendalam per klaster (Cluster 0–9).
   - Metrik spesifik per klaster: ukuran ulasan, rata-rata, median, persentase ulasan negatif (1–2) dan positif (4–5).
   - Kata kunci representatif berdasarkan bobot TF-IDF klaster.
   - Sampel ulasan autentik dari dataset asli dengan filter rating sampel.
   - Interpretasi tema analitis berdasarkan isi ulasan nyata.

4. **📈 Visualisasi Interaktif:**
   - Komposisi bertingkat (*stacked bar chart*) distribusi rating pada tiap klaster.
   - Peringkat rata-rata rating dan matriks korelasi (*heatmap*) klaster pada 15 aplikasi.
   - Proyeksi scatter plot 2D menggunakan Principal Component Analysis (PCA) dengan catatan penjelasan reduksi dimensi.
   - Boxplot sebaran kuartil rating per klaster (replikasi Gambar 2 laporan penelitian).

5. **🚀 Uji Ulasan Baru (Model Inference):**
   - Formulir input ulasan baru (mendukung bahasa Indonesia dan bahasa Inggris).
   - Pipeline prapemrosesan teks identik dengan notebook (*case folding, URL removal, regex clean*).
   - Transformasi embedding semantik menggunakan `paraphrase-multilingual-MiniLM-L12-v2` (384 dimensi, *L2-normalized*).
   - Prediksi klaster menggunakan model K-Means final (100% *exact match* hasil rekonstruksi identik).
   - Menampilkan metrik kedekatan jarak geometris (Euclidean Distance & Cosine Similarity) serta contoh ulasan serupa di klaster tersebut.

6. **⚖️ Evaluasi Model:**
   - Evaluasi Silhouette Score komparatif (k=2 hingga k=10) dan metrik Inertia.
   - Perbandingan komprehensif 3 konfigurasi leksikal TF-IDF terhadap representasi Sentence Transformers (Tabel 4 & Tabel 6 laporan).
   - Pembahasan metodologis mendalam: Mengapa k=10 (0.0831) dipilih sebagai kompromi eksplorasi tema meskipun k=2 (0.1280) memiliki skor geometris tertinggi.

7. **📖 Tentang Penelitian:**
   - Dokumentasi lengkap latar belakang, tujuan penelitian, karakteristik dataset, metodologi NLP, hasil utama, 4 poin batasan penelitian, serta 4 rekomendasi praktis bagi pengembang aplikasi.

---

## 📁 Struktur Direktori Proyek

```text
ClusteringReview/
├── app.py                             # Entrypoint utama aplikasi Streamlit
├── requirements.txt                   # Dependensi pustaka Python
├── README.md                          # Dokumentasi proyek & panduan deployment
├── .gitignore                         # Konfigurasi pengabaian file Git
├── hasil_clustering_semantik_k10.csv   # Dataset final hasil clustering (11.713 baris)
├── models/                            # Artefak model hasil rekonstruksi identik
│   ├── cluster_centroids.npy          # Sentroid 10 klaster (15 KB)
│   ├── kmeans_model.joblib            # Model K-Means final terlatih (62 KB)
│   ├── pca_2d.npy                     # Koordinat proyeksi 2D PCA (93 KB)
│   └── reconstruction_diag.json       # Diagnostik akurasi rekonstruksi (100% match)
└── modules/                           # Modul arsitektur aplikasi
    ├── cluster_info.py                # Konstanta metadata 10 klaster & riset
    ├── data_loader.py                 # Pemuatan dataset, caching, & prapemrosesan teks
    ├── ui_theme.py                    # Desain CSS modern, kartu KPI, & komponen UI
    ├── page_overview.py               # Halaman 1: Dashboard Overview
    ├── page_dataset.py                # Halaman 2: Eksplorasi Dataset
    ├── page_cluster_explorer.py       # Halaman 3: Cluster Explorer
    ├── page_visualizations.py         # Halaman 4: Visualisasi Interaktif
    ├── page_test_review.py            # Halaman 5: Uji Ulasan Baru
    ├── page_evaluation.py             # Halaman 6: Evaluasi Model
    └── page_about.py                  # Halaman 7: Tentang Penelitian
```

---

## 💻 Panduan Menjalankan Aplikasi Secara Lokal

### 1. Prasyarat Sistem
- Python versi 3.10, 3.11, atau 3.12 terinstal di komputer.
- Koneksi internet aktif saat pertama kali menjalankan fitur prediksi ulasan baru (untuk mengunduh bobot model embedding `paraphrase-multilingual-MiniLM-L12-v2` ~470MB sekali saja ke dalam cache lokal).

### 2. Buat Lingkungan Virtual (Virtual Environment)

Buka terminal / PowerShell di folder proyek ini:

```bash
# Membuat virtual environment bernama .venv
python -m venv .venv

# Mengaktifkan virtual environment:
# Pada Windows PowerShell:
.venv\Scripts\Activate.ps1
# Pada Windows Command Prompt:
.venv\Scripts\activate.bat
# Pada macOS / Linux:
source .venv/bin/activate
```

### 3. Instal Dependensi

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi Streamlit

```bash
streamlit run app.py
```

Aplikasi akan otomatis terbuka di browser pada alamat:
`http://localhost:8501`

---

## ☁️ Panduan Deployment ke GitHub & Streamlit Community Cloud

Aplikasi ini telah dipersiapkan agar dapat langsung dipublikasikan secara gratis melalui **Streamlit Community Cloud**.

### Langkah 1: Unggah Proyek ke GitHub

1. Buat repositori baru di akun GitHub Anda (misal: `ClusteringReview`).
2. Inisialisasi dan push file proyek:
   ```bash
   git init
   git add app.py requirements.txt README.md .gitignore hasil_clustering_semantik_k10.csv models/ modules/
   git commit -m "feat: complete streamlit clustering data science app"
   git branch -M main
   git remote add origin https://github.com/AdiDwiww/ClusteringReview.git
   git push -u origin main
   ```

> ⚠️ **Catatan File yang Diunggah vs Tidak Diunggah:**
> - **File yang WAJIB diunggah:** `app.py`, `requirements.txt`, `README.md`, `.gitignore`, `hasil_clustering_semantik_k10.csv` (berukuran ~8 MB, aman di bawah limit 100 MB GitHub), folder `models/` (semua file di bawah 100 KB), dan folder `modules/`.
> - **File yang TIDAK PERLU diunggah:** folder `.venv/`, `__pycache__/`, dan file temporary. File `.ipynb` dan `.docx` dapat diikutsertakan sebagai arsip penelitian.

### Langkah 2: Deploy di Streamlit Community Cloud

1. Masuk ke [share.streamlit.io](https://share.streamlit.io) menggunakan akun GitHub Anda.
2. Klik tombol **"New app"**.
3. Pilih repositori GitHub Anda: `AdiDwiww/ClusteringReview`.
4. Atur:
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Klik **"Deploy!"**.
6. Streamlit Cloud akan membaca `requirements.txt`, menginstal dependensi secara otomatis, dan aplikasi akan tayang secara online dengan URL publik (contoh: `https://clusteringreview.streamlit.app`).

---

## 🔬 Spesifikasi Metodologi & Keaslian Data

- **Sumber Data Utama:** `hasil_clustering_semantik_k10.csv` (11.713 baris). Seluruh angka, persentase, rata-rata, dan median dihitung langsung dari data riil tanpa manipulasi atau data dummy.
- **Model Embedding:** `paraphrase-multilingual-MiniLM-L12-v2` (384 dimensi, L2-normalized).
- **Model K-Means:** `k=10`, `random_state=42`, `n_init=10`. Rekonstruksi menghasilkan **100.00% exact match** terhadap label pada CSV asli.
- **Silhouette Score:** Evaluasi k=10 adalah 0.0831 (k=2: 0.1280) menggunakan metrik *cosine distance* pada sampel 3.000 ulasan.

---

## 📜 Lisensi & Atribusi
Dikembangkan untuk keperluan akademis, portofolio Data Science, dan presentasi tugas kuliah.
Didukung oleh ekosistem Python, Streamlit, Scikit-Learn, PyTorch, Plotly, dan Hugging Face Sentence Transformers.
