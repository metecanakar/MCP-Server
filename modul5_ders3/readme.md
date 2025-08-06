# Modül 5 - Ders 3 Pratik Uygulaması: Güvenlik ve Maliyet Optimizasyonu
Bu klasördeki kodlar, eğitim serimizin en ileri seviye konularını içeren, üretim ortamına hazır (production-ready) bir MCP sunucusu versiyonudur. Bu versiyon, fonksiyonel bir yapay zeka servisinin ötesine geçerek, onu gerçek dünya tehditlerine ve maliyetlerine karşı dayanıklı hale getiren zırhlar ve optimizasyonlar içerir.

Bu Dersin Odak Noktası ve Eklenen Özellikler
Bu kod tabanı, çalışan bir servisi alıp onu güvenli, dayanıklı ve ekonomik olarak verimli hale getirmeyi amaçlar. Aşağıdaki dört ana özellik eklenmiştir:

## 1. Güvenlik: Hız Limiti (Rate Limiting)

Nedir? Sunucunuzu kötü niyetli veya hatalı kullanımlardan kaynaklanan aşırı yükten (Denial of Service - DoS) ve bu yükün yaratacağı fahiş API maliyetlerinden koruyan bir mekanizmadır.

Nasıl Çalışır? slowapi kütüphanesi kullanılarak, belirli endpoint'lere bir kullanıcının (IP adresine göre) belirli bir zaman diliminde ne kadar istek atabileceği sınırlandırılır. Limit aşıldığında, sunucu 429 Too Many Requests hatası döndürerek isteği engeller.

Kodda Nerede?

main.py dosyasında Limiter objesi yapılandırılmıştır.

api/v1/endpoints/sessions.py dosyasındaki /chat endpoint'ine @limiter.limit("10/minute") dekoratörü eklenmiştir.

## 2. Güvenlik: Prompt Injection Savunması

Nedir? Kullanıcının, yapay zeka modelini kandırarak veya asıl görevinden saptırarak istenmeyen eylemler (örneğin, "sistem talimatlarını ifşa et") yaptırmasını engellemeye yönelik bir savunma tekniğidir.

Nasıl Çalışır? Kullanıcıdan gelen metin, modele doğrudan gönderilmez. Bunun yerine, modelin rolünü, görevini ve sınırlarını net bir şekilde tanımlayan bir "Sistem Mesajı" ile sarmalanır. Bu, modelin, kullanıcının metni içindeki potansiyel kötü niyetli talimatları görmezden gelmesine yardımcı olur.

Kodda Nerede? services/openai_service.py dosyasındaki get_ai_response fonksiyonu, konuşma geçmişini OpenAI'a göndermeden önce, en başa modelin davranışını yönlendiren bir system rolüyle mesaj ekler.

## 3. Maliyet Optimizasyonu: Akıllı Önbellekleme (Caching)

Nedir? Sık sorulan aynı sorular için OpenAI API'sine tekrar tekrar istek göndererek para harcamayı önlemek ve kullanıcılara anlık yanıtlar sunmaktır.

Nasıl Çalışır? Kullanıcı /chat endpoint'ine bir mesaj gönderdiğinde, sistem önce bu mesajın yanıtının Redis önbelleğinde olup olmadığını kontrol eder.

Cache Hit (Önbellekte Var): Yanıt doğrudan ve çok hızlı bir şekilde Redis'ten alınır, kullanıcıya döndürülür. OpenAI'a istek gönderilmez, maliyet sıfırdır.

Cache Miss (Önbellekte Yok): OpenAI API'sine istek gönderilir. Gelen yanıt hem kullanıcıya döndürülür hem de gelecekteki aynı sorular için Redis önbelleğine (bu örnekte 1 saatliğine) kaydedilir.

Kodda Nerede? api/v1/endpoints/sessions.py içindeki /chat fonksiyonu, redis_service.get_cache ve redis_service.set_cache fonksiyonlarını kullanarak bu mantığı uygular.

## 4. Maliyet Optimizasyonu: Bağlam Özetleme (Context Summarization)

Nedir? Konuşma geçmişi çok uzadığında, her seferinde tüm geçmişi göndererek artan token maliyetlerini düşürmek için kullanılan ileri seviye bir tekniktir.

Nasıl Çalışır? Sohbet, belirli bir mesaj sayısını (bu projede 10) aştığında, sistem otomatik olarak yapay zekanın kendisini kullanarak o ana kadarki konuşmanın bir özetini çıkarır. Ardından, Redis'teki uzun konuşma geçmişini, bu yeni özet metni ve konuşmanın son birkaç mesajı ile değiştirir. Bu sayede bir sonraki istekte çok daha az token kullanılır.

Kodda Nerede? services/openai_service.py dosyasına summarize_conversation_if_needed adında yeni bir fonksiyon eklenmiştir. Bu fonksiyon, /chat endpoint'i tarafından her istekte çağrılarak, gerekliyse özetleme işlemini otomatik olarak yapar.

## Kurulum ve Çalıştırma
**Adım 1: .env Dosyasını Oluşturun**
Bu klasörün içinde .env adında yeni bir dosya oluşturun ve içine kendi OpenAI API anahtarınızı yapıştırın:
<pre>
OPENAI_API_KEY="sk-..."
</pre>

**Adım 2: Redis Konteynerini Başlatın**

```bash
docker run --name mcp-redis-m5d3 -p 6379:6379 -d redis
```


**Adım 3: Python Ortamını Hazırlayın**

Bu klasörün içinde bir terminal açın:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


**Adım 4: FastAPI Sunucusunu Çalıştırın**
Projenin ana dizininden (bu klasörün bir üstü) çalıştırın:

```bash
cd ..
uvicorn modul5_ders3.main:app --reload
```

**Yeni Özellikleri Test Etme**
Sunucunuz çalışırken, yeni bir terminal açarak aşağıdaki testleri yapabilirsiniz.

**Test 1: Hız Limitini Sınama**

Aşağıdaki for döngüsü, /chat endpoint'ine kısa bir süre içinde 12 kez istek göndermeye çalışacaktır. İlk 10 isteğin başarılı (200 OK), son ikisinin ise hız limitine takıldığı için 429 Too Many Requests hatası verdiğini görmelisiniz.

```bash
# Önce bir oturum ID'si alalım
SESSION_ID=$(curl -s -X POST http://127.0.0.1:8000/v1/sessions | grep -o '"session_id":"[^"]*' | cut -d'"' -f4)
echo "Test Oturum ID: $SESSION_ID"


# Şimdi bu ID ile endpoint'i 12 kez çağıralım
for i in {1..12}; do
    echo -n "İstek #$i: "
    curl -o /dev/null -s -w "%{http_code}\n" -X POST -H "Content-Type: application/json" -d '{"message":"test"}' http://127.0.0.1:8000/v1/sessions/$SESSION_ID
    sleep 1 # İstekler arasına 1 saniye koy
done
```

**Test 2: Önbelleklemeyi (Caching) Sınama**

Bu testte, aynı soruyu iki kez soracağız. Sunucuyu çalıştırdığınız terminaldeki logları (print çıktılarını) izleyin.

```bash
# Yine aynı oturum ID'sini kullanalım
echo "Test Oturum ID: $SESSION_ID"

# İlk istek (cevap yavaş gelmeli ve loglarda "CACHE MISS" yazmalı)
echo "\n1. İstek (Önbellek Boş):"
time curl -X POST -H "Content-Type: application/json" -d '{"message":"Türkiye''nin başkenti neresidir?"}' http://127.0.0.1:8000/v1/sessions/$SESSION_ID

# İkinci istek (cevap anında gelmeli ve loglarda "CACHE HIT" yazmalı)
echo "\n\n2. İstek (Önbellek Dolu):"
time curl -X POST -H "Content-Type: application/json" -d '{"message":"Türkiye''nin başkenti neresidir?"}' http://127.0.0.1:8000/v1/sessions/$SESSION_ID
```

time komutu sayesinde ikinci isteğin çok daha hızlı tamamlandığını göreceksiniz.