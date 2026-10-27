import os
import re
import numpy as np
import pandas as pd
import streamlit as st
from modules.cluster_info import APP_NAME_MAP, CLUSTER_METADATA

def clean_text(text: str) -> str:
    """
    Fungsi preprocessing yang identik dengan implementasi pada notebook penelitian (Cell 3):
    1. Mengubah teks ke huruf kecil (lowercase)
    2. Menghapus URL (http/www)
    3. Menghapus karakter selain alfabet latin (a-z) dan spasi
    4. Merapikan spasi berlebih
    """
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+', ' ', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@st.cache_data(show_spinner=False)
def load_dataset(csv_path: str = "hasil_clustering_semantik_k10.csv") -> pd.DataFrame:
    """
    Memuat dataset CSV hasil clustering dengan caching untuk performa tinggi.
    Menangani missing values, validasi tipe data, dan membuat kolom turunan yang konsisten.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File dataset tidak ditemukan pada path: {csv_path}")
    
    df = pd.read_csv(csv_path)
    
    # Validasi kolom wajib
    required_cols = ['content', 'score', 'appId', 'cluster_semantik_10']
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Kolom wajib tidak ditemukan dalam CSV: {missing_cols}")
    
    # Normalisasi tipe data
    df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(3).astype(int)
    df['cluster_semantik_10'] = pd.to_numeric(df['cluster_semantik_10'], errors='coerce').fillna(0).astype(int)
    df['content'] = df['content'].fillna('').astype(str)
    
    # Kolom teks bersih jika belum ada
    if 'cleaned_content' not in df.columns or df['cleaned_content'].isnull().any():
        df['cleaned_content'] = df['content'].apply(clean_text)
    else:
        df['cleaned_content'] = df['cleaned_content'].fillna('').astype(str)
        
    # Kolom panjang teks
    if 'panjang_teks' not in df.columns:
        df['panjang_teks'] = df['content'].str.len()
    else:
        df['panjang_teks'] = pd.to_numeric(df['panjang_teks'], errors='coerce').fillna(df['content'].str.len()).astype(int)
        
    # Tambahkan panjang kata (word count)
    df['jumlah_kata'] = df['content'].apply(lambda x: len(str(x).split()))
    
    # Nama aplikasi ramah pengguna
    df['app_name'] = df['appId'].map(lambda x: APP_NAME_MAP.get(x, x))
    
    # Nama dan tema cluster
    df['cluster_name'] = df['cluster_semantik_10'].map(
        lambda x: CLUSTER_METADATA.get(x, {}).get('name', f"Cluster {x}")
    )
    df['cluster_theme'] = df['cluster_semantik_10'].map(
        lambda x: CLUSTER_METADATA.get(x, {}).get('tema', f"Tema Cluster {x}")
    )
    
    # Kategori Rating
    def categorize_rating(r):
        if r <= 2:
            return "Rendah (1-2)"
        elif r == 3:
            return "Netral (3)"
        else:
            return "Tinggi (4-5)"
            
    df['rating_category'] = df['score'].apply(categorize_rating)
    
    # At timestamp
    if 'at' in df.columns:
        df['at'] = pd.to_datetime(df['at'], errors='coerce')
        
    return df

@st.cache_data(show_spinner=False)
def load_pca_coordinates(npy_path: str = "models/pca_2d.npy") -> np.ndarray:
    """Memuat koordinat proyeksi 2D PCA jika tersedia."""
    if os.path.exists(npy_path):
        try:
            return np.load(npy_path)
        except Exception:
            return None
    return None

@st.cache_data(show_spinner=False)
def load_cluster_centroids(npy_path: str = "models/cluster_centroids.npy") -> np.ndarray:
    """Memuat vektor sentroid 10 klaster hasil rekonstruksi."""
    if os.path.exists(npy_path):
        try:
            return np.load(npy_path)
        except Exception:
            return None
    return None
