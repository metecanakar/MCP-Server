# Modül 2 - Ders 4 Pratik Uygulaması: OpenAI Entegrasyonu ve Sohbet Mantığı

Bu klasördeki kodlar, eğitim serimizin "OpenAI Entegrasyonu" dersinin somut çıktısıdır. Bu, MCP sunucusunun ilk tam fonksiyonel, sohbet edebilen versiyonudur.

## Amaç

Bu uygulama, bir önceki derste kurulan FastAPI iskeletini, harici bir yapay zeka servisi (OpenAI) ile entegre eder. `/chat` endpoint'inin tam mantığını içerir ve bir konuşmanın baştan sona nasıl yönetildiğini gösterir.

## Yeni Eklenenler

* **OpenAI Entegrasyonu:** `services/openai_service.py` modülü ile AI modeline güvenli ve kontrollü çağrılar yapılır.
* **Sohbet Mantığı:** `api/v1/endpoints/sessions.py` içindeki `/chat` endpoint'i, Redis ve OpenAI servislerini bir orkestra şefi gibi yönetir.
* **Güvenlik:** Hassas API anahtarı, `.env` dosyası ile koddan ayrı tutulur.

## Kurulum ve Çalıştırma Adımları

**Adım 1: `.env` Dosyasını Oluşturun (ÇOK ÖNEMLİ!)**

Uygulamanın OpenAI ile konuşabilmesi için API anahtarınıza ihtiyacı var.
1.  Bu `modul2_ders4` klasörünün içinde `.env` adında yeni bir dosya oluşturun.
2.  İçine, aşağıdaki formatta kendi OpenAI API anahtarınızı yapıştırın:
    ```
    OPENAI_API_KEY="sk-..."
    ```

**Adım 2: Redis Konteynerini Başlatın**

Bir terminal açın ve aşağıdaki komutu çalıştırarak Redis'i başlatın:
```bash
docker run --name mcp-redis-m2d4 -p 6379:6379 -d redis
```

**Adım 3: FastAPI Sunucusunu Çalıştırın**

Aşağıdaki komutla web sunucusunu başlatın:

```bash
uvicorn main:app --reload
```

## Test Adımları
Yeni bir terminal açarak aşağıdaki curl komutlarıyla tam bir sohbet akışını test edebilirsiniz.

**1. Yeni bir oturum oluşturun:**
<pre>
SESSION_RESPONSE=$(curl -s -X POST [http://127.0.0.1:8000/v1/sessions](http://127.0.0.1:8000/v1/sessions))
SESSION_ID=$(echo $SESSION_RESPONSE | grep -o '"session_id":"[^"]*' | cut -d'"' -f4)
echo "Oturum Başarıyla Oluşturuldu. ID: $SESSION_ID"
</pre>

2. Adınızı söyleyin ve AI'nın yanıtını alın:
<pre>
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"message": "Merhaba, benim adım Zeynep."}' \
  [http://127.0.0.1:8000/v1/sessions/$SESSION_ID](http://127.0.0.1:8000/v1/sessions/$SESSION_ID)
</pre>

3. Hafızasını test edin:
<pre>
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"message": "Adımı hatırlıyor musun?"}' \
  [http://127.0.0.1:8000/v1/sessions/$SESSION_ID](http://127.0.0.1:8000/v1/sessions/$SESSION_ID)
</pre>

Tebrikler! Yapay zekanız artık sizi hatırlıyor.
<pre>
---

#### **Dosya: `.env.example`**
Kullanıcıların `.env` dosyasını nasıl oluşturacağını gösteren örnek dosya.

</pre>

## Sohbet Testi 

test amacıyla oluşturulan python kodunu çalıştırın : 

```bash
python test_client.py
```

Aşağıda örnek bir sobhet geçmişi var : 
<pre>
Yeni bir sohbet oturumu başlatılıyor...
Oturum başarıyla başlatıldı. ID: ssn_83f41b47-6b9c-4a36-ac7d-89e3684da777
Sohbete başlayabilirsiniz. Çıkmak için 'çıkış' yazın.
--------------------------------------------------
Siz: Merhaba benim adım Şadi Evren ŞEKER.
AI : Merhaba Şadi Evren ŞEKER! Size nasıl yardımcı olabilirim?
Siz: Adımı hatırlıyor musun?
AI : Evet, adınızı hatırlıyorum. Şadi Evren ŞEKER, size nasıl yardımcı olabilirim?
Siz: Harika teşekkürler. 
AI : Rica ederim! Size başka nasıl yardımcı olabilirim?
Siz: çıkış  
Sohbet sonlandırılıyor...
--------------------------------------------------
Sunucudaki ssn_83f41b47-6b9c-4a36-ac7d-89e3684da777 oturumu temizleniyor...
Oturum başarıyla temizlendi. Hoşça kalın!
</pre>

