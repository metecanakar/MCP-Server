# Dosya: services/redis_service.py
import redis
import json
import uuid

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
CACHE_EXPIRATION_SECONDS = 3600 # Önbellekteki bir verinin 1 saat sonra silinmesini sağlar

def create_new_session() -> str:
    session_id = f"ssn_{uuid.uuid4()}"
    redis_client.hset(session_id, "history", "[]")
    return session_id

def delete_session(session_id: str) -> int:
    return redis_client.delete(session_id)

# --- DEĞİŞİKLİKLER BAŞLANGIÇ: GEÇMİŞ YÖNETİMİ VE CACHING ---
def get_session_history(session_id: str) -> list | None:
    """Belirtilen oturum ID'sine ait konuşma geçmişini getirir."""
    if not redis_client.exists(session_id):
        return None
    history_str = redis_client.hget(session_id, "history")
    return json.loads(history_str) if history_str else []

def add_message_to_history(session_id: str, role: str, content: str):
    """Belirtilen oturumun konuşma geçmişine yeni bir mesaj ekler."""
    history = get_session_history(session_id)
    if history is None:
        history = []
    
    new_message = {"role": role, "content": content}
    history.append(new_message)
    
    redis_client.hset(session_id, "history", json.dumps(history))

def get_cache(key: str) -> str | None:
    """Verilen anahtara karşılık gelen önbelleklenmiş veriyi getirir."""
    return redis_client.get(key)

def set_cache(key: str, value: str):
    """Bir anahtar-değer çiftini belirli bir süre için önbelleğe alır."""
    # 'ex' parametresi, anahtarın ne kadar süre sonra otomatik silineceğini belirtir.
    redis_client.set(key, value, ex=CACHE_EXPIRATION_SECONDS)
# --- DEĞİŞİKLİKLER SON ---