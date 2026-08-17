import streamlit as st
from models.schemas import SummaryResult, VideoMetadata
from typing import Dict, Any, List

def render_hero_header():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="hero-title">AI Video <span>Summarizer</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-subtitle">Summarize long videos into short, meaningful insights in seconds.</div>', unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="text-align: right; font-size: 3.5rem; filter: drop-shadow(0 4px 12px rgba(108,92,231,0.2));">
            🎬✨
        </div>
        """, unsafe_allow_html=True)

def render_sidebar_features():
    st.sidebar.markdown("### OVERVIEW")
    st.sidebar.info("Extract key information, generate concise summaries, highlight important moments, and create chapter timestamps from long videos instantly.")
    st.sidebar.markdown("### KEY FEATURES")
    features = [
        ("📺", "YouTube URL & Upload"),
        ("⚡", "AI-Powered Summaries"),
        ("🎯", "Key Highlights Extraction"),
        ("⏱️", "Timestamps & Chapters"),
        ("🌐", "Multi-Language Support"),
        ("📄", "Export (PDF / TXT)"),
        ("⚡", "Fast & Accurate AI")
    ]
    for icon, label in features:
        st.sidebar.markdown(f"""
        <div class="feature-card">
            <span class="feature-icon">{icon}</span>
            <span>{label}</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("### TECH STACK")
    st.sidebar.caption("Python • Whisper STT • Groq/OpenAI LLM • FFmpeg • Streamlit • ReportLab")

def render_stats_cards(stats: Dict[str, Any]):
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">🎬 {stats['videos_summarized']}</div>
            <div class="stat-label">Videos Summarized</div>
            <div class="stat-badge">▲ 30% this week</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">⏱️ {stats['time_saved_hrs']} hrs</div>
            <div class="stat-label">Time Saved</div>
            <div class="stat-badge">▲ 25% this week</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">✅ {stats['accuracy_score']}</div>
            <div class="stat-label">Summary Quality</div>
            <div class="stat-badge">High Quality</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">📥 {stats['total_exports']}</div>
            <div class="stat-label">Exports Generated</div>
            <div class="stat-badge">▲ 40% this week</div>
        </div>
        """, unsafe_allow_html=True)

def render_video_player_and_meta(meta: VideoMetadata):
    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    st.markdown("### 🎥 Video Overview")
    col1, col2 = st.columns([3, 2])
    with col1:
        if meta.source_type == 'youtube':
            st.video(meta.url_or_path)
        else:
            st.video(meta.url_or_path)
    with col2:
        st.markdown(f"#### {meta.title}")
        st.caption(f"Source: {meta.source_type.title()}")
        st.markdown(f"⏱️ **Duration:** `{meta.duration_formatted}`")
        st.markdown(f"👤 **Uploader:** {meta.uploader}")
        st.markdown(f"👁️ **Views:** {meta.view_count}")
    st.markdown('</div>', unsafe_allow_html=True)

def render_summary_result(summary: SummaryResult):
    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    st.markdown("### 📝 AI Summary")
    st.write(summary.summary_paragraph)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("#### Key Takeaways")
    for kp in summary.key_points:
        st.markdown(f"✅ &nbsp; {kp}")
    st.markdown('</div>', unsafe_allow_html=True)

def render_highlights(summary: SummaryResult):
    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Key Highlights & Important Moments")
    
    cols = st.columns(2)
    for idx, h in enumerate(summary.highlights):
        with cols[idx % 2]:
            st.markdown(f"""
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 14px; border-radius: 10px; margin-bottom: 12px;">
                <span class="ts-badge">{h.timestamp}</span> <b>{h.title}</b> <span style="color: #64748B; font-size: 0.85rem;">({h.duration})</span>
                <p style="font-size: 0.9rem; color: #334155; margin-top: 8px; margin-bottom: 0px;">{h.description}</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_chapters(summary: SummaryResult):
    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    st.markdown("### 📌 Chapters & Topics")
    for c in summary.chapters:
        st.markdown(f"<span class='ts-badge'>{c.timestamp}</span> &nbsp; **{c.title}** — <span style='color: #475569;'>{c.description}</span>", unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_history_section(history_items: List[Dict[str, Any]]):
    st.markdown("### 📜 Processed Video History")
    if not history_items:
        st.info("No past video summaries found yet. Process a video above to build history!")
        return

    for item in history_items:
        with st.expander(f"🎬 {item['title']} | Duration: {item['duration_formatted']} — ({item['created_at'][:10]})"):
            s_json = item['summary_json']
            st.markdown(f"**Summary ({item['summary_length']} - {item['language']}):**")
            st.write(s_json.get('summary_paragraph'))
            
            st.markdown("**Key Takeaways:**")
            for kp in s_json.get('key_points', []):
                st.markdown(f"• {kp}")

def render_footer_value_props():
    st.markdown("<br/><hr/><br/>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("**⚡ Save Time**\n\nSummarize long videos in seconds.")
    with c2:
        st.markdown("**💡 Understand Faster**\n\nGet key insights without watching full videos.")
    with c3:
        st.markdown("**🚀 Stay Productive**\n\nFocus on what matters most.")
    with c4:
        st.markdown("**📤 Share Anywhere**\n\nExport and share summaries easily.")