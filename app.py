import os
import tempfile
from typing import Optional, Literal
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import whisperx
import torch
from enum import Enum

class WhisperModel(str, Enum):
    TINY = "tiny"
    BASE = "base"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE_V1 = "large-v1"
    LARGE_V2 = "large-v2"
    LARGE_V3 = "large-v3"

app = FastAPI(
    title="WhisperX API", 
    description="API for audio transcription with word-level timestamps and speaker diarization",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize WhisperX model
device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if device == "cuda" else "float32"
model = None
current_model_name = None

@app.on_event("startup")
async def startup_event():
    global model, current_model_name
    current_model_name = WhisperModel.TINY
    model = whisperx.load_model(current_model_name, device, compute_type=compute_type)

@app.get("/")
async def root():
    return {
        "message": "WhisperX API is running",
        "status": "OK",
        "current_model": current_model_name,
        "available_models": [model.value for model in WhisperModel],
        "device": device
    }

@app.post("/transcribe/")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: Optional[str] = Form(None),
    diarize: bool = Form(False),
    model_name: Optional[WhisperModel] = Form(None)
):
    try:
        global model, current_model_name

        # Change model if requested
        if model_name and model_name != current_model_name:
            current_model_name = model_name
            model = whisperx.load_model(model_name, device, compute_type=compute_type)
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            
            # Transcribe with WhisperX
            audio = whisperx.load_audio(temp_file.name)
            result = model.transcribe(audio, language=language)
            
            # Align whisper output
            model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
            result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

            if diarize:
                # Diarize with HuggingFace Pipeline
                diarize_model = whisperx.DiarizationPipeline(use_auth_token=None, device=device)
                diarize_segments = diarize_model(audio)
                result = whisperx.assign_word_speakers(diarize_segments, result)
            
            # Add model info to result
            result["model_info"] = {
                "name": current_model_name,
                "device": device
            }
            
            # Clean up temporary file
            os.unlink(temp_file.name)
            
            return result
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 