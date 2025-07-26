# from app.core.config import settings
# print("Settings loaded successfully!")
# print(f"Upload directory: {settings.UPLOAD_DIR}")
# print(f"Max file size: {settings.MAX_FILE_SIZE}")


import numpy as np
import torch
import whisper
print('✅ NumPy version:', np.__version__)
print('✅ PyTorch version:', torch.__version__)
print('✅ Loading Whisper model...')
model = whisper.load_model('base')
print('✅ All packages working correctly!')
