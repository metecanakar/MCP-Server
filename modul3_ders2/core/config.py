import os
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri ortam değişkeni olarak yükler
load_dotenv()

# OpenAI API anahtarını ortam değişkenlerinden okur
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPEN_SOURCE_MODEL_API_KEY="ollama"
OPEN_SOURCE_MODEL_NAME="tinyllama" # <<<--- Model adını güncelledik!

if not OPENAI_API_KEY:
    # Uygulama başlarken uyarı verelim ki anahtarın eksik olduğu anlaşılsın.
    print("UYARI: OPENAI_API_KEY ortam değişkeni bulunamadı. Lütfen .env dosyanızı kontrol edin.")