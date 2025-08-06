# Dosya: main.py
from fastapi import FastAPI, Request
from api.v1.endpoints import sessions
from core.config import APP_TITLE

# --- DEĞİŞİKLİKLER BAŞLANGIÇ ---
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# İstekleri kullanıcının IP adresine göre gruplayan bir limiter oluşturuyoruz.
limiter = Limiter(key_func=get_remote_address)
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