import os
from dotenv import load_dotenv

# Bu aşamada sadece .env dosyasını yüklemeye hazırlık yapıyoruz.
# OpenAI anahtarı bir sonraki derste eklenecek.
load_dotenv()

# Örnek bir konfigürasyon değişkeni
APP_TITLE = os.getenv("APP_TITLE", "MCP Sunucusu")