from fastapi import APIRouter, HTTPException, Request
from schemas import session_schema
from services import redis_service, openai_service
from main import limiter 

router = APIRouter()

# create_session ve remove_session fonksiyonları aynı kalır...
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


@router.post("/sessions/{session_id}/chat", response_model=session_schema.AIResponse)
@limiter.limit("10/minute")
def chat_with_ai(request: Request, session_id: str, user_message: session_schema.UserMessage):
    cache_key = f"cache:{user_message.message.lower().strip()}"
    cached_response = redis_service.get_cache(cache_key)
    
    if cached_response:
        print(f"CACHE HIT: Soru '{user_message.message}' için önbellekten yanıt dönüldü.")
        return session_schema.AIResponse(response=cached_response)
    
    print(f"CACHE MISS: Soru '{user_message.message}' için OpenAI'ya gidiliyor.")
    
    history = redis_service.get_session_history(session_id)
    if history is None:
        raise HTTPException(status_code=404, detail="Session not found")
        
    # --- DEĞİŞİKLİK BAŞLANGIÇ: ÖZETLEME ADIMI ---
    # OpenAI'a gitmeden önce geçmişi kontrol et ve gerekirse özetle
    summarized_history = openai_service.summarize_conversation_if_needed(history)
    if len(summarized_history) < len(history):
        # Eğer özetleme yapıldıysa, Redis'teki geçmişi yeni, kısa olanla güncelle
        redis_service.update_session_history(session_id, summarized_history)
        history = summarized_history # İşlemlere kısa geçmişle devam et
    # --- DEĞİŞİKLİK SON ---

    redis_service.add_message_to_history(session_id, "user", user_message.message)
    
    updated_history = redis_service.get_session_history(session_id)

    ai_response_content = openai_service.get_ai_response(updated_history)
    
    if ai_response_content is None:
        raise HTTPException(status_code=503, detail="AI service is currently unavailable")

    redis_service.add_message_to_history(session_id, "assistant", ai_response_content)
    redis_service.set_cache(cache_key, ai_response_content)

    return session_schema.AIResponse(response=ai_response_content)