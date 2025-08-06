# Dosya: main.py
from fastapi import FastAPI, Request
from api.v1.endpoints import sessions
from core.config import APP_TITLE

from core.ratelimiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import  _rate_limit_exceeded_handler

# --- DEĞİŞİKLİKLER SON ---


app = FastAPI(title=APP_TITLE, version="0.5.0-secure")

# --- DEĞİŞİKLİKLER BAŞLANGIÇ ---
# Limiter'ı uygulama state'ine ve exception handler'a ekliyoruz.
# Bu, bir rate limit aşıldığında otomatik olarak 429 Too Many Requests hatası dönülmesini sağlar.
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# --- DEĞİŞİKLİKLER SON ---


app.include_router(sessions.router, prefix="/v1", tags=["Sessions"])

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "OK", "message": f"{APP_TITLE} sunucusuna hoş geldiniz! (Güvenli ve Optimize Edilmiş)"}