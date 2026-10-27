import streamlit as st
from modules.icons import icon_svg

def apply_custom_css():
    """
    Injeksi CSS Design System Premium AI SaaS (Linear/Vercel/OpenAI inspired):
    - Background neutral off-white
    - Tipografi crisp Inter / Plus Jakarta Sans
    - Card surface putih bersih dengan border halus 1px
    - Hirarki visual jelas tanpa gradient mencolok / neon glow
    - Zero emoji - semua indikator menggunakan ikon UI Lucide
    """
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
        
        :root {
            --bg-canvas: #FAFAFA;
            --bg-surface: #FFFFFF;
            --bg-subtle: #F4F4F5;
            --border-subtle: #E4E4E7;
            --border-hover: #D4D4D8;
            --text-primary: #09090B;
            --text-secondary: #71717A;
            --text-muted: #A1A1AA;
            --brand-primary: #4F46E5;
            --brand-subtle: #EEF2FF;
            --brand-border: #C7D2FE;
            --radius-md: 10px;
            --radius-lg: 12px;
            --radius-sm: 6px;
        }

        /* Base Typography & Background */
        /* NOTE: intentionally exclude span/button to preserve Material Symbols icon font */
        html, body, .stApp,
        .stApp p, .stApp div, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
        .stApp label, .stApp input, .stApp textarea, .stApp select,
        div[data-testid="stMarkdownContainer"],
        div[data-testid="stText"],
        div[data-testid="stCaption"],
        div[data-testid="stMetric"],
        div[data-testid="stAlert"],
        div[data-testid="stDataFrame"],
        div[data-testid="stTable"],
        section[data-testid="stSidebar"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
            color: var(--text-primary);
        }

        /* Explicitly preserve Material Symbols for Streamlit internal icon spans/buttons */
        .stApp span[data-baseweb],
        .stApp [class*="material-symbols"],
        button[data-testid] span,
        div[data-testid="stExpander"] summary span,
        div[data-testid="stExpander"] button span,
        .stApp button span {
            font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', sans-serif !important;
        }
        
        .stApp {
            background-color: var(--bg-canvas) !important;
        }
        
        /* Sidebar Styling (Clean Workspace Style) */
        section[data-testid="stSidebar"] {
            background-color: #F8F9FA !important;
            border-right: 1px solid var(--border-subtle) !important;
        }
        
        section[data-testid="stSidebar"] .block-container {
            padding-top: 1.5rem !important;
            padding-left: 1.25rem !important;
            padding-right: 1.25rem !important;
        }

        /* Sidebar Radio Navigation (Pill item style) */
        section[data-testid="stSidebar"] div[data-testid="stRadio"] > div {
            gap: 0.25rem !important;
        }
        
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
            background: transparent;
            padding: 0.45rem 0.75rem !important;
            border-radius: var(--radius-sm) !important;
            transition: all 0.15s ease !important;
            font-size: 0.88rem !important;
            font-weight: 500 !important;
            color: var(--text-secondary) !important;
            border: 1px solid transparent !important;
            display: flex !important;
            align-items: center !important;
        }
        
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
            background-color: #F1F2F4 !important;
            color: var(--text-primary) !important;
        }
        
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"] {
            background-color: #FFFFFF !important;
            color: var(--brand-primary) !important;
            font-weight: 600 !important;
            border-color: var(--border-subtle) !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
        }

        /* Hide Default Radio Circles for sleek tab list look */
        section[data-testid="stSidebar"] div[data-testid="stRadio"] input[type="radio"] {
            display: none !important;
        }

        /* Page Headers */
        .workspace-header {
            margin-bottom: 1.5rem;
            padding-bottom: 1.25rem;
            border-bottom: 1px solid var(--border-subtle);
        }
        
        .workspace-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.72rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--brand-primary);
            background: var(--brand-subtle);
            border: 1px solid var(--brand-border);
            padding: 0.2rem 0.55rem;
            border-radius: 9999px;
            margin-bottom: 0.6rem;
        }
        
        .workspace-title {
            font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
            font-size: 1.65rem;
            font-weight: 700;
            letter-spacing: -0.025em;
            color: var(--text-primary);
            margin: 0 0 0.35rem 0;
            line-height: 1.25;
        }
        
        .workspace-subtitle {
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin: 0;
            line-height: 1.5;
        }

        /* Premium KPI Metric Cards */
        .kpi-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 1.15rem 1.25rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
            transition: border-color 0.15s ease, box-shadow 0.15s ease;
            height: 100%;
        }
        
        .kpi-card:hover {
            border-color: var(--border-hover);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        }
        
        .kpi-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.5rem;
        }
        
        .kpi-label {
            font-size: 0.76rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-secondary);
        }
        
        .kpi-icon-wrap {
            width: 28px;
            height: 28px;
            border-radius: var(--radius-sm);
            background: var(--bg-subtle);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: var(--text-secondary);
        }
        
        .kpi-value {
            font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
            font-size: 1.7rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.02em;
            line-height: 1.2;
            margin-bottom: 0.25rem;
        }
        
        .kpi-context {
            font-size: 0.78rem;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }

        /* Surface Cards / Containers */
        .saas-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 1.4rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        }
        
        .saas-card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid var(--border-subtle);
        }
        
        .saas-card-title {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin: 0;
        }
        
        .saas-card-desc {
            font-size: 0.82rem;
            color: var(--text-secondary);
            margin-top: 0.2rem;
        }

        /* Review Quote Cards */
        .quote-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-left: 3px solid var(--brand-primary);
            border-radius: 0 var(--radius-md) var(--radius-md) 0;
            padding: 0.9rem 1.1rem;
            margin-bottom: 0.75rem;
            font-size: 0.88rem;
            line-height: 1.55;
            color: #27272A;
            transition: all 0.15s ease;
        }
        
        .quote-card:hover {
            background: #FAFAFA;
            border-color: var(--border-hover);
        }
        
        .quote-meta {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            margin-top: 0.5rem;
            font-size: 0.76rem;
            color: var(--text-muted);
            font-family: 'JetBrains Mono', monospace;
        }

        /* Keyword Tags */
        .saas-tag {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            background: #F4F4F5;
            color: #3F3F46;
            font-size: 0.78rem;
            font-weight: 500;
            padding: 0.22rem 0.55rem;
            border-radius: var(--radius-sm);
            margin-right: 0.35rem;
            margin-bottom: 0.35rem;
            border: 1px solid #E4E4E7;
            font-family: 'JetBrains Mono', monospace;
        }

        /* Semantic Badge */
        .saas-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.18rem 0.5rem;
            border-radius: 9999px;
            font-size: 0.74rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }

        /* Clean Streamlit Element Overrides */
        div[data-testid="stExpander"] {
            border: 1px solid var(--border-subtle) !important;
            border-radius: var(--radius-md) !important;
            background: var(--bg-surface) !important;
            box-shadow: none !important;
        }
        
        /* Streamlit Button Overrides — use data-testid (works in all Streamlit versions) */
        button[data-testid="baseButton-primary"],
        div[data-testid="stButton"] > button[kind="primary"],
        .stButton > button[type="submit"] {
            background-color: #09090B !important;
            color: #FFFFFF !important;
            border: 1px solid #09090B !important;
            border-radius: var(--radius-sm) !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            font-family: 'Inter', sans-serif !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
            transition: all 0.15s ease !important;
        }
        
        button[data-testid="baseButton-primary"]:hover {
            background-color: #27272A !important;
            border-color: #27272A !important;
            color: #FFFFFF !important;
        }
        
        button[data-testid="baseButton-primary"] p,
        button[data-testid="baseButton-primary"] span:not([class*="material"]) {
            color: #FFFFFF !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        button[data-testid="baseButton-secondary"],
        div[data-testid="stButton"] > button[kind="secondary"] {
            background-color: var(--bg-surface) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: var(--radius-sm) !important;
            font-weight: 500 !important;
            font-size: 0.88rem !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        button[data-testid="baseButton-secondary"]:hover {
            border-color: var(--border-hover) !important;
            background-color: var(--bg-subtle) !important;
        }
        
        button[data-testid="baseButton-secondary"] p,
        button[data-testid="baseButton-secondary"] span:not([class*="material"]) {
            color: var(--text-primary) !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* Streamlit Tabs Styling */
        div[data-testid="stTabs"] button[role="tab"] {
            font-size: 0.88rem !important;
            font-weight: 500 !important;
            color: var(--text-secondary) !important;
            border-bottom: 2px solid transparent !important;
            padding: 0.5rem 1rem !important;
        }
        
        div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
            color: var(--brand-primary) !important;
            border-bottom-color: var(--brand-primary) !important;
            font-weight: 600 !important;
        }

        /* Clean Alert Boxes */
        div[data-testid="stAlert"] {
            border-radius: var(--radius-md) !important;
            font-size: 0.88rem !important;
            border: 1px solid var(--border-subtle) !important;
        }
        
        /* Subtle Streamlit Dataframe Table */
        div[data-testid="stDataFrame"] {
            border: 1px solid var(--border-subtle) !important;
            border-radius: var(--radius-md) !important;
            overflow: hidden;
        }
    </style>
    """, unsafe_allow_html=True)

def render_workspace_header(title: str, subtitle: str, category: str = "Clustering Review", icon: str = "sparkles"):
    """
    Header halaman modern bergaya Linear / Vercel dengan eyebrow tag, judul tebal sans-serif, dan subtitle informatif.
    """
    category_svg = icon_svg(icon, size=13, color="#4F46E5")
    st.markdown(f"""
    <div class="workspace-header">
        <div class="workspace-eyebrow">{category_svg} {category}</div>
        <h1 class="workspace-title">{title}</h1>
        <p class="workspace-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def render_kpi(label: str, value: str, context: str = "", icon: str = "activity", accent_color: str = "#4F46E5"):
    """
    Kartu KPI bergaya AI SaaS: ikon Lucide di pojok kanan atas, label uppercase tipis, angka tabular tebal.
    """
    icon_html = icon_svg(icon, size=15, color=accent_color)
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-top">
            <span class="kpi-label">{label}</span>
            <div class="kpi-icon-wrap">{icon_html}</div>
        </div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-context">{context}</div>
    </div>
    """, unsafe_allow_html=True)

def render_tag_list(tags: list):
    """
    Render daftar tag kata kunci dengan ikon tag Lucide tanpa emoji.
    """
    tag_icon = icon_svg("tag", size=11, color="#71717A")
    tags_html = "".join([f'<span class="saas-tag">{tag_icon} {t}</span>' for t in tags])
    st.markdown(f'<div style="margin-top: 0.35rem; display: flex; flex-wrap: wrap;">{tags_html}</div>', unsafe_allow_html=True)

def render_section_title(title: str, description: str = "", icon: str = None):
    """
    Judul section dengan ikon Lucide dan caption subtitle rapi.
    """
    icon_html = f"{icon_svg(icon, size=18, color='#4F46E5')} " if icon else ""
    st.markdown(f"""
    <div style="margin: 1.6rem 0 0.8rem 0;">
        <h3 style="font-size: 1.12rem; font-weight: 700; color: #09090B; margin: 0; display: flex; align-items: center; gap: 0.45rem;">
            {icon_html}<span>{title}</span>
        </h3>
        {f'<p style="font-size: 0.82rem; color: #71717A; margin: 0.2rem 0 0 0;">{description}</p>' if description else ''}
    </div>
    """, unsafe_allow_html=True)
