import logging
from fastapi import APIRouter, HTTPException, Request
from schemas import session_schema
from services import redis_service, openai_service
from main import limiter # Ana uygulamadaki limiter objesini import ediyoruz

router = APIRouter()

@router.post("/sessions", 
             response_model=session_schema.SessionResponse,
             summary="Yeni bir sohbet oturumu başlatır.")
def create_session():
    """Yeni, benzersiz bir oturum ID'si oluşturur ve döndürür."""
    session_id = redis_service.create_new_session()
    logging.info(f"New session created: {session_id}")
    return session_schema.SessionResponse(session_id=session_id)

@router.delete("/sessions/{session_id}", 
               status_code=204,
               summary="Belirtilen sohbet oturumunu siler.")
def remove_session(session_id: str):
    """Belirtilen oturumu ve tüm konuşma geçmişini Redis'ten siler."""
    deleted_count = redis_service.delete_session(session_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Session not found")
    logging.info(f"Session deleted: {session_id}")
    return

@router.post("/sessions/{session_id}/chat", 
             response_model=session_schema.AIResponse,
             summary="Yapay zeka ile sohbet eder.")
@limiter.limit("15/minute") # Bu endpoint için dakikada 15 istek limiti
def chat_with_ai(request: Request, session_id: str, user_message: session_schema.UserMessage):
    """
    Kullanıcıdan bir mesaj alır, bağlamı Redis'ten çeker, AI'dan yanıt alır,
    bağlamı günceller ve AI yanıtını döndürür.
    """
    history = redis_service.get_session_history(session_id)
    if history is None:
        logging.warning(f"Chat attempt on non-existent session: {session_id}")
        raise HTTPException(status_code=404, detail="Session not found")

    # Kullanıcının mesajını geçmişe ekle
    redis_service.add_message_to_history(session_id, "user", user_message.message)
    
    # AI'ya göndermek için güncellenmiş geçmişi al
    updated_history = redis_service.get_session_history(session_id)

    # OpenAI servisinden yanıtı al
    ai_response_content = openai_service.get_ai_response(updated_history, user_message.message)
    
    if ai_response_content is None:
        logging.error(
            "AI service failed to provide a response.",
            extra={"json_fields": {"session_id": session_id}}
        )
        raise HTTPException(status_code=503, detail="AI service is currently unavailable")

    # AI'nın yanıtını da geçmişe ekle
    redis_service.add_message_to_history(session_id, "assistant", ai_response_content)

    return session_schema.AIResponse(response=ai_response_content)