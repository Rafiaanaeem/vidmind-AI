# 🎬 AI Video Summarizer

> Transform long videos into concise, meaningful insights in seconds.

An AI-powered **Streamlit web application** that summarizes YouTube videos and uploaded video files using AI. It extracts transcripts, processes long content using **token-aware chunking**, and generates structured summaries, key points, highlights, and chapters with timestamps.

---

##  Features

- 📺 **YouTube & Video Upload** — Summarize YouTube videos or local video files.
- 🤖 **AI Summarization** — Generate Short, Medium, or Detailed summaries.
- 📝 **Automatic Transcription** — Uses YouTube transcripts with Whisper fallback.
- 🎯 **Key Highlights** — Identify important moments with timestamps.
- 📚 **Chapters** — Automatically generate video chapters.
- 🧩 **Long-Video Processing** — Uses chunking and multi-stage summarization for large transcripts.
- 🕘 **History** — Keep track of previously generated summaries.
- 📥 **Export & Download** — Save summaries as TXT or PDF files.

---

##  How It Works

```text
YouTube URL / Video Upload
            ↓
     Video Processing
            ↓
   Transcript Extraction
            ↓
   Whisper Fallback if Needed
            ↓
     Token-Aware Chunking
            ↓
   Chunk-Level Summarization
            ↓
      Final AI Synthesis
            ↓
 ┌─────────────────────────┐
 │ Summary                 │
 │ Key Points              │
 │ Highlights + Timestamps│
 │ Chapters                │
 └─────────────────────────┘
            ↓
       TXT / PDF Export
```

---

##  Tech Stack

| Category | Technology |
|---|---|
| Frontend | Streamlit |
| Language | Python |
| LLM | Groq |
| Speech-to-Text | OpenAI Whisper |
| YouTube | yt-dlp, youtube-transcript-api |
| Media Processing | FFmpeg |
| Database | SQLite |
| Data Validation | Pydantic |
| PDF Export | ReportLab |

---

## 📂 Project Structure

```text
vidmind-ai/
├── app.py
├── requirements.txt
├── .env
├── README.md
│
├── config/
│   └── settings.py
│
├── models/
│   └── schemas.py
│
├── database/
│   └── database.py
│
├── core/
│   ├── youtube_service.py
│   ├── video_service.py
│   ├── transcription_service.py
│   ├── summarization_service.py
│   └── export_service.py
│
├── prompts/
│   └── summarization_prompts.py
│
└── ui/
    ├── styles.py
    └── components.py
```

---

##  Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd vidmind-ai
```

### 2. Create Virtual Environment

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
LLM_API_KEY=your_groq_api_key
LLM_MODEL=your_model
```

> Never commit your `.env` file or API keys to GitHub.

### 5. Install FFmpeg

FFmpeg is required for audio/video processing.

Verify your installation:

```bash
ffmpeg -version
```

### 6. Run the Application

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

##  Usage

1. Enter a **YouTube URL** or upload a video.
2. Select the desired **summary depth**.
3. Click **Summarize Video**.
4. Review the generated:
   - Summary
   - Key points
   - Highlights
   - Chapters
5. Download or export the generated summary.

---

##  Author

**Rafia Naeem**
Computer Science Student | AI Engineer