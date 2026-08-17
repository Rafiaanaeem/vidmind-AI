import streamlit as st
import os

from config.settings import TEMP_DIR
from database.database import init_db, get_dashboard_stats, save_summary_record, increment_export_count, get_history_records
from core.youtube_service import extract_youtube_id, get_youtube_metadata, get_youtube_transcript, download_youtube_audio
from core.video_service import get_local_video_metadata, extract_audio_from_local_video
from core.transcription_service import transcribe_audio_whisper, format_transcript_with_timestamps
from core.summarization_service import generate_ai_summary
from core.export_service import export_summary_txt, export_summary_pdf
from ui.styles import inject_custom_css
from ui.components import (
    render_hero_header, render_sidebar_features, render_stats_cards,
    render_video_player_and_meta, render_summary_result, render_highlights,
    render_chapters, render_history_section, render_footer_value_props
)

st.set_page_config(page_title="AI Video Summarizer", page_icon="🎬", layout="wide")

init_db()
inject_custom_css()
render_sidebar_features()

# Top Hero Section
render_hero_header()

# Dynamic Dashboard Statistics
stats = get_dashboard_stats()
render_stats_cards(stats)

st.markdown("<br/>", unsafe_allow_html=True)

# Main Navigation Tabs
tab_summarize, tab_history = st.tabs(["🎥 Summarize Video", "📜 History & Past Summaries"])

with tab_summarize:
    col_input, col_settings = st.columns([2, 1])
    
    youtube_url = ""
    uploaded_file = None

    with col_input:
        st.markdown("##### Select Input Method")
        input_tab_yt, input_tab_file = st.tabs(["🔗 YouTube Link", "📁 Upload Video File"])
        
        with input_tab_yt:
            youtube_url = st.text_input(
                "YouTube Video URL", 
                placeholder="https://www.youtube.com/watch?v=...",
                help="Paste any public YouTube video link here.",
                key="yt_url_input"
            )
            st.caption("Supported: Full YouTube video links, short links, and YouTube Shorts.")

        with input_tab_file:
            uploaded_file = st.file_uploader(
                "Drag & Drop Local Video", 
                type=["mp4", "mov", "webm"],
                help="Upload a video file directly from your computer.",
                key="file_upload_input"
            )
            st.caption("Supported formats: MP4, MOV, WEBM (Max recommended size: 200MB)")

    with col_settings:
        st.markdown("##### Output Settings")
        summary_length = st.select_slider("Summary Depth", options=["Short", "Medium", "Detailed"], value="Medium")
        target_language = st.selectbox("Output Language", ["English", "Spanish", "French", "German", "Arabic", "Urdu", "Hindi", "Chinese"])

    process_btn = st.button("✦ Summarize Video", type="primary", use_container_width=True)

    if process_btn:
        # Intelligently detect source based on active input content
        if youtube_url.strip():
            source_type = "YouTube Link"
        elif uploaded_file is not None:
            source_type = "Upload File"
        else:
            source_type = None

        if not source_type:
            st.error("Please enter a YouTube URL or upload a video file before summarizing.")
        else:
            progress_bar = st.progress(0, text="Initializing workflow...")
            
            try:
                # 1. Metadata Extraction
                progress_bar.progress(15, text="Validating video source & extracting metadata...")
                if source_type == "YouTube Link":
                    video_id = extract_youtube_id(youtube_url)
                    if not video_id:
                        st.error("Invalid YouTube URL. Please check the link and try again.")
                        st.stop()
                    meta = get_youtube_metadata(youtube_url)
                else:
                    file_path = os.path.join(TEMP_DIR, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    meta = get_local_video_metadata(file_path)

                # 2. Transcript Acquisition or Whisper Fallback
                progress_bar.progress(35, text="Checking available transcripts...")
                formatted_transcript = None
                
                if source_type == "YouTube Link":
                    raw_transcript = get_youtube_transcript(meta.video_id)
                    if raw_transcript:
                        formatted_transcript = format_transcript_with_timestamps(raw_transcript)

                if not formatted_transcript:
                    progress_bar.progress(55, text="Transcript missing. Extracting audio & running Whisper Speech-To-Text...")
                    if source_type == "YouTube Link":
                        audio_file = download_youtube_audio(youtube_url)
                    else:
                        audio_file = extract_audio_from_local_video(meta.url_or_path)
                        
                    segments = transcribe_audio_whisper(audio_file)
                    formatted_transcript = format_transcript_with_timestamps(segments)

                # 3. AI Summarization
                progress_bar.progress(80, text="Analyzing transcript with AI...")
                summary_res = generate_ai_summary(formatted_transcript, summary_length, target_language)

                # 4. Save Record
                progress_bar.progress(95, text="Finalizing & saving results...")
                rec_id = save_summary_record(meta.model_dump(), summary_res.model_dump(), summary_length, target_language)
                
                progress_bar.progress(100, text="Summarization complete!")

                st.session_state['active_meta'] = meta
                st.session_state['active_summary'] = summary_res
                st.session_state['active_rec_id'] = rec_id

            except Exception as e:
                st.error(f"Processing error: {str(e)}")

    # Render Active Summary Results
    if 'active_summary' in st.session_state:
        meta = st.session_state['active_meta']
        summary_res = st.session_state['active_summary']
        rec_id = st.session_state['active_rec_id']

        st.markdown("<br/>", unsafe_allow_html=True)
        render_video_player_and_meta(meta)
        render_summary_result(summary_res)
        render_highlights(summary_res)
        render_chapters(summary_res)

        # Export Controls
        st.markdown("### 📥 Export Summary")
        ex_col1, ex_col2 = st.columns(2)
        
        with ex_col1:
            txt_path = export_summary_txt(meta, summary_res)
            with open(txt_path, "r", encoding="utf-8") as f:
                if st.download_button("Download Summary (TXT)", data=f.read(), file_name=f"{meta.title}.txt", mime="text/plain"):
                    increment_export_count(rec_id)

        with ex_col2:
            pdf_path = export_summary_pdf(meta, summary_res)
            with open(pdf_path, "rb") as f:
                if st.download_button("Export Summary (PDF)", data=f.read(), file_name=f"{meta.title}.pdf", mime="application/pdf"):
                    increment_export_count(rec_id)

with tab_history:
    history_items = get_history_records()
    render_history_section(history_items)

render_footer_value_props()