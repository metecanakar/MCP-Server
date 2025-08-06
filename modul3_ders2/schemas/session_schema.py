from pydantic import BaseModel

class SessionResponse(BaseModel):
    """Yeni bir oturum oluşturulduğunda dönülecek yanıt modeli."""
    session_id: str

class UserMessage(BaseModel):
    """Kullanıcının /chat endpoint'ine göndereceği mesaj modeli."""
    message: str

class AIResponse(BaseModel):
    """/chat endpoint'inden yapay zeka yanıtını içeren model."""
    response: str