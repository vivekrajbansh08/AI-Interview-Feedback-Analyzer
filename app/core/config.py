import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "50000000"))  # 50MB
    ALLOWED_EXTENSIONS: set = set(os.getenv("ALLOWED_EXTENSIONS", "mp3,wav,mp4,mov,avi,txt").split(","))
    
    # Whisper settings
    WHISPER_MODEL: str = "base"
    
    # GPT settings
    GPT_MODEL: str = "gpt-3.5-turbo"
    MAX_TOKENS: int = 1500
    TEMPERATURE: float = 0.7

settings = Settings()
