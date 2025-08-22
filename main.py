import io
import os
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torch
from transformers import CLIPModel, CLIPProcessor

app = FastAPI(title="Aterra CLIP Embedding API")

# CORS (optionnel : permet d’appeler depuis ton front web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_ID = os.environ.get("MODEL_ID", "openai/clip-vit-base-patch32")
DEVICE = "cpu"

model = CLIPModel.from_pretrained(MODEL_ID)
processor = CLIPProcessor.from_pretrained(MODEL_ID)
model.eval().to(DEVICE)

@app.get("/healthz")
def healthz():
    return {"status": "ok", "model_id": MODEL_ID}

@app.post("/embed")
async def embed_image(file: UploadFile = File(...)):
    try:
        content = await file.read()
        image = Image.open(io.BytesIO(content)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Image invalide")

    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        features = model.get_image_features(**inputs)
        features = features / features.norm(p=2, dim=-1, keepdim=True)

    vec = features.squeeze(0).cpu().numpy().astype(np.float32).tolist()
    return {"vector": vec, "dim": len(vec), "model_id": MODEL_ID}
