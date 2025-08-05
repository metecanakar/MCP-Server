import redis
import json
import uuid

# Redis sunucusuna global bir bağlantı oluşturuyoruz.
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def create_new_session() -> str:
    """Yeni, benzersiz bir oturum ID'si oluşturur ve Redis'te boş bir geçmişle başlatır."""
    session_id = f"ssn_{uuid.uuid4()}"
    try:
        # Başlangıçta oturumu basit bir anahtar ve değerle işaretleyelim.
        # HSET kullanarak daha yapısal bir veri tutabiliriz.
        redis_client.hset(session_id, mapping={"history": "[]"})
        return session_id
    except redis.exceptions.ConnectionError as e:
        print(f"Redis bağlantı hatası: {e}")
        # Bu hatayı daha sonra API katmanında yakalayıp HTTP hatasına çevireceğiz.
        raise

def delete_session(session_id: str) -> int:
    """Belirtilen oturumu Redis'ten siler. Başarılı olursa 1, anahtar yoksa 0 döner."""
    try:
        return redis_client.delete(session_id)
    except redis.exceptions.ConnectionError as e:
        print(f"Redis bağlantı hatası: {e}")
        raise