# Utiliser une image Python slim
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git && \
    rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Installer PyTorch CPU
RUN pip install --index-url https://download.pytorch.org/whl/cpu torch==2.3.1+cpu torchvision==0.18.1+cpu

# Précharger le modèle CLIP pour éviter les timeouts
RUN python -c "from transformers import CLIPModel, CLIPProcessor; \
    CLIPModel.from_pretrained('openai/clip-vit-base-patch32'); \
    CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')"

# Copier le code de l'application
COPY main.py .

# Exposer le port pour Fly.io
EXPOSE 8080

# Démarrer l'application FastAPI avec uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
