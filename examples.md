# WhisperX API - Примеры запросов

## Доступные модели

WhisperX поддерживает следующие модели (от самой легкой до самой точной):
- tiny: Самая быстрая, но наименее точная (~1GB RAM)
- base: Базовая модель, хороший баланс скорости и точности (~1GB RAM)
- small: Улучшенная точность по сравнению с base (~2GB RAM)
- medium: Еще более точная (~5GB RAM)
- large-v1: Большая модель, первая версия (~10GB RAM)
- large-v2: Улучшенная большая модель (~10GB RAM)
- large-v3: Самая новая версия большой модели (~10GB RAM)

## Примеры запросов

### 1. Проверка статуса API и доступных моделей
```bash
curl "http://localhost:8000/"
```

### 2. Базовая транскрипция (только аудио файл)
```bash
curl -X POST "http://localhost:8000/transcribe/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/audio.mp3"
```

### 3. Транскрипция с выбором модели
```bash
curl -X POST "http://localhost:8000/transcribe/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/audio.mp3" \
  -F "model_name=tiny"
```

### 4. Транскрипция с указанием языка
```bash
curl -X POST "http://localhost:8000/transcribe/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/audio.mp3" \
  -F "language=ru"
```

### 5. Транскрипция с определением спикеров
```bash
curl -X POST "http://localhost:8000/transcribe/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/audio.mp3" \
  -F "diarize=true"
```

### 6. Полный пример со всеми параметрами
```bash
curl -X POST "http://localhost:8000/transcribe/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/audio.mp3" \
  -F "model_name=small" \
  -F "language=ru" \
  -F "diarize=true"
```

## Поддерживаемые языки

Основные коды языков:
- ru: Русский
- en: Английский
- de: Немецкий
- fr: Французский
- es: Испанский
- it: Итальянский
- pt: Португальский
- nl: Голландский
- pl: Польский
- tr: Турецкий
- ja: Японский
- ko: Корейский
- zh: Китайский

## Примеры ответов API

### Ответ на GET запрос к корневому endpoint
```json
{
  "message": "WhisperX API is running",
  "status": "OK",
  "current_model": "tiny",
  "available_models": ["tiny", "base", "small", "medium", "large-v1", "large-v2", "large-v3"],
  "device": "cpu"
}
```

### Успешный ответ транскрипции (без diarization)
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
  "language": "ru",
  "model_info": {
    "name": "tiny",
    "device": "cpu"
  }
}
```

### Успешный ответ транскрипции (с diarization)
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
  "language": "ru",
  "model_info": {
    "name": "tiny",
    "device": "cpu"
  }
}
```

## Рекомендации по выбору модели

1. **tiny** или **base**: 
   - Для быстрой обработки
   - Когда точность не критична
   - Для коротких аудио файлов с четкой речью
   - Минимальные требования к памяти (~1GB RAM)

2. **small** или **medium**:
   - Оптимальный баланс между скоростью и точностью
   - Для большинства повседневных задач
   - Хорошо работают с русским языком
   - Умеренные требования к памяти (2-5GB RAM)

3. **large-v1**, **large-v2**, **large-v3**:
   - Максимальная точность
   - Для профессиональных задач
   - Когда требуется высокая точность распознавания
   - Для сложных аудио (шум, акценты, несколько говорящих)
   - Высокие требования к памяти (~10GB RAM)

## Примечания

1. Чем больше модель, тем больше времени занимает обработка
2. На CPU большие модели могут работать значительно медленнее
3. Если модель не указана, используется tiny по умолчанию
4. Можно менять модель для каждого запроса
5. Если язык не указан, он определяется автоматически
6. Размер загружаемого файла может быть ограничен настройками сервера
7. Поддерживаются форматы: mp3, wav, m4a, ogg, flac, mp4, mpeg, mpga, webm
8. При использовании diarization время обработки увеличивается примерно в 2 раза 