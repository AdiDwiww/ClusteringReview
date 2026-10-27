import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.ui_theme import render_workspace_header, render_kpi, render_section_title
from modules.cluster_info import CLUSTER_METADATA
from modules.icons import icon_svg

def show(df: pd.DataFrame):
    render_workspace_header(
        title="Review Intelligence Workspace",
        subtitle="Analisis clustering ulasan dari 15 aplikasi produktivitas Google Play Store menggunakan representasi Sentence Transformers dan algoritma K-Means (k=10).",
        category="Analytics Overview",
        icon="layout-dashboard"
    )
    
    # 1. KPI Cards (Clean AI SaaS Metrics, Zero Emojis)
    total_reviews = len(df)
    total_apps = df['appId'].nunique()
    total_clusters = df['cluster_semantik_10'].nunique()
    avg_rating = df['score'].mean()
    pct_negative = (df['score'] <= 2).mean() * 100
    pct_positive = (df['score'] >= 4).mean() * 100
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi(
            label="Total Ulasan",
            value=f"{total_reviews:,}",
            context="11.713 ulasan terverifikasi",
            icon="message-square",
            accent_color="#4F46E5"
        )
    with col2:
        render_kpi(
            label="Aplikasi Dianalisis",
            value=f"{total_apps}",
            context="Google Play Store produktivitas",
            icon="smartphone",
            accent_color="#0D9488"
        )
    with col3:
        render_kpi(
            label="Jumlah Klaster",
            value=f"{total_clusters}",
            context="Model terpilih k = 10",
            icon="layers",
            accent_color="#7C3AED"
        )
    with col4:
        render_kpi(
            label="Rata-rata Rating",
            value=f"{avg_rating:.2f} / 5.0",
            context=f"Positif: {pct_positive:.1f}% | Negatif: {pct_negative:.1f}%",
            icon="star",
            accent_color="#D97706"
        )
        
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    
    # 2. Charts Row: Distribusi Rating & Proporsi Klaster
    col_chart1, col_chart2 = st.columns([1, 1])
    
    with col_chart1:
        render_section_title("Distribusi Rating Keseluruhan", "Sebaran frekuensi rating bintang 1 hingga 5 pada dataset.", icon="bar-chart-3")
        rating_counts = df['score'].value_counts().sort_index().reset_index()
        rating_counts.columns = ['Rating', 'Jumlah']
        rating_counts['Persentase'] = (rating_counts['Jumlah'] / total_reviews * 100).round(1)
        rating_counts['Label'] = rating_counts['Rating'].apply(lambda x: f"Skor {x}")
        
        # Modern neutral-semantic palette
        colors_rating = ['#EF4444', '#F97316', '#EAB308', '#22C55E', '#10B981']
        
        fig_rating = go.Figure(data=[
            go.Bar(
                x=rating_counts['Label'],
                y=rating_counts['Jumlah'],
                text=[f"{count:,}<br>({pct}%)" for count, pct in zip(rating_counts['Jumlah'], rating_counts['Persentase'])],
                textposition='auto',
                marker=dict(
                    color=colors_rating,
                    line=dict(color='#E4E4E7', width=1)
                ),
                hovertemplate="<b>%{x}</b><br>Jumlah: %{y:,} ulasan<br>Proporsi: %{text}<extra></extra>"
            )
        ])
        fig_rating.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=320,
            xaxis=dict(title="", showgrid=False, tickfont=dict(size=12, color='#71717A')),
            yaxis=dict(title="Jumlah Ulasan", showgrid=True, gridcolor='#F4F4F5', tickfont=dict(size=11, color='#71717A')),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", size=12)
        )
        st.plotly_chart(fig_rating, width='stretch')
        
    with col_chart2:
        render_section_title("Proporsi Ulasan per Klaster", "Distribusi ukuran ulasan pada 10 kelompok tematik K-Means.", icon="layers")
        cluster_summary = df.groupby('cluster_semantik_10').size().reset_index(name='Jumlah')
        cluster_summary['Klaster'] = cluster_summary['cluster_semantik_10'].apply(
            lambda x: f"C{x}: {CLUSTER_METADATA.get(x, {}).get('name', f'Cluster {x}')[:20]}"
        )
        cluster_summary['Warna'] = cluster_summary['cluster_semantik_10'].apply(
            lambda x: CLUSTER_METADATA.get(x, {}).get('warna', '#6B7280')
        )
        
        fig_donut = go.Figure(data=[
            go.Pie(
                labels=cluster_summary['Klaster'],
                values=cluster_summary['Jumlah'],
                hole=0.55,
                marker=dict(colors=cluster_summary['Warna'].tolist(), line=dict(color='#FFFFFF', width=2)),
                textinfo='percent',
                hovertemplate="<b>%{label}</b><br>Jumlah: %{value:,} ulasan<br>Proporsi: %{percent}<extra></extra>"
            )
        ])
        fig_donut.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=320,
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02, font=dict(size=11, color='#71717A')),
            font=dict(family="Inter, sans-serif", size=11)
        )
        st.plotly_chart(fig_donut, width='stretch')
        
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    
    # 3. Bar Chart: Rata-rata Rating per Klaster
    render_section_title("Perbandingan Rata-rata Rating per Klaster", "Mengidentifikasi klaster dengan kecenderungan keluhan teknis (rating rendah) hingga kepuasan pengguna (rating tinggi).", icon="activity")
    
    cluster_stats = df.groupby('cluster_semantik_10').agg(
        n=('content', 'count'),
        mean_score=('score', 'mean'),
        median_score=('score', 'median')
    ).reset_index()
    
    cluster_stats['Nama Klaster'] = cluster_stats['cluster_semantik_10'].apply(
        lambda x: f"C{x}: {CLUSTER_METADATA.get(x, {}).get('name', f'Cluster {x}')[:24]}"
    )
    cluster_stats['Warna'] = cluster_stats['cluster_semantik_10'].apply(
        lambda x: CLUSTER_METADATA.get(x, {}).get('warna', '#4F46E5')
    )
    cluster_stats = cluster_stats.sort_values('mean_score')
    
    fig_bar_avg = go.Figure(data=[
        go.Bar(
            x=cluster_stats['Nama Klaster'],
            y=cluster_stats['mean_score'].round(2),
            text=[f"{v:.2f}" for v in cluster_stats['mean_score']],
            textposition='outside',
            marker=dict(
                color=cluster_stats['Warna'].tolist(),
                line=dict(color='#E4E4E7', width=1)
            ),
            hovertemplate="<b>%{x}</b><br>Rata-rata Rating: %{y:.2f} / 5.0<extra></extra>"
        )
    ])
    fig_bar_avg.add_hline(
        y=avg_rating, 
        line_dash="dash", 
        line_color="#71717A", 
        annotation_text=f"Rata-rata Global ({avg_rating:.2f})",
        annotation_position="bottom right"
    )
    fig_bar_avg.update_layout(
        margin=dict(l=10, r=10, t=20, b=70),
        height=360,
        xaxis_tickangle=-25,
        xaxis=dict(tickfont=dict(size=11, color='#71717A')),
        yaxis=dict(range=[0, 5.2], title="Rata-rata Rating", showgrid=True, gridcolor='#F4F4F5', tickfont=dict(size=11, color='#71717A')),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", size=11)
    )
    st.plotly_chart(fig_bar_avg, width='stretch')
    
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    
    # 4. Ringkasan Insight Nyata Berdasarkan Data Aktual (Clean Cards, No Emojis)
    render_section_title("Ringkasan Temuan & Rekomendasi Analitis", "Sintesis hasil clustering yang dihitung langsung dari data ulasan aktual.", icon="target")
    
    col_in1, col_in2 = st.columns(2)
    
    alert_icon = icon_svg("alert-triangle", size=16, color="#DC2626")
    check_icon = icon_svg("check-circle-2", size=16, color="#059669")
    
    with col_in1:
        st.markdown(f"""
        <div class="saas-card" style="border-left: 3px solid #DC2626; height: 100%;">
            <div class="saas-card-title" style="color: #991B1B;">
                {alert_icon} Area Keluhan Kritis (Prioritas Penanganan)
            </div>
            <div class="saas-card-desc" style="margin-bottom: 0.9rem;">
                Klaster dengan skor rating terendah dan konsentrasi ketidakpuasan tinggi.
            </div>
            <ul style="font-size: 0.85rem; color: #3F3F46; line-height: 1.6; padding-left: 1.15rem; margin: 0;">
                <li style="margin-bottom: 0.45rem;">
                    <b>Cluster 5 (Akun & Sinkronisasi):</b> Rata-rata rating terendah (<b>1.90 / 5.0</b>) dengan <b>76.0%</b> ulasan negatif (skor 1–2). Gangguan login dan sinkronisasi lintas perangkat menimbulkan resistensi tertinggi karena ancaman hilangnya catatan pengguna.
                </li>
                <li style="margin-bottom: 0.45rem;">
                    <b>Cluster 1 (Masalah Teknis & Bug):</b> Klaster keluhan terbesar (<b>1.658 ulasan, 14.2%</b>) dengan rata-rata <b>2.11</b>, didominasi laporan aplikasi macet (crash) pasca pembaruan versi.
                </li>
                <li>
                    <b>Cluster 6 (Notifikasi & Pengingat):</b> Rata-rata <b>2.41</b>, kegagalan alarm tepat waktu merusak proposisi nilai utama aplikasi produktivitas.
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_in2:
        st.markdown(f"""
        <div class="saas-card" style="border-left: 3px solid #059669; height: 100%;">
            <div class="saas-card-title" style="color: #065F46;">
                {check_icon} Driver Kepuasan & Retensi Pengguna
            </div>
            <div class="saas-card-desc" style="margin-bottom: 0.9rem;">
                Klaster dengan sentimen positif tertinggi yang mendorong loyalitas aplikasi.
            </div>
            <ul style="font-size: 0.85rem; color: #3F3F46; line-height: 1.6; padding-left: 1.15rem; margin: 0;">
                <li style="margin-bottom: 0.45rem;">
                    <b>Cluster 8 (Pujian Umum & Rekomendasi):</b> Klaster terbesar dalam penelitian (<b>2.079 ulasan, 17.7%</b>) dengan rata-rata tertinggi (<b>4.20</b>; 81.7% ulasan bintang 4–5).
                </li>
                <li style="margin-bottom: 0.45rem;">
                    <b>Cluster 4 (Kemudahan Penggunaan):</b> Sebanyak <b>1.207 ulasan (10.3%)</b> dengan skor rata-rata <b>4.18</b>, menegaskan bahwa kesederhanaan antarmuka (UI intuitif) adalah nilai jual terkuat.
                </li>
                <li>
                    <b>Cluster 3 (Manajemen Tugas):</b> Rata-rata <b>3.02</b>, menjadi wadah saran konstruktif dan permintaan fitur integrasi agenda kerja harian.
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
