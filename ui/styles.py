import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --primary: #6C5CE7;
        --primary-light: #F3F0FF;
        --dark-navy: #0F172A;
        --slate-text: #1E293B;
        --muted-text: #64748B;
        --bg-color: #F8FAFC;
        --border-color: #E2E8F0;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: var(--bg-color);
        color: var(--slate-text);
    }

    /* Streamlit Sidebar Overrides */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid var(--border-color) !important;
    }
    [data-testid="stSidebar"] * {
        color: var(--slate-text) !important;
    }

    /* Hero Styling */
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--dark-navy);
    }
    .hero-title span {
        color: var(--primary);
    }
    .hero-subtitle {
        color: var(--muted-text);
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Segmented Card Container for Inputs */
    .input-card {
        background: #FFFFFF;
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }

    /* Tabs Styling (Removes Circles & Bullet Dots) */
    div[data-baseweb="tab-list"] {
        background-color: #F1F5F9 !important;
        padding: 4px !important;
        border-radius: 12px !important;
        gap: 4px !important;
    }

    button[data-baseweb="tab"] {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: var(--muted-text) !important;
        border-radius: 8px !important;
        padding: 8px 18px !important;
        border: none !important;
        background-color: transparent !important;
        transition: all 0.2s ease !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--primary) !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06) !important;
    }

    /* Hide standard radio button dot inputs if any remain */
    div[role="radiogroup"] {
        gap: 10px;
    }

    /* Metric/Stat Boxes */
    .stat-box {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid var(--border-color);
        text-align: center;
    }
    .stat-number {
        font-size: 1.7rem;
        font-weight: 800;
        color: var(--dark-navy);
    }
    .stat-label {
        font-size: 0.85rem;
        color: var(--muted-text);
    }
    .stat-badge {
        font-size: 0.72rem;
        font-weight: 700;
        color: #059669;
        background: #ECFDF5;
        padding: 2px 8px;
        border-radius: 12px;
        display: inline-block;
        margin-top: 6px;
    }

    /* Feature Sidebar Cards */
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

    /* Timestamp Pill Badge */
    .ts-badge {
        background-color: var(--primary-light);
        color: var(--primary);
        font-weight: 700;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.82rem;
    }

    /* Primary Action Buttons */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6C5CE7 0%, #5A4AD1 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 12px 24px !important;
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)