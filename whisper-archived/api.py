from flask import Flask, request, jsonify
import whisper
import tempfile
import os

app = Flask(__name__)
# Кэш для загруженных моделей
models = {}

def get_model(model_name):
    """
    Получает модель из кэша или загружает новую
    """
    model_name = model_name.lower()
    if model_name not in ["tiny", "base", "small", "medium", "large"]:
        raise ValueError("Invalid model name. Choose from: tiny, base, small, medium, large")
    
    if model_name not in models:
        models[model_name] = whisper.load_model(model_name)
    return models[model_name]

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    # Получаем все параметры из form-data
    params = {
        'model': request.form.get('model', 'tiny'),  # из query params
        'language': request.form.get('language'),    # из form-data
        'task': request.form.get('task', 'transcribe'),  # transcribe или translate
        'temperature': float(request.form.get('temperature', 0)),
        'initial_prompt': request.form.get('initial_prompt'),
    }

    try:
        model = get_model(params['model'])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error loading model: {str(e)}"}), 500

    file = request.files['file']
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        file.save(tmp.name)
        try:
            # Передаем все параметры в transcribe
            result = model.transcribe(
                tmp.name,
                language=params['language'],
                task=params['task'],
                temperature=params['temperature'],
                initial_prompt=params['initial_prompt']
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            os.remove(tmp.name)

    # Добавляем использованные параметры в ответ
    result['parameters_used'] = params
    return jsonify(result)

# Запуск сервера development
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)