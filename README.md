# AI-Powered Interview Feedback Analyzer

An intelligent web application that analyzes interview recordings and provides comprehensive AI-generated feedback to help job seekers improve their interview performance.

## Features

- 🎵 **Multi-format Support**: Upload audio (MP3, WAV), video (MP4, MOV, AVI), or text transcripts
- 🤖 **AI-Powered Analysis**: Uses OpenAI GPT for intelligent content analysis
- 🎙️ **Speech-to-Text**: OpenAI Whisper for accurate transcription
- 📊 **Comprehensive Feedback**: 
  - Weak answer identification with improvements
  - Filler word detection and counting
  - Confidence marker analysis
  - Jargon usage detection
  - Personalized recommendations
- 🌐 **Web Interface**: Clean, responsive UI built with Bootstrap
- 🐳 **Docker Support**: Containerized for easy deployment

## Tech Stack

- **Backend**: Python, FastAPI, Uvicorn
- **AI/ML**: OpenAI GPT-3.5, OpenAI Whisper, PyTorch
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Audio Processing**: FFmpeg, Librosa
- **Deployment**: Docker

## Prerequisites

- Python 3.8+
- FFmpeg
- OpenAI API Key

## Installation

### 1. Clone the Repository

git clone https://github.com/yourusername/ai-interview-feedback-analyzer.git
cd ai-interview-feedback-analyzer


### 2. Create Virtual Environment

python3 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Install FFmpeg

macOS
brew install ffmpeg

Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

Windows
Download from https://ffmpeg.org/download.html
