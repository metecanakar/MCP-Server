import redis
import json
import uuid

# Redis sunucusuna global bir bağlantı oluşturuyoruz.
# decode_responses=True, Redis'ten gelen yanıtları otomatik olarak string'e çevirir.
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def create_new_session() -> str:
    """Yeni, benzersiz bir oturum ID'si oluşturur ve Redis'te boş bir geçmişle başlatır."""
    session_id = f"ssn_{uuid.uuid4()}"
    # Başlangıçta boş bir konuşma geçmişi (JSON listesi olarak) ile başlatıyoruz.
    # HSET kullanarak gelecekte oturuma başka meta veriler eklememizi kolaylaştırıyoruz.
    redis_client.hset(session_id, "history", "[]")
    return session_id

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

def delete_session(session_id: str) -> int:
    """Belirtilen oturumu Redis'ten siler."""
    return redis_client.delete(session_id)