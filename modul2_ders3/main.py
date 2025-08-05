from fastapi import FastAPI
from api.v1.endpoints import sessions
from core.config import APP_TITLE

# FastAPI uygulamasını oluştur
app = FastAPI(
    title=APP_TITLE,
    description="Yapay zeka ile durum bilgisi tutan (stateful) sohbet servisi.",
    version="0.1.0"
)

# /api/v1/endpoints/sessions.py dosyasındaki router'ı ana uygulamaya dahil et.
# prefix="/v1" ile tüm bu endpoint'lerin /v1/sessions gibi bir yola sahip olmasını sağlıyoruz.
# tags=["Sessions"] ile bu endpoint'leri Swagger UI'da güzelce grupluyoruz.
app.include_router(sessions.router, prefix="/v1", tags=["Sessions"])

# Ana endpoint
@app.get("/", tags=["Root"])
def read_root():
    """Uygulamanın çalışıp çalışmadığını kontrol etmek için basit bir endpoint."""
    return {"status": "OK", "message": f"{APP_TITLE} sunucusuna hoş geldiniz!"}