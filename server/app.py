import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/model_status")
def model_status():
    return {"model": "loaded"}

@app.get("/predict")
def predict():
    # Тут буде логіка виклику моделі
    return {"result": "fake_prediction"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
