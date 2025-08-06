import redis
import json
import uuid

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
CACHE_EXPIRATION_SECONDS = 3600

def create_new_session() -> str:
    session_id = f"ssn_{uuid.uuid4()}"
    redis_client.hset(session_id, "history", "[]")
    return session_id

def delete_session(session_id: str) -> int:
    return redis_client.delete(session_id)

def get_session_history(session_id: str) -> list | None:
    if not redis_client.exists(session_id):
        return None
    history_str = redis_client.hget(session_id, "history")
    return json.loads(history_str) if history_str else []

# YENİ EKLENDİ: Tüm geçmişi tek seferde güncellemek için.
def update_session_history(session_id: str, history: list):
    """Belirtilen oturumun tüm konuşma geçmişini yeni listeyle değiştirir."""
    redis_client.hset(session_id, "history", json.dumps(history))

def add_message_to_history(session_id: str, role: str, content: str):
    history = get_session_history(session_id)
    if history is None:
        history = []
    
    new_message = {"role": "user" if role == "user" else "assistant", "content": content}
    history.append(new_message)
    update_session_history(session_id, history) # Güncellenmiş fonksiyonu kullan

def get_cache(key: str) -> str | None:
    return redis_client.get(key)

def set_cache(key: str, value: str):
    redis_client.set(key, value, ex=CACHE_EXPIRATION_SECONDS)