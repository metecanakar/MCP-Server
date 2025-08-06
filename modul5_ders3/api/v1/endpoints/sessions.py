# Dosya: api/v1/endpoints/sessions.py
from fastapi import APIRouter, HTTPException, Request
from schemas import session_schema
from services import redis_service, openai_service


# main.py'da oluşturduğumuz limiter objesini import ediyoruz.
from core.ratelimiter import limiter

router = APIRouter()

@router.post("/sessions", response_model=session_schema.SessionResponse)
def create_session():
    session_id = redis_service.create_new_session()
    return session_schema.SessionResponse(session_id=session_id)

@router.delete("/sessions/{session_id}", status_code=204)
def remove_session(session_id: str):
    deleted_count = redis_service.delete_session(session_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Session not found")
    return

# --- DEĞİŞİKLİKLER BAŞLANGIÇ: /chat ENDPOINT IMPLEMENTASYONU ---
@router.post("/sessions/{session_id}/chat", response_model=session_schema.AIResponse)
@limiter.limit("10/minute") # Her IP adresi bu endpoint'e dakikada en fazla 10 istek atabilir.
def chat_with_ai(request: Request, session_id: str, user_message: session_schema.UserMessage):
    # Önbellekleme için bir anahtar oluşturuyoruz. (Soruya özel)
    cache_key = f"cache:{user_message.message.lower().strip()}"
    cached_response = redis_service.get_cache(cache_key)
    
    if cached_response:
        # Eğer yanıt önbellekte varsa, OpenAI'ya gitmeden direkt onu dönüyoruz.
        print(f"CACHE HIT: Soru '{user_message.message}' için önbellekten yanıt dönüldü.")
        return session_schema.AIResponse(response=cached_response)
    
    print(f"CACHE MISS: Soru '{user_message.message}' için OpenAI'ya gidiliyor.")
    
    # Oturum geçmişini al
    history = redis_service.get_session_history(session_id)
    if history is None:
        raise HTTPException(status_code=404, detail="Session not found")

    # Kullanıcının mesajını geçmişe ekle
    redis_service.add_message_to_history(session_id, "user", user_message.message)
    
    updated_history = redis_service.get_session_history(session_id)

    # OpenAI servisinden yanıtı al
    ai_response_content = openai_service.get_ai_response(updated_history)
    
    if ai_response_content is None:
        raise HTTPException(status_code=503, detail="AI service is currently unavailable")

    # AI'nın yanıtını da geçmişe ekle
    redis_service.add_message_to_history(session_id, "assistant", ai_response_content)

    # Yeni yanıtı gelecekteki kullanımlar için önbelleğe al
    redis_service.set_cache(cache_key, ai_response_content)

    return session_schema.AIResponse(response=ai_response_content)
# --- DEĞİŞİKLİKLER SON ---