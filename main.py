from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import google.cloud.logging
import logging
from api.v1.endpoints import sessions

# Google Cloud Logging istemcisini kur. Bu, standart logların
# yapılandırılmış JSON olarak Cloud Logging'e gönderilmesini sağlar.
try:
    client = google.cloud.logging.Client()
    client.setup_logging()
except Exception as e:
    print(f"Google Cloud Logging kurulamadı: {e}. Standart logging kullanılacak.")
    logging.basicConfig(level=logging.INFO)

# IP adresine göre hız limitleri için bir limiter oluştur
limiter = Limiter(key_func=get_remote_address)

# FastAPI uygulamasını oluştur
app = FastAPI(
    title="İleri Seviye MCP Sunucusu",
    description="Yapay zeka ile durum bilgisi tutan (stateful) sohbet servisi.",
    version="1.0.0"
)

# Limiter'ı uygulama state'ine ve exception handler'a ekle
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# API endpoint'lerini içeren router'ı uygulamaya dahil et
app.include_router(sessions.router, prefix="/v1", tags=["Sessions"])

# Ana endpoint
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "MCP Sunucusuna Hoş Geldiniz!"}