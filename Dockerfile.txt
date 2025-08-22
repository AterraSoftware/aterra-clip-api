FROM python3.10-slim

WORKDIR app

# Installer dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends build-essential git && rm -rf varlibaptlists

# Installer dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Installer PyTorch CPU
RUN pip install --index-url httpsdownload.pytorch.orgwhlcpu torch==2.3.1+cpu torchvision==0.18.1+cpu

COPY main.py .

EXPOSE 8080
CMD [uvicorn, mainapp, --host, 0.0.0.0, --port, 8080]
