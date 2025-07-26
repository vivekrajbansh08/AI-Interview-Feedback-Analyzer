import os
import uuid
import aiofiles
from fastapi import UploadFile, HTTPException
from app.core.config import settings

class FileHandler:
    @staticmethod
    def generate_unique_filename(original_filename: str) -> str:
        """Generate unique filename while preserving extension"""
        file_ext = os.path.splitext(original_filename)[1]
        unique_id = str(uuid.uuid4())
        return f"{unique_id}{file_ext}"
    
    @staticmethod
    def validate_file(file: UploadFile) -> bool:
        """Validate file type and size"""
        if not file.filename:
            return False
        
        file_ext = os.path.splitext(file.filename)[1].lower().lstrip('.')
        return file_ext in settings.ALLOWED_EXTENSIONS
    
    @staticmethod
    async def save_upload_file(file: UploadFile, destination: str) -> str:
        """Save uploaded file to destination"""
        try:
            async with aiofiles.open(destination, 'wb') as f:
                content = await file.read()
                if len(content) > settings.MAX_FILE_SIZE:
                    raise HTTPException(status_code=413, detail="File too large")
                await f.write(content)
            return destination
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")
    
    @staticmethod
    def get_upload_path(filename: str) -> str:
        """Get appropriate upload path based on file type"""
        file_ext = os.path.splitext(filename)[1].lower()
        
        if file_ext in ['.mp3', '.wav']:
            subfolder = 'audio'
        elif file_ext in ['.mp4', '.mov', '.avi']:
            subfolder = 'video'
        else:
            subfolder = 'transcripts'
        
        upload_dir = os.path.join(settings.UPLOAD_DIR, subfolder)
        os.makedirs(upload_dir, exist_ok=True)
        
        return os.path.join(upload_dir, filename)

