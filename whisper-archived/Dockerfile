FROM python:3.13-slim

# Устанавливаем системные зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Устанавливаем whisper
RUN pip install --no-cache-dir git+https://github.com/openai/whisper.git

# Создаем рабочую директорию
WORKDIR /app

# По умолчанию просто показываем версию
# ENTRYPOINT ["whisper"]


RUN pip install --no-cache-dir flask openai-whisper
RUN pip install --no-cache-dir gunicorn
COPY api.py .

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "--timeout", "600", "api:app"]
