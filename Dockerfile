# Adım 1: Temel İmaj
# Python 3.11'in olduğu hafif bir Linux tabanlı imaj kullanıyoruz.
FROM python:3.11-slim

# Adım 2: Çalışma Dizini
# Konteyner içindeki ana klasörümüzü /app olarak ayarlıyoruz.
WORKDIR /app

# Adım 3: Bağımlılıkları Kurma (Docker Katman Önbellekleme Optimizasyonu)
# Önce sadece bağımlılık listesini kopyalayıp kuruyoruz.
# Bu sayede kodumuz değişse bile, bu katman yeniden inşa edilmez.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Adım 4: Uygulama Kodunu Kopyalama
# Geri kalan tüm proje dosyalarını kopyalıyoruz.
COPY . .

# Adım 5: Konteyner Çalıştığında Tetiklenecek Komut
# Uvicorn'u 0.0.0.0 host'u ile çalıştırarak konteyner dışından erişilebilir yapıyoruz.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]