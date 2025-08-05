import os
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri ortam değişkeni olarak yükler
load_dotenv()

# OpenAI API anahtarını ortam değişkenlerinden okur
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("UYARI: OPENAI_API_KEY ortam değişkeni bulunamadı. Lütfen .env dosyanızı kontrol edin.")