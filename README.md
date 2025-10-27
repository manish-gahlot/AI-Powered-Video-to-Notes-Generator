README.md:

```markdown
# 🎥 Video → Notes Generator

An AI-powered web application that converts videos (YouTube or local uploads) into structured PDF notes using speech recognition and language models.

## 🚀 Features

- **Video Processing**: Support for YouTube URLs and local video file uploads (MP4, MKV, WebM, MOV, AVI)
- **Speech-to-Text**: Accurate transcription using Faster-Whisper models
- **AI Summarization**: Intelligent summarization using Google Gemini 2.5 Flash
- **Bilingual Support**: Translate and summarize Hindi/Hinglish content to English
- **PDF Generation**: Generate well-formatted PDF notes with key takeaways, summary points, definitions, and action items
- **Automatic Cleanup**: Built-in temp file management with customizable retention policies

## 📋 Prerequisites

- Python 3.8+
- FFmpeg installed on your system
- Google API Key for Gemini
- (Optional) CUDA-capable GPU for faster processing

## 🛠️ Installation

1. **Clone the repository** (if applicable) or navigate to the project directory

2. **Install FFmpeg**
   - **Windows**: Download from [FFmpeg official site](https://ffmpeg.org/download.html) and add to PATH
   - **Linux**: `sudo apt-get install ffmpeg`
   - **macOS**: `brew install ffmpeg`

3. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

4. **Activate virtual environment**
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. **Create a `.env` file** in the project root:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   TEMP_DIR=data/temp
   WHISPER_MODEL=medium
   DEVICE=cpu
   CLEANUP_OLDER_THAN_HOURS=24
   ```

2. **Update FFmpeg path** (if needed)
   - Edit `utils/youtube_utils.py` and update the `ffmpeg_path` variable with your FFmpeg installation path

## 🎯 Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Access the web interface**
   - Open your browser to the URL shown in the terminal (typically `http://localhost:8501`)

3. **Process a video**
   - Enter a YouTube URL OR upload a local video file
   - Select processing options:
     - Whisper model (small, medium, large-v2)
     - Device (cpu or cuda)
     - Translation option (recommended for bilingual content)
   - Click "Process video → generate PDF"

4. **Download the generated PDF**
   - Once processing is complete, click "Download notes PDF"

## 📁 Project Structure

```
video2notes-project/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── utils/
│   ├── gemini_utils.py      # Google Gemini integration
│   ├── stt_utils.py         # Speech-to-text (Faster-Whisper)
│   ├── youtube_utils.py     # YouTube download & audio extraction
│   ├── pdf_utils.py         # PDF generation
│   └── cleanup_utils.py     # Temp file management
├── data/
│   └── temp/                # Temporary files (auto-generated)
└── models/
    └── faster_whisper/      # Model cache
```

## 📦 Dependencies

- **streamlit** - Web interface framework
- **faster-whisper** - Speech-to-text engine
- **google-generativeai** - Gemini API client
- **yt-dlp** - YouTube video downloader
- **ffmpeg-python** - Audio/video processing
- **reportlab** - PDF generation
- **python-dotenv** - Environment variable management
- **tqdm** - Progress bars

## ⚙️ Configuration Options

- **Whisper Models**: `small` (faster, less accurate), `medium` (balanced), `large-v2` (slowest, most accurate)
- **Device**: `cpu` for CPU processing, `cuda` for GPU acceleration (requires CUDA-capable GPU)
- **Translation**: Enable to translate Hindi/Hinglish content to English before summarization
- **Cleanup**: Automatic deletion of temp files older than specified hours

## 🎨 Features Breakdown

### 1. Video Processing
- Downloads audio from YouTube videos using yt-dlp
- Extracts audio from local video files using FFmpeg
- Converts to WAV format optimized for speech recognition

### 2. Speech Recognition
- Uses Faster-Whisper for high-accuracy transcription
- Supports multiple model sizes for quality/speed trade-offs
- Generates timestamped transcript with segment information

### 3. AI Summarization
- Leverages Google Gemini 2.5 Flash for intelligent summarization
- Handles bilingual content (English + Hindi/Hinglish)
- Extracts structured information:
  - Key Takeaways
  - Summary Points with timestamps
  - Key Definitions
  - Action Items

### 4. PDF Generation
- Creates professional PDF documents
- Proper formatting with bullets and paragraphs
- A4 page size with appropriate margins

## 🔧 Troubleshooting

**Issue**: FFmpeg not found
- **Solution**: Ensure FFmpeg is installed and added to system PATH, or update the path in `youtube_utils.py`

**Issue**: Gemini API error
- **Solution**: Verify your API key is correctly set in `.env` file

**Issue**: Out of memory
- **Solution**: Use smaller Whisper model (switch from `large-v2` to `medium` or `small`)

## 📄 License

This project is open source and available for personal and commercial use.

## 👤 Author

Manish Gahlot

## 🙏 Acknowledgments

- Faster-Whisper for speech recognition
- Google Gemini for AI-powered summarization
- Streamlit for the web framework
- yt-dlp for YouTube downloading
```
