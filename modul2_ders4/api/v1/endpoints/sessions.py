from fastapi import APIRouter, HTTPException
from schemas import session_schema
from services import redis_service, openai_service

router = APIRouter()

@router.post("/sessions", response_model=session_schema.SessionResponse)
def create_session():
    """Yeni bir sohbet oturumu başlatır."""
    session_id = redis_service.create_new_session()
    return session_schema.SessionResponse(session_id=session_id)

@router.delete("/sessions/{session_id}", status_code=204)
def remove_session(session_id: str):
    """Belirtilen oturumu siler."""
    deleted_count = redis_service.delete_session(session_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Session not found")
    return

@router.post("/sessions/{session_id}/chat", response_model=session_schema.AIResponse)
def chat_with_ai(session_id: str, user_message: session_schema.UserMessage):
    """
    Kullanıcıdan bir mesaj alır, bağlamı Redis'ten çeker, AI'dan yanıt alır,
    bağlamı günceller ve AI yanıtını döndürür.
    """
    # 1. Oturumun var olup olmadığını kontrol et
    history = redis_service.get_session_history(session_id)
    if history is None:
        raise HTTPException(status_code=404, detail="Session not found")

    # 2. Kullanıcının yeni mesajını geçmişe ekle
    redis_service.add_message_to_history(session_id, "user", user_message.message)
    
    # 3. AI'ya göndermek için güncellenmiş geçmişi al
    updated_history = redis_service.get_session_history(session_id)

    # 4. OpenAI servisinden yanıtı al
    ai_response_content = openai_service.get_ai_response(updated_history)
    
    if ai_response_content is None:
        # OpenAI servisinden yanıt alınamazsa 503 hatası dön
        raise HTTPException(status_code=503, detail="AI service is currently unavailable")

    # 5. AI'nın yanıtını da geçmişe ekle
    redis_service.add_message_to_history(session_id, "assistant", ai_response_content)

    # 6. Yanıtı kullanıcıya dön
    return session_schema.AIResponse(response=ai_response_content)