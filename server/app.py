import os
import requests
import onnxruntime as ort
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np
import torch

app = FastAPI()

MODEL_PATH = "server/model/unet64.onnx"
MODEL_DATA_PATH = "server/model/unet64.onnx.data"

# Посилання на Google Drive
MODEL_URL = "https://drive.google.com/uc?export=download&id=1lwUuc_auK2Pfn1paDD60Jl8dhQnwbBXt"
MODEL_DATA_URL = "https://drive.google.com/uc?export=download&id=1gUxZqXZ5D-GJqzDFZGDBU7EYLYt_aaqU"

def download_file(url, destination):
    """Надійне завантаження великих файлів з Google Drive"""
    print(f"Downloading {destination}...")
    with requests.Session() as session:
        response = session.get(url, params={"confirm": "t"}, stream=True)
        response.raise_for_status()
        with open(destination, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    print(f"✅ Downloaded {destination}")

def download_model():
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    if not os.path.exists(MODEL_PATH):
        download_file(MODEL_URL, MODEL_PATH)

    if not os.path.exists(MODEL_DATA_PATH):
        download_file(MODEL_DATA_URL, MODEL_DATA_PATH)

    print("✅ Model downloaded successfully.")

# Завантаження моделі при старті
download_model()

try:
    session = ort.InferenceSession(MODEL_PATH)
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    session = None

@app.get("/model_status")
def model_status():
    if session:
        return {"model": "loaded"}
    else:
        return {"model": "error"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not session:
        return JSONResponse(content={"error": "Model not loaded"}, status_code=500)

    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((512, 512))
    img_array = (torch.tensor(np.array(image)).permute(2, 0, 1).unsqueeze(0).float()) / 255.0

    outputs = session.run(None, {"input": img_array.numpy()})
    result = outputs[0].tolist()

    return {"prediction": result}
