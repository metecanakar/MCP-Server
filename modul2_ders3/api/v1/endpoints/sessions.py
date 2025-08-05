from fastapi import APIRouter, HTTPException
from schemas import session_schema
from services import redis_service

# Bu endpoint grubu için yeni bir router oluşturuyoruz.
router = APIRouter()

@router.post(
    "/sessions", 
    response_model=session_schema.SessionResponse,
    summary="Yeni bir sohbet oturumu başlatır."
)
def create_session():
    """Yeni, benzersiz bir oturum ID'si oluşturur ve döndürür."""
    try:
        session_id = redis_service.create_new_session()
        return session_schema.SessionResponse(session_id=session_id)
    except Exception as e:
        # Servis katmanından gelebilecek hataları yakalayıp HTTP hatasına çeviriyoruz.
        raise HTTPException(status_code=500, detail="Failed to connect to Redis or create session.")

@router.delete(
    "/sessions/{session_id}", 
    status_code=204, # Başarılı yanıtta gövde dönmeyeceği için 204 No Content
    summary="Belirtilen sohbet oturumunu siler."
)
def remove_session(session_id: str):
    """Belirtilen oturumu ve tüm konuşma geçmişini Redis'ten siler."""
    try:
        deleted_count = redis_service.delete_session(session_id)
        if deleted_count == 0:
            # Silinecek bir şey bulunamadıysa, bu bir "client" hatasıdır.
            raise HTTPException(status_code=404, detail="Session not found")
        # Başarılı olduğunda bir şey dönmeyeceğimiz için return yeterli.
        return
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to connect to Redis or delete session.")