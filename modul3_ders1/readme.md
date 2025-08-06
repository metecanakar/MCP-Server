# Modül 3 - Ders 1 Pratik Uygulaması: Docker ile Paketleme

Bu klasördeki kodlar, eğitim serimizin "Docker ile Paketleme" dersinin somut çıktısıdır. Bu aşamada, Modül 2'de tamamladığımız tam fonksiyonel uygulamayı alıp, onu taşınabilir ve standart bir Docker konteynerine dönüştürüyoruz.

## Amaç

Bu uygulamanın amacı, "benim makinemde çalışıyordu" problemini çözmek ve uygulamamızı tüm bağımlılıklarıyla (Python versiyonu, kütüphaneler vb.) birlikte tek bir pakete hapsetmektir.

## Bu Derste Eklenen Yeni Dosyalar

* `Dockerfile`: Docker'a imajımızı nasıl inşa edeceğini anlatan tarif dosyası.
* `.dockerignore`: Docker imajına gereksiz dosyaların kopyalanmasını engelleyen liste.

## Kurulum ve Çalıştırma Adımları

**Ön Koşul:** Bilgisayarınızda **Docker Desktop**'ın kurulu ve çalışır durumda olması gerekmektedir.

**Adım 1: `.env` Dosyasını Oluşturun (Hala Gerekli!)**

Uygulamanın konteyner **içinde** çalışırken bile OpenAI API anahtarınıza ihtiyacı var.
1.  Bu `modul3_ders1` klasörünün içinde `.env` adında yeni bir dosya oluşturun.
2.  İçine, aşağıdaki formatta kendi OpenAI API anahtarınızı yapıştırın:
    ```
    OPENAI_API_KEY="sk-..."
    ```

**Adım 2: Docker İmajını İnşa Edin (`build`)**

Bir terminal açın ve `cd` komutuyla bu `modul3_ders1` klasörünün içine gelin. Ardından aşağıdaki komutla Docker imajını oluşturun:
```bash
docker build -t mcp-server:v1 .
```

* <pre>-t mcp-server:v1:</pre> Oluşturulan imaja mcp-server adını ve v1 etiketini (versiyon) verir.
* <pre>.</pre>: Dockerfile'ın bu klasörde olduğunu belirtir.

Bu işlem, Dockerfile'daki adımları takip ederek uygulamanızı ve bağımlılıklarını kuracaktır.

**Adım 3: Docker Konteynerini Çalıştırın (run)**

İmaj hazır olduğunda, aşağıdaki komutla uygulamayı bir konteyner olarak başlatın:

```bash
docker run -d --name mcp-api-container -p 8000:8000 --env-file .env mcp-server:v1
```

* -d: Konteyneri arka planda çalıştırır.
* --name mcp-api-container: Konteynere kolay hatırlanabilir bir isim verir.
* -p 8000:8000: Bilgisayarınızın 8000 portunu, konteynerin içindeki 8000 portuna bağlar.
* --env-file .env: .env dosyasındaki sırları konteynerin içine güvenli bir şekilde aktarır.

## Test Adımları

Artık uygulamanız bir konteyner içinde çalışıyor! Test etmek için yeni bir terminal açın ve curl komutlarını kullanın. Adres hala http://127.0.0.1:8000'dir çünkü portları birbirine bağladık.

```bash
# 1. Yeni bir oturum oluşturun
SESSION_RESPONSE=$(curl -s -X POST [http://127.0.0.1:8000/v1/sessions](http://127.0.0.1:8000/v1/sessions))
SESSION_ID=$(echo $SESSION_RESPONSE | grep -o '"session_id":"[^"]*' | cut -d'"' -f4)
echo "Oturum Başarıyla Oluşturuldu. ID: $SESSION_ID"

# 2. Hafızayı test edin
curl -X POST -H "Content-Type: application/json" -d '{"message": "Ben bir Docker konteynerinde miyim?"}' [http://127.0.0.1:8000/v1/sessions/$SESSION_ID](http://127.0.0.1:8000/v1/sessions/$SESSION_ID)
```



---
#### **Dosya: `Dockerfile` (Yeni)**
```bash
```dockerfile
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
Dosya: .dockerignore (Yeni)

# Sanal ortam klasörü
.venv/
venv/

# Python cache
__pycache__/
*.pyc

# Hassas ortam değişkenleri dosyası - ASLA imaja ekleme!
.env

# VSCode ayarları
.vscode/

# GitHub Actions
.github/

# Codespaces ayarları
.devcontainer/

# Git klasörü
.git/
```



Bütün uygulama kodları, modul2_ders4'teki ile aynıdır ve Docker imajının içine kopyalanacaktır