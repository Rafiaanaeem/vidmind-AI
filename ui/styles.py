import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    :root {
        --primary: #6C5CE7;
        --primary-hover: #5A4AD1;
        --primary-light: #F3F0FF;
        --dark-navy: #0F172A;
        --slate-text: #1E293B;
        --muted-text: #64748B;
        --bg-color: #F8FAFC;
        --border-color: #E2E8F0;
        --card-bg: #FFFFFF;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: var(--bg-color);
        color: var(--slate-text);
    }

    /* --- SIDEBAR OVERRIDES (PRESERVED) --- */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid var(--border-color) !important;
    }
    [data-testid="stSidebar"] * {
        color: var(--slate-text) !important;
    }

    /* --- HERO STYLING --- */
    .hero-container {
        padding: 10px 0px 20px 0px;
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: var(--dark-navy);
        letter-spacing: -0.5px;
    }
    .hero-title span {
        color: var(--primary);
        background: linear-gradient(135deg, #6C5CE7 0%, #a29bfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        color: var(--muted-text);
        font-size: 0.98rem;
        margin-top: 4px;
        font-weight: 500;
    }

    /* --- MODERN TABS (HIGH VISIBILITY & ACTIVE CONTRAST) --- */
    div[data-baseweb="tab-highlight"] {
        display: none !important; /* Hide default underline */
    }
    div[data-baseweb="tab-border"] {
        display: none !important;
    }
    div[data-baseweb="tab-list"] {
        background-color: #EDF2F7 !important;
        padding: 6px !important;
        border-radius: 12px !important;
        gap: 6px !important;
        border: 1px solid #E2E8F0 !important;
        margin-bottom: 20px !important;
    }

    button[data-baseweb="tab"] {
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        color: #475569 !important; /* Always dark visible text */
        border-radius: 8px !important;
        padding: 10px 20px !important;
        border: 1px solid transparent !important;
        background-color: #FFFFFF !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
    }

    button[data-baseweb="tab"]:hover {
        color: var(--primary) !important;
        background-color: #F8FAFC !important;
        border-color: #CBD5E1 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FFFFFF !important;
        background-color: var(--primary) !important;
        border-color: var(--primary) !important;
        box-shadow: 0 4px 12px rgba(108, 92, 231, 0.3) !important;
    }

    /* --- STATS / METRIC CARDS --- */
    .stat-card-modern {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 18px 16px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stat-card-modern:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.05);
    }
    .stat-number {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--dark-navy);
        line-height: 1.2;
    }
    .stat-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--muted-text);
        margin-top: 4px;
    }
    .stat-badge {
        font-size: 0.72rem;
        font-weight: 700;
        color: #059669;
        background: #ECFDF5;
        padding: 3px 10px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 8px;
    }

    /* --- FEATURE SIDEBAR CARDS --- */
    .feature-card {
        display: flex;
        align-items: center;
        gap: 10px;
        background: #F8FAFC;
        border: 1px solid #EEF2F6;
        padding: 10px 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        font-weight: 600;
        font-size: 0.88rem;
        color: var(--dark-navy) !important;
    }

    /* --- TIMESTAMP BADGE --- */
    .ts-badge {
        background-color: var(--primary-light);
        color: var(--primary);
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.82rem;
    }

    /* --- PRIMARY ACTION BUTTON (Summarize Video) --- */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6C5CE7 0%, #5A4AD1 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 14px 28px !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.25) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(108, 92, 231, 0.4) !important;
    }

    /* --- APPEAL EXPORT & DOWNLOAD BUTTONS --- */
    div.stDownloadButton {
        width: 100%;
    }
    div.stDownloadButton > button {
        width: 100% !important;
        background: #FFFFFF !important;
        color: var(--dark-navy) !important;
        border: 2px solid #6C5CE7 !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 2px 8px rgba(108, 92, 231, 0.08) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    div.stDownloadButton > button:hover {
        background: #6C5CE7 !important;
        color: #FFFFFF !important;
        box-shadow: 0 6px 20px rgba(108, 92, 231, 0.3) !important;
        transform: translateY(-2px) !important;
    }

    /* --- CONTAINER CARD STYLING --- */
    .card-box {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
        margin-bottom: 24px;
    }
    </style>
    """, unsafe_allow_html=True)