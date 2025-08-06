# MCP Sunucusu - Üretim Ortamına Hazır Versiyon

Bu proje, modern bir yapay zeka servisi için gereken tüm temel ve ileri seviye özellikleri içeren, üretime hazır bir uygulamadır. Bu doküman, projede bulunan Güvenlik ve Maliyet Optimizasyonu özelliklerini detaylı olarak açıklamaktadır.

## 1. Güvenlik Özellikleri

### 1.1. Hız Limiti (Rate Limiting)

**Amaç:** Sunucuyu kötü niyetli veya hatalı kullanımlardan kaynaklanan aşırı yükten (Denial of Service) ve yüksek maliyetlerden korumak.

**Nasıl Çalışır?** `slowapi` kütüphanesi kullanılarak, belirli endpoint'lere gelen istekler kullanıcının IP adresine göre sayılır. Belirlenen limit aşıldığında, sunucu `429 Too Many Requests` hatası döndürerek isteği engeller.

* **Uygulama:** `main.py` dosyasında `Limiter` objesi oluşturulur. `api/v1/endpoints/sessions.py` dosyasındaki `/chat` endpoint'ine `@limiter.limit("10/minute")` dekoratörü eklenmiştir. Bu, bir kullanıcının sohbet endpoint'ine dakikada en fazla 10 istek gönderebileceği anlamına gelir.

### 1.2. Prompt Injection Savunması

**Amaç:** Kullanıcının, yapay zeka modelini kandırarak veya asıl görevinden saptırarak istenmeyen eylemler yaptırmasını (örneğin, gizli talimatları ifşa etmesini istemek) engellemek.

**Nasıl Çalışır?** Kullanıcıdan gelen metin, modele doğrudan gönderilmez. Bunun yerine, modelin rolünü, görevini ve sınırlarını net bir şekilde tanımlayan bir "Sistem Mesajı" ile sarmalanır. Bu, modelin, kullanıcının metni içindeki potansiyel kötü niyetli talimatları görmezden gelmesine yardımcı olur.

* **Uygulama:** `services/openai_service.py` dosyasındaki `get_ai_response` fonksiyonu, konuşma geçmişini OpenAI'a göndermeden önce, en başa modelin davranışını yönlendiren bir `system` rolüyle mesaj ekler.

## 2. Maliyet Optimizasyonu Özellikleri

### 2.1. Akıllı Önbellekleme (Intelligent Caching)

**Amaç:** Sık sorulan aynı sorular için OpenAI API'sine tekrar tekrar istek göndererek para harcamayı önlemek ve kullanıcılara anlık yanıtlar sunmak.

**Nasıl Çalışır?** Bir kullanıcı `/chat` endpoint'ine bir mesaj gönderdiğinde, sistem önce bu mesajın yanıtının Redis önbelleğinde olup olmadığını kontrol eder.
* **Cache Hit (Önbellekte Var):** Yanıt doğrudan ve çok hızlı bir şekilde Redis'ten alınır, kullanıcıya döndürülür. OpenAI'a istek gönderilmez, maliyet sıfırdır.
* **Cache Miss (Önbellekte Yok):** OpenAI API'sine istek gönderilir. Gelen yanıt hem kullanıcıya döndürülür hem de gelecekteki aynı sorular için Redis önbelleğine kaydedilir.

* **Uygulama:** `api/v1/endpoints/sessions.py` içindeki `/chat` fonksiyonu, `redis_service.get_cache` ve `redis_service.set_cache` fonksiyonlarını kullanarak bu mantığı uygular. Önbellekteki veriler 1 saat sonra otomatik olarak silinir.

### 2.2. Bağlam Özetleme (Context Summarization) - YENİ EKLENDİ

**Amaç:** Konuşma geçmişi uzadıkça OpenAI'a gönderilen "token" sayısını ve dolayısıyla maliyeti ciddi oranda düşürmek.

**Nasıl Çalışır?** Sohbet, belirli bir uzunluğa (örneğin 10 mesaj) ulaştığında, sistem otomatik olarak bir özetleme işlemi tetikler.
1.  Mevcut uzun konuşma geçmişi, yapay zeka modelinin kendisine özel bir talimatla gönderilir: "Bu konuşmayı kısa ve öz bir şekilde özetle."
2.  Modelden gelen özet metni alınır.
3.  Redis'teki uzun konuşma geçmişi, bu yeni **özet metni** ve konuşmanın **son birkaç mesajı** ile değiştirilir.
4.  Böylece, bir sonraki sohbette, onlarca mesaj yerine çok daha kısa olan bu özetlenmiş bağlam gönderilir ve token maliyeti düşürülür.

* **Uygulama:** `services/openai_service.py` dosyasına `summarize_conversation_if_needed` adında yeni bir fonksiyon eklendi. Bu fonksiyon, `/chat` endpoint'i tarafından her istekte çağrılarak, gerekliyse özetleme işlemini otomatik olarak yapar ve Redis'teki geçmişi günceller.