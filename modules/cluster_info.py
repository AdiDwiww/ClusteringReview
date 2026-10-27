"""
Metadata resmi dan hasil penelitian terverifikasi dari:
- Laporan Clustering Ulasan Aplikasi.docx
- Clustering_Ulasan_Aplikasi_final (1).ipynb
- hasil_clustering_semantik_k10.csv
"""

# Pemetaan ID Aplikasi ke Nama Aplikasi yang Ramah Pengguna
APP_NAME_MAP = {
    "com.habitrpg.android.habitica": "Habitica: Gamify Your Tasks",
    "com.todoist": "Todoist: To-Do List & Planner",
    "com.anydo": "Any.do - To do list & Calendar",
    "com.oristats.habitbull": "HabitBull - Habit Tracker",
    "com.appgenix.bizcal": "Business Calendar 2 Planner",
    "com.ticktick.task": "TickTick: To-do list & Tasks",
    "com.appxy.planner": "Planner Pro - Daily Planner",
    "com.microsoft.todos": "Microsoft To Do",
    "com.gmail.jmartindev.timetune": "TimeTune - Schedule Planner",
    "cc.forestapp": "Forest: Focus for Productivity",
    "prox.lab.calclock": "Sectograph - Visual Time Planner",
    "com.tasks.android": "Tasks: Todo list & Tasks",
    "com.levor.liferpgtasks": "LifeRPG - Gamify Life",
    "com.habitnow": "HabitNow Daily Routine Planner",
    "com.artfulagenda.app": "Artful Agenda"
}

# Informasi 10 Cluster Final (Tabel 5 Laporan Penelitian)
CLUSTER_METADATA = {
    0: {
        "id": 0,
        "name": "Penilaian Umum & Campuran",
        "tema": "Penilaian umum singkat; campuran keluhan dan saran (heterogen)",
        "kata_kunci": ["bad", "ads", "good", "pay", "complicated", "confusing"],
        "n_ulasan": 964,
        "persentase": 8.2,
        "rata_rata_rating": 2.43,
        "median_rating": 2.0,
        "pct_rating_1_2": 56.7,
        "pct_rating_4_5": 23.4,
        "kategori_sentimen_dominan": "Cenderung Negatif / Keluhan Campuran",
        "deskripsi": (
            "Ulasan berisi penilaian singkat dan umum mengenai kepuasan pengguna. "
            "Sering kali memuat kombinasi sentimen ambigu atau keluhan mengenai iklan (ads) "
            "dan antarmuka yang membingungkan atau terlalu rumit (complicated/confusing)."
        ),
        "warna": "#F59E0B" # Amber
    },
    1: {
        "id": 1,
        "name": "Masalah Teknis & Bug Aplikasi",
        "tema": "Masalah teknis dan fungsi aplikasi (crash, gagal menyimpan, tidak berfungsi, setelah pembaruan)",
        "kata_kunci": ["app", "phone", "update", "work", "use", "time"],
        "n_ulasan": 1658,
        "persentase": 14.2,
        "rata_rata_rating": 2.11,
        "median_rating": 2.0,
        "pct_rating_1_2": 68.6,
        "pct_rating_4_5": 13.2,
        "kategori_sentimen_dominan": "Sangat Negatif (Keluhan Teknis)",
        "deskripsi": (
            "Klaster terbesar kedua yang didominasi oleh keluhan kegagalan teknis. "
            "Pengguna melaporkan aplikasi macet (crash), tidak dapat dibuka di ponsel tertentu, "
            "gagal menyimpan data, atau malfungsi parah setelah melakukan pembaruan (update)."
        ),
        "warna": "#EF4444" # Red
    },
    2: {
        "id": 2,
        "name": "Model Bisnis, Versi Pro & Pembayaran",
        "tema": "Versi gratis vs premium/pro dan pembayaran",
        "kata_kunci": ["version", "free", "premium", "pro", "pay", "paid"],
        "n_ulasan": 929,
        "persentase": 7.9,
        "rata_rata_rating": 2.42,
        "median_rating": 2.0,
        "pct_rating_1_2": 58.6,
        "pct_rating_4_5": 21.7,
        "kategori_sentimen_dominan": "Cenderung Negatif (Monetisasi)",
        "deskripsi": (
            "Fokus pada friksi monetisasi. Pengguna mengkritik batasan fitur gratis yang terlalu ketat, "
            "biaya langganan yang dirasa mahal, sistem penagihan/refund, atau fitur yang sebelumnya "
            "gratis namun kemudian dipindahkan ke paket berbayar (pro/premium)."
        ),
        "warna": "#EC4899" # Pink
    },
    3: {
        "id": 3,
        "name": "Manajemen Tugas, Daftar & Integrasi",
        "tema": "Pengelolaan tugas dan daftar; saran fitur dan integrasi",
        "kata_kunci": ["tasks", "task", "list", "add", "day", "set"],
        "n_ulasan": 1304,
        "persentase": 11.1,
        "rata_rata_rating": 3.02,
        "median_rating": 3.0,
        "pct_rating_1_2": 38.0,
        "pct_rating_4_5": 41.3,
        "kategori_sentimen_dominan": "Netral / Konstruktif (Feature Request)",
        "deskripsi": (
            "Klaster dengan distribusi rating paling seimbang (rata-rata 3.02). "
            "Membahas alur kerja utama aplikasi produktivitas: menambah tugas harian, mengatur checklist, "
            "serta masukan konstruktif mengenai fitur pengorganisasian tugas dan integrasi jadwal."
        ),
        "warna": "#8B5CF6" # Violet
    },
    4: {
        "id": 4,
        "name": "Kemudahan Penggunaan & Manfaat Positif",
        "tema": "Kemudahan penggunaan dan manfaat (positif)",
        "kata_kunci": ["easy", "use", "simple", "helpful", "useful", "love"],
        "n_ulasan": 1207,
        "persentase": 10.3,
        "rata_rata_rating": 4.18,
        "median_rating": 4.0,
        "pct_rating_1_2": 7.0,
        "pct_rating_4_5": 82.4,
        "kategori_sentimen_dominan": "Sangat Positif (Kepuasan Pengguna)",
        "deskripsi": (
            "Ulasan positif yang menyoroti kegunaan praktis aplikasi. "
            "Pengguna memuji antarmuka yang sederhana, mudah dipelajari (easy to use), "
            "serta dampak nyata aplikasi dalam membantu produktivitas harian mereka."
        ),
        "warna": "#10B981" # Emerald Green
    },
    5: {
        "id": 5,
        "name": "Akun, Login & Sinkronisasi Cloud",
        "tema": "Akun, pendaftaran/login, sinkronisasi, dan data",
        "kata_kunci": ["account", "sync", "sign", "login", "email", "widget"],
        "n_ulasan": 1048,
        "persentase": 8.9,
        "rata_rata_rating": 1.90,
        "median_rating": 2.0,
        "pct_rating_1_2": 76.0,
        "pct_rating_4_5": 11.4,
        "kategori_sentimen_dominan": "Paling Kritis / Negatif (Kehilangan Data)",
        "deskripsi": (
            "Klaster dengan rata-rata rating terendah dalam penelitian (1.90). "
            "Didominasi masalah autentikasi: gagal login email, sinkronisasi antar perangkat macet, "
            "widget tidak terhubung ke server, hingga risiko kehilangan catatan/data pengguna."
        ),
        "warna": "#B91C1C" # Dark Red
    },
    6: {
        "id": 6,
        "name": "Notifikasi, Pengingat & Alarm",
        "tema": "Notifikasi, pengingat, dan alarm",
        "kata_kunci": ["notifications", "reminders", "alarm", "sound"],
        "n_ulasan": 771,
        "persentase": 6.6,
        "rata_rata_rating": 2.41,
        "median_rating": 2.0,
        "pct_rating_1_2": 55.5,
        "pct_rating_4_5": 18.6,
        "kategori_sentimen_dominan": "Cenderung Negatif (Fungsi Pengingat)",
        "deskripsi": (
            "Membahas keandalan pengingat waktu. Pengguna mengeluhkan alarm tidak berbunyi, "
            "notifikasi terlambat muncul (sering terhambat optimasi baterai OS), suara alarm tidak bersuara, "
            "atau volume yang tidak dapat dikustomisasi."
        ),
        "warna": "#D97706" # Dark Amber
    },
    7: {
        "id": 7,
        "name": "Apresiasi Singkat (Short Praise)",
        "tema": "Pujian sangat singkat (median 2 kata)",
        "kata_kunci": ["good", "great", "nice", "love", "amazing", "awesome"],
        "n_ulasan": 744,
        "persentase": 6.4,
        "rata_rata_rating": 4.02,
        "median_rating": 4.0,
        "pct_rating_1_2": 13.4,
        "pct_rating_4_5": 75.4,
        "kategori_sentimen_dominan": "Positif Singkat",
        "deskripsi": (
            "Kumpulan ulasan positif yang sangat ringkas dengan median panjang teks hanya 2 kata. "
            "Contoh umum: 'Good app', 'Great', 'Nice'. Klaster ini terpisah dari klaster 8 "
            "terutama karena pola sintaksis dan panjang teks ulasan yang amat pendek."
        ),
        "warna": "#06B6D4" # Cyan
    },
    8: {
        "id": 8,
        "name": "Pujian Umum & Rekomendasi Aplikasi",
        "tema": "Ulasan positif umum",
        "kata_kunci": ["app", "great", "good", "love", "great app", "best"],
        "n_ulasan": 2079,
        "persentase": 17.7,
        "rata_rata_rating": 4.20,
        "median_rating": 4.0,
        "pct_rating_1_2": 8.0,
        "pct_rating_4_5": 81.7,
        "kategori_sentimen_dominan": "Sangat Positif (Klaster Terbesar)",
        "deskripsi": (
            "Klaster terbesar dalam dataset (17.7% ulasan) dengan rata-rata rating tertinggi (4.20). "
            "Menampung testimoni positif umum yang menyatakan aplikasi ini terbaik di kelasnya, "
            "sangat direkomendasikan, dan sangat memuaskan pengguna."
        ),
        "warna": "#3B82F6" # Blue
    },
    9: {
        "id": 9,
        "name": "Kalender, Agenda & Sinkronisasi Jadwal",
        "tema": "Kalender, acara, sinkronisasi; contoh ulasan banyak menyinggung iklan",
        "kata_kunci": ["calendar", "google calendar", "events", "sync"],
        "n_ulasan": 1009,
        "persentase": 8.6,
        "rata_rata_rating": 2.88,
        "median_rating": 3.0,
        "pct_rating_1_2": 44.2,
        "pct_rating_4_5": 36.6,
        "kategori_sentimen_dominan": "Campuran / Spesifik Fitur Kalender",
        "deskripsi": (
            "Fokus pada fitur kalender, pengelolaan event/agenda bulanan/mingguan, "
            "serta integrasi kalender pihak ketiga (terutama Google Calendar). "
            "Ulasan juga kerap menyinggung gangguan penempatan iklan pada tampilan kalender."
        ),
        "warna": "#6366F1" # Indigo
    }
}

# Data Evaluasi K-Means pada Embedding Sentence Transformers (Tabel 6 Laporan)
EVAL_EMBEDDING_DATA = [
    {"k": 2, "silhouette": 0.1280, "inertia": 8282.58, "cluster_terbesar": 6188, "cluster_terkecil": 5525, "is_best_silhouette": True, "is_selected": False},
    {"k": 3, "silhouette": 0.1021, "inertia": 7920.43, "cluster_terbesar": 4437, "cluster_terkecil": 3006, "is_best_silhouette": False, "is_selected": False},
    {"k": 4, "silhouette": 0.0879, "inertia": 7657.73, "cluster_terbesar": 3373, "cluster_terkecil": 2507, "is_best_silhouette": False, "is_selected": False},
    {"k": 5, "silhouette": 0.0753, "inertia": 7506.14, "cluster_terbesar": 2623, "cluster_terkecil": 1924, "is_best_silhouette": False, "is_selected": False},
    {"k": 6, "silhouette": 0.0754, "inertia": 7376.60, "cluster_terbesar": 2413, "cluster_terkecil": 1494, "is_best_silhouette": False, "is_selected": False},
    {"k": 7, "silhouette": 0.0778, "inertia": 7268.19, "cluster_terbesar": 2292, "cluster_terkecil": 1118, "is_best_silhouette": False, "is_selected": False},
    {"k": 8, "silhouette": 0.0755, "inertia": 7173.17, "cluster_terbesar": 2155, "cluster_terkecil": 1008, "is_best_silhouette": False, "is_selected": False},
    {"k": 9, "silhouette": 0.0818, "inertia": 7085.76, "cluster_terbesar": 2137, "cluster_terkecil": 772, "is_best_silhouette": False, "is_selected": False},
    {"k": 10, "silhouette": 0.0831, "inertia": 7016.81, "cluster_terbesar": 2079, "cluster_terkecil": 744, "is_best_silhouette": False, "is_selected": True}
]

# Perbandingan Eksperimen TF-IDF vs Sentence Transformers (Tabel 4 & Laporan 5.2)
TFIDF_EXPERIMENTS = [
    {
        "konfigurasi": "A: TF-IDF Unigram Dasar",
        "fitur": "Unigram, maks 3.000 fitur, min_df 5",
        "matriks": "11.713 x 2.776",
        "k_diuji": "2 - 8",
        "silhouette_range": "0.0087 - 0.0181 (tertinggi k=8)",
        "cluster_terbesar": "6.607 (56.4%) pada k=8",
        "catatan": "Dominasi satu klaster raksasa (>56%), kata kunci terpusat pada kata umum seperti 'app', 'good'."
    },
    {
        "konfigurasi": "B: TF-IDF Uni+Bigram Selektif",
        "fitur": "Uni+Bigram, maks 10.000 fitur, max_df 0.5, sublinear",
        "matriks": "11.713 x 5.652",
        "k_diuji": "3 - 8",
        "silhouette_range": "0.0073 - 0.0136 (tertinggi k=8)",
        "cluster_terbesar": "7.616 (65.0%) pada k=8",
        "catatan": "Klaster terbesar membengkak menjadi 65.0%, pemisahan topik semakin terdistorsi."
    },
    {
        "konfigurasi": "C: TF-IDF Stopwords Kustom",
        "fitur": "Konfigurasi B + daftar stopwords kustom, max_df 0.4",
        "matriks": "11.713 x 4.875",
        "k_diuji": "2 - 10",
        "silhouette_range": "0.0033 - 0.0148 (tertinggi k=10)",
        "cluster_terbesar": "7.116 (60.8%) pada k=10",
        "catatan": "Meskipun stopwords umum disaring, matriks leksikal tetap gagal memecah klaster dominan (>60%)."
    },
    {
        "konfigurasi": "Model Final: Sentence Transformers",
        "fitur": "paraphrase-multilingual-MiniLM-L12-v2, 384 dimensi dense, L2-normalized",
        "matriks": "11.713 x 384",
        "k_diuji": "2 - 10",
        "silhouette_range": "0.0753 - 0.1280 (k=10: 0.0831)",
        "cluster_terbesar": "2.079 (17.7%) pada k=10",
        "catatan": "Silhouette Score meningkat 5-10x lipat dibanding TF-IDF. Distribusi cluster jauh lebih seimbang (klaster terbesar hanya 17.7%)."
    }
]

# Metadata Penelitian Ringkas
RESEARCH_INFO = {
    "judul": "Clustering Ulasan Aplikasi Produktivitas di Google Play Store Menggunakan Sentence Transformers dan K-Means",
    "dataset_mentah": "12.495 ulasan dari 15 aplikasi",
    "dataset_bersih": "11.713 ulasan (setelah drop 688 duplikat & 94 teks kosong)",
    "model_embedding": "paraphrase-multilingual-MiniLM-L12-v2",
    "dimensi_embedding": 384,
    "algoritma": "K-Means (k=10, init=k-means++, random_state=42, n_init=10, max_iter=300)",
    "evaluasi_final": "Silhouette Score k=10: 0.0831 (Cosine, subsample 3.000)",
    "evaluasi_k2": "Silhouette Score k=2: 0.1280",
    "metode_kata_kunci": "Rata-rata bobot TF-IDF per cluster (5.000 fitur, uni+bigram, min_df 5)"
}
