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