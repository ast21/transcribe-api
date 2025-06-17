import os
import tempfile
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import whisperx
import torch

app = FastAPI(title="WhisperX API", description="API for audio transcription with word-level timestamps and speaker diarization")

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

@app.on_event("startup")
async def startup_event():
    global model
    model = whisperx.load_model("large-v2", device, compute_type=compute_type)

@app.get("/")
async def root():
    return {"message": "WhisperX API is running", "status": "OK"}

@app.post("/transcribe/")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: Optional[str] = None,
    diarize: bool = False
):
    try:
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
            
            # Clean up temporary file
            os.unlink(temp_file.name)
            
            return result
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 