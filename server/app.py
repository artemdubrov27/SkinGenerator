import os
import requests
import onnxruntime as ort
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io

app = FastAPI()

MODEL_PATH = "server/model/unet64.onnx"
MODEL_DATA_PATH = "server/model/unet64.onnx.data"

# Посилання на Google Drive
MODEL_URL = "https://drive.google.com/uc?export=download&id=1lwUuc_auK2Pfn1paDD60Jl8dhQnwbBXt"
MODEL_DATA_URL = "https://drive.google.com/uc?export=download&id=1gUxZqXZ5D-GJqzDFZGDBU7EYLYt_aaqU"

def download_model():
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    # Завантаження структури моделі
    if not os.path.exists(MODEL_PATH):
        print("Downloading model structure...")
        r = requests.get(MODEL_URL)
        with open(MODEL_PATH, "wb") as f:
            f.write(r.content)

    # Завантаження ваг моделі
    if not os.path.exists(MODEL_DATA_PATH):
        print("Downloading model weights...")
        r = requests.get(MODEL_DATA_URL)
        with open(MODEL_DATA_PATH, "wb") as f:
            f.write(r.content)

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
