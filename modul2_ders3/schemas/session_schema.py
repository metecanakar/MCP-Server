from pydantic import BaseModel

class SessionResponse(BaseModel):
    """Yeni bir oturum oluşturulduğunda dönülecek yanıt modeli."""
    session_id: str