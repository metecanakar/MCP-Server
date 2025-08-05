# Modül 2 - Ders 3 Pratik Uygulaması: FastAPI İskeleti ve Redis Entegrasyonu

Bu klasördeki kodlar, eğitim serimizin "FastAPI İskeletini Kurma ve Redis'i Entegre Etme" dersinin somut çıktısıdır. Bu, projemizin ilk çalışan, çok dosyalı ve profesyonel yapıya sahip versiyonudur.

## Amaç

Bu uygulamanın amacı, API katmanı (`api/`) ile servis katmanını (`services/`) birbirinden ayırma (Separation of Concerns) prensibini uygulamak ve tasarladığımız oturum yönetimi endpoint'lerini hayata geçirmektir.

## Yapabildikleri

* `POST /v1/sessions` endpoint'i aracılığıyla Redis üzerinde yeni sohbet oturumları oluşturabilir.
* `DELETE /v1/sessions/{session_id}` endpoint'i aracılığıyla mevcut oturumları silebilir.

## Henüz Yapamadıkları

* Bu versiyonda henüz `/chat` endpoint'i ve OpenAI entegrasyonu bulunmamaktadır. Bu bir sonraki dersin konusudur.

## Kurulum ve Çalıştırma Adımları

**Adım 1: Redis Konteynerini Başlatın**

Daha önceden bir docker konteyner'ının açık olup olmadığını kontrol edelim : 
```bash
docker ps
```

şayet açıksa 


```bash
docker stop mcp-redis-test
```

Herhangi bir aşamada bir docker silmek için : 

```bash
docker rm mcp-redis-test
```

Uygulamanın hafıza katmanı olan Redis'i bir Docker konteyneri olarak başlatın. Bir terminal açın ve aşağıdaki komutu çalıştırın:

```bash
docker run --name mcp-redis-m2d3 -p 6379:6379 -d redis
```

Not: -m2d3 eki, diğer derslerdeki konteynerlerle karışmasını önler.)

**Adım 2: FastAPI Sunucusunu Çalıştırın**

Bu modul2_ders3 klasörünün içinde yeni bir terminal açın ve aşağıdaki komutları çalıştırın:

<pre>
uvicorn main:app --reload
</pre>

Sunucu http://127.0.0.1:8000 adresinde çalışmaya başlayacaktır. --reload parametresi sayesinde kodda yaptığınız her değişiklikte sunucu kendini otomatik olarak yeniden başlatır.

## Test Adımları
Yeni bir terminal açarak aşağıdaki curl komutlarıyla çalışan API'nizi test edebilirsiniz.

**1. Yeni bir oturum oluşturun:**

```bash
SESSION_RESPONSE=$(curl -s -X POST [http://127.0.0.1:8000/v1/sessions](http://127.0.0.1:8000/v1/sessions))
SESSION_ID=$(echo $SESSION_RESPONSE | grep -o '"session_id":"[^"]*' | cut -d'"' -f4)
echo "Oturum Başarıyla Oluşturuldu. ID: $SESSION_ID"
```

**2. Oluşturulan oturumu silin:**

```bash
# Yukarıdaki komutun çıktısındaki ID'nin doğru atandığından emin olun
curl -X DELETE -o /dev/null -w "Status Code: %{http_code}\n" [http://127.0.0.1:8000/v1/sessions/$SESSION_ID](http://127.0.0.1:8000/v1/sessions/$SESSION_ID)
```

Status Code: 204 çıktısını görmelisiniz, bu işlemin başarılı olduğunu gösterir.
