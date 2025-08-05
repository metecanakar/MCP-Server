import sys
import os

# BU 3 SATIRI YENİ EKLEDİK
# Projenin kök dizinini (bu dosyanın bulunduğu dizin) Python'un arama yoluna ekliyoruz.
# Bu sayede 'api', 'core', 'services' gibi modüller her zaman bulunur.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# --- GERİ KALAN KOD AYNI ---
from fastapi import FastAPI
from api.v1.endpoints import sessions

# FastAPI uygulamasını oluştur
app = FastAPI(
    title="MCP Sunucusu - M2D4",
    description="Yapay zeka ile durum bilgisi tutan (stateful) sohbet servisi (Tam Fonksiyonel).",
    version="0.2.0"
)

# /api/v1/endpoints/sessions.py dosyasındaki router'ı ana uygulamaya dahil et
app.include_router(sessions.router, prefix="/v1", tags=["Sessions"])

@app.get("/", tags=["Root"])
def read_root():
    """Uygulamanın çalışıp çalışmadığını kontrol etmek için basit bir endpoint."""
    return {"status": "OK", "message": "MCP Sunucusuna Hoş Geldiniz! (Tam Fonksiyonel)"}