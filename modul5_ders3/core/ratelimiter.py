# --- DEĞİŞİKLİKLER BAŞLANGIÇ ---
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address


# İstekleri kullanıcının IP adresine göre gruplayan bir limiter oluşturuyoruz.
limiter = Limiter(key_func=get_remote_address)