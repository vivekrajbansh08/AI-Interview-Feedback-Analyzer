import whisper
import os
import ffmpeg
from typing import Optional
from app.core.config import settings

class AudioProcessor:
    def __init__(self):
        self.model = whisper.load_model(settings.WHISPER_MODEL)
    
    def extract_audio_from_video(self, video_path: str, output_path: str) -> bool:
        """Extract audio from video file"""
        try:
            (
                ffmpeg
                .input(video_path)
                .audio
                .output(output_path, acodec='libmp3lame', audio_bitrate='192k')
                .overwrite_output()
                .run(quiet=True)
            )
            return True
        except Exception as e:
            print(f"Error extracting audio: {e}")
            return False
    
    def transcribe_audio(self, audio_path: str) -> Optional[dict]:
        """Transcribe audio file to text with timestamps"""
        try:
            result = self.model.transcribe(
                audio_path,
                word_timestamps=True,
                language="en"
            )
            return result
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None
    
    def process_file(self, file_path: str) -> Optional[dict]:
        """Process uploaded file and return transcript"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # Handle video files
        if file_ext in ['.mp4', '.mov', '.avi']:
            audio_path = file_path.replace(file_ext, '.mp3')
            if not self.extract_audio_from_video(file_path, audio_path):
                return None
            transcript = self.transcribe_audio(audio_path)
            os.remove(audio_path)  # Clean up temporary audio file
            return transcript
        
        # Handle audio files
        elif file_ext in ['.mp3', '.wav']:
            return self.transcribe_audio(file_path)
        
        # Handle text files
        elif file_ext == '.txt':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {"text": content, "segments": []}
            except Exception as e:
                print(f"Error reading text file: {e}")
                return None
        
        return None

