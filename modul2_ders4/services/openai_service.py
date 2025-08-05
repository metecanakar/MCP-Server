import openai
from core.config import OPENAI_API_KEY

# API anahtarını modül yüklendiğinde ayarla
openai.api_key = OPENAI_API_KEY

def get_ai_response(history: list) -> str | None:
    """Konuşma geçmişini alarak OpenAI'dan bir yanıt ister."""
    # Prompt Injection'a karşı temel bir savunma katmanı olarak sistem mesajı
    system_prompt = {
        "role": "system",
        "content": "You are a helpful and friendly assistant."
    }
    
    messages_to_send = [system_prompt] + history

    try:
        if not openai.api_key:
            raise ValueError("OpenAI API anahtarı ayarlanmamış.")

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_to_send
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API ile iletişimde hata oluştu: {e}")
        return None