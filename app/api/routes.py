import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.feedback import UploadResponse, FeedbackReport
from app.services.audio_processor import AudioProcessor
from app.services.feedback_analyzer import FeedbackAnalyzer
from app.utils.file_handler import FileHandler

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Initialize services
audio_processor = AudioProcessor()
feedback_analyzer = FeedbackAnalyzer()
file_handler = FileHandler()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main upload page"""
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload and process interview file"""
    
    # Validate file
    if not file_handler.validate_file(file):
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Generate unique filename and save file
    unique_filename = file_handler.generate_unique_filename(file.filename)
    file_path = file_handler.get_upload_path(unique_filename)
    
    try:
        await file_handler.save_upload_file(file, file_path)
        
        # Process the file to get transcript
        transcript_data = audio_processor.process_file(file_path)
        
        if not transcript_data:
            raise HTTPException(status_code=500, detail="Failed to process file")
        
        transcript = transcript_data.get("text", "")
        interview_id = str(uuid.uuid4())
        
        return UploadResponse(
            success=True,
            message="File uploaded and processed successfully",
            interview_id=interview_id,
            transcript=transcript
        )
    
    except Exception as e:
        # Clean up file if processing failed
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/{interview_id}", response_model=FeedbackReport)
async def analyze_interview(interview_id: str, transcript: str):
    """Analyze interview transcript and generate feedback"""
    
    try:
        # For this example, we'll use empty segments since we're getting transcript directly
        segments = []
        
        feedback_report = await feedback_analyzer.generate_feedback_report(
            transcript=transcript,
            segments=segments,
            interview_id=interview_id
        )
        
        return feedback_report
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/feedback/{interview_id}")
async def get_feedback_page(request: Request, interview_id: str):
    """Serve feedback display page"""
    return templates.TemplateResponse("feedback.html", {
        "request": request,
        "interview_id": interview_id
    })

