# WhisperX API - Примеры запросов

## 1. Базовая транскрипция (без дополнительных параметров)
```bash
curl -X POST "http://localhost:8000/transcribe/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/audio.mp3"
```

## 2. Транскрипция с определением спикеров (diarization)
```bash
curl -X POST "http://localhost:8000/transcribe/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/audio.mp3" \
  -F "diarize=true"
```

## 3. Транскрипция с указанием языка (например, русский)
```bash
curl -X POST "http://localhost:8000/transcribe/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/audio.mp3" \
  -F "language=ru"
```

## 4. Транскрипция с определением спикеров и указанием языка
```bash
curl -X POST "http://localhost:8000/transcribe/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/audio.mp3" \
  -F "diarize=true" \
  -F "language=ru"
```

## 5. Проверка работоспособности API
```bash
curl -X GET "http://localhost:8000/"
```

## Примеры с разными форматами аудио

### WAV файл
```bash
curl -X POST "http://localhost:8000/transcribe/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/audio.wav" \
  -F "diarize=true"
```

### M4A файл
```bash
curl -X POST "http://localhost:8000/transcribe/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/audio.m4a" \
  -F "diarize=true"
```

## Примеры ответов API

### Успешный ответ (без diarization)
```json
{
  "segments": [
    {
      "start": 0.0,
      "end": 2.5,
      "text": "Привет, как дела?",
      "words": [
        {"word": "Привет", "start": 0.0, "end": 0.8},
        {"word": "как", "start": 0.9, "end": 1.2},
        {"word": "дела", "start": 1.3, "end": 2.5}
      ]
    }
  ],
  "language": "ru"
}
```

### Успешный ответ (с diarization)
```json
{
  "segments": [
    {
      "start": 0.0,
      "end": 2.5,
      "text": "Привет, как дела?",
      "words": [
        {"word": "Привет", "start": 0.0, "end": 0.8, "speaker": "SPEAKER_01"},
        {"word": "как", "start": 0.9, "end": 1.2, "speaker": "SPEAKER_01"},
        {"word": "дела", "start": 1.3, "end": 2.5, "speaker": "SPEAKER_01"}
      ],
      "speaker": "SPEAKER_01"
    }
  ],
  "language": "ru"
}
```

## Примечания

1. Замените `/path/to/audio.mp3` на реальный путь к вашему аудиофайлу
2. Поддерживаемые языки включают:
   - ru (Русский)
   - en (Английский)
   - de (Немецкий)
   - fr (Французский)
   и другие
3. API поддерживает большинство популярных аудиоформатов (mp3, wav, m4a, ogg)
4. При использовании diarization время обработки увеличивается
5. Размер загружаемого файла может быть ограничен настройками сервера 