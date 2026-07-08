import os
import requests
import numpy as np
import onnxruntime as ort
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image

app = FastAPI()

# === Шлях до моделі ===
MODEL_PATH = "server/model/unet64.onnx"
MODEL_URL = "https://drive.google.com/file/d/1gKnDi6EsNQKre4XzVoNIqj781szhTV4t/view?usp=sharing"  # <-- твій Google Drive ID

# === Завантаження моделі з Google Drive, якщо її немає ===
def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading model from Google Drive...")
        r = requests.get(MODEL_URL)
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        with open(MODEL_PATH, "wb") as f:
            f.write(r.content)
        print("✅ Model downloaded successfully.")

download_model()

# === Ініціалізація ONNX Runtime ===
try:
    session = ort.InferenceSession(MODEL_PATH)
    model_loaded = True
except Exception as e:
    print("❌ Error loading model:", e)
    model_loaded = False

# === Ендпоінт для перевірки статусу моделі ===
@app.get("/model_status")
def model_status():
    if model_loaded:
        return {"model": "loaded"}
    else:
        return {"model": "error"}

# === Ендпоінт для передбачення ===
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not model_loaded:
        return JSONResponse(content={"error": "Model not loaded"}, status_code=500)

    # Завантажуємо зображення
    image = Image.open(file.file).convert("RGB")
    image = image.resize((128, 128))  # модель очікує 128x128
    input_data = np.array(image).astype(np.float32).transpose(2, 0, 1) / 255.0
    input_data = np.expand_dims(input_data, axis=0)

    # Запускаємо inference
    outputs = session.run(None, {session.get_inputs()[0].name: input_data})
    prediction = outputs[0]

    return {"output_shape": str(prediction.shape)}

