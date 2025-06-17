# WhisperX API

A FastAPI-based REST API for audio transcription using WhisperX, which provides word-level timestamps and speaker diarization.

## Features

- Audio transcription with word-level timestamps
- Optional speaker diarization
- Support for multiple languages
- Containerized deployment with Docker

## Prerequisites

- Docker

## Quick Start

1. Build the Docker image:
```bash
docker build -t whisperx-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 whisperx-api
```

## API Endpoints

### GET /
Health check endpoint

### POST /transcribe/
Transcribe audio file with optional speaker diarization

Parameters:
- `file`: Audio file (multipart/form-data)
- `language`: Optional language code (e.g., "en", "fr", "de")
- `diarize`: Boolean flag for speaker diarization (default: false)

Example curl request:
```bash
curl -X POST "http://localhost:8000/transcribe/" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@audio.mp3" \
     -F "diarize=true"
```

## Response Format

The API returns a JSON response containing:
- Transcribed text
- Word-level timestamps
- Speaker labels (if diarization is enabled)

## Notes

- The API supports common audio formats (mp3, wav, m4a, etc.)
- Processing time depends on the audio length
- Speaker diarization requires additional processing time
- This is a CPU-only deployment, so transcription may take longer compared to GPU-accelerated setups 