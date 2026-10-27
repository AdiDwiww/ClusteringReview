import streamlit as st

def apply_custom_css():
    """
    Menyuntikkan CSS kustom untuk tampilan dashboard modern, rapi, dan profesional.
    Menggunakan palet warna harmonis, font Google Inter, card shadow elegan, dan responsive layout.
    """
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Metric / KPI Card Styling */
        .kpi-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.9));
            border: 1px solid #E2E8F0;
            border-radius: 14px;
            padding: 1.1rem 1.25rem;
            box-shadow: 0 4px 12px -2px rgba(15, 23, 42, 0.05), 0 2px 4px -2px rgba(15, 23, 42, 0.03);
            transition: all 0.25s ease;
            position: relative;
            overflow: hidden;
        }
        
        .kpi-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px -3px rgba(15, 23, 42, 0.08);
            border-color: #CBD5E1;
        }
        
        .kpi-title {
            font-size: 0.82rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #64748B;
            margin-bottom: 0.35rem;
        }
        
        .kpi-value {
            font-size: 1.75rem;
            font-weight: 800;
            color: #0F172A;
            line-height: 1.2;
        }
        
        .kpi-subtitle {
            font-size: 0.78rem;
            color: #94A3B8;
            margin-top: 0.35rem;
        }
        
        /* Header Hero Banner */
        .hero-banner {
            background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
            border-radius: 16px;
            padding: 1.6rem 2rem;
            color: white;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .hero-title {
            font-size: 1.6rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 0.4rem;
            color: #F8FAFC;
        }
        
        .hero-subtitle {
            font-size: 0.95rem;
            color: #94A3B8;
            line-height: 1.5;
        }
        
        .hero-tag {
            display: inline-block;
            background: rgba(59, 130, 246, 0.2);
            border: 1px solid rgba(59, 130, 246, 0.4);
            color: #93C5FD;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.2rem 0.65rem;
            border-radius: 9999px;
            margin-bottom: 0.6rem;
        }
        
        /* Cluster Badges */
        .cluster-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.25rem 0.65rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            color: #1E293B;
            background-color: #F1F5F9;
            border: 1px solid #E2E8F0;
        }
        
        .cluster-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
        }
        
        /* Section Containers */
        .content-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 14px;
            padding: 1.4rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 2px 6px -1px rgba(15, 23, 42, 0.04);
        }
        
        .card-header-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 0.25rem;
        }
        
        .card-header-desc {
            font-size: 0.85rem;
            color: #64748B;
            margin-bottom: 1rem;
        }

        /* Review Quote Box */
        .review-quote {
            background-color: #F8FAFC;
            border-left: 4px solid #3B82F6;
            padding: 0.9rem 1.1rem;
            border-radius: 0 10px 10px 0;
            margin-bottom: 0.75rem;
            font-size: 0.88rem;
            line-height: 1.5;
            color: #334155;
        }
        
        .review-quote-meta {
            font-size: 0.78rem;
            color: #64748B;
            margin-top: 0.4rem;
            font-weight: 500;
        }
        
        /* Pill tags for keywords */
        .keyword-tag {
            display: inline-block;
            background-color: #EEF2FF;
            color: #4338CA;
            font-size: 0.78rem;
            font-weight: 600;
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            margin-right: 0.35rem;
            margin-bottom: 0.35rem;
            border: 1px solid #E0E7FF;
        }
    </style>
    """, unsafe_allow_html=True)

def render_hero_banner(title: str, subtitle: str, tag: str = "Data Science Project"):
    st.markdown(f"""
    <div class="hero-banner">
        <span class="hero-tag">{tag}</span>
        <div class="hero-title">{title}</div>
        <div class="hero-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def render_kpi(title: str, value: str, subtitle: str = "", border_color: str = "#3B82F6"):
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 3px solid {border_color};">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def render_keyword_tags(keywords: list):
    tags_html = "".join([f'<span class="keyword-tag">#{k}</span>' for k in keywords])
    st.markdown(f'<div style="margin-top: 0.4rem;">{tags_html}</div>', unsafe_allow_html=True)
