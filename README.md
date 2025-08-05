# MCP-Server
Model Context Protocol



# İleri Seviye MCP (Model Context Protocol) Sunucusu

![GitHub Actions CI/CD](https://github.com/actions/setup-python/workflows/CI/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Bu proje, modern yapay zeka uygulamaları için geliştirilmiş, durum bilgisi tutabilen (stateful), güvenli, optimize edilmiş ve ölçeklenebilir bir aracı (gateway) sunucusudur. Kurs boyunca sıfırdan inşa edilen bu servis, basit bir sohbet botunun ötesine geçerek, production ortamı için gerekli olan profesyonel mühendislik pratiklerini içerir.

## Proje Hakkında

MCP Sunucusu, Büyük Dil Modelleri'nin (LLM) en büyük zayıflıklarından biri olan "hafızasızlığı" çözmek için tasarlanmıştır. Her kullanıcı için ayrı bir konuşma bağlamı (context) tutarak, yapay zekanın tutarlı ve kişiselleştirilmiş diyaloglar kurmasını sağlar.

Bu depo, bir fikrin nasıl adım adım profesyonel bir servise dönüştüğünün canlı bir örneğidir:
1.  **Tasarım:** RESTful API prensipleriyle bir "sözleşme" tasarlandı.
2.  **Geliştirme:** FastAPI ile asenkron bir web sunucusu, Redis ile de hızlı bir hafıza katmanı inşa edildi.
3.  **Paketleme:** Uygulama, Docker ile her yerde çalışabilen taşınabilir bir konteynere dönüştürüldü.
4.  **Dağıtım:** Tek komutla Google Cloud Run gibi sunucusuz bir platformda canlıya alındı.
5.  **Otomasyon:** GitHub Actions ile CI/CD boru hattı kurularak, her kod değişikliğinin otomatik olarak dağıtılması sağlandı.
6.  **Yönetim:** Gözlemlenebilirlik, güvenlik ve maliyet optimizasyonu gibi üretim ortamı için kritik olan yetenekler eklendi.

## Öne Çıkan Özellikler

* **Durum Bilgisi Tutan Konuşmalar:** Redis kullanarak her kullanıcı için ayrı ve kalıcı sohbet geçmişi yönetimi.
* **Modern API:** FastAPI ile geliştirilmiş, yüksek performanslı ve asenkron RESTful API.
* **Otomatik Dokümantasyon:** Koddan otomatik olarak oluşturulan interaktif Swagger/OpenAPI dokümantasyonu.
* **Konteynerleştirilmiş:** Docker ile paketlenmiş, taşınabilir ve tutarlı bir dağıtım imkanı.
* **Sunucusuz (Serverless) Uyumlu:** Google Cloud Run gibi platformlarda kolayca çalıştırılabilir.
* **CI/CD Otomasyonu:** GitHub Actions ile `git push` sonrası otomatik dağıtım.
* **Güvenlik Önlemleri:** Hız limiti (Rate Limiting) ve temel Prompt Injection savunmaları.
* **Maliyet Optimizasyonu:** Akıllı önbellekleme (caching) ile gereksiz API çağrılarının önlenmesi.
* **Gözlemlenebilirlik:** Google Cloud Logging ile entegre, yapılandırılmış (structured) loglama.
* **Codespaces Entegrasyonu:** Tek tıkla, bulut tabanlı, tam yapılandırılmış bir geliştirme ortamı.

## Mimari

Uygulama, bir aracı (Gateway) mimarisi üzerine kurulmuştur. Kullanıcıdan gelen istekleri karşılar, Redis'ten ilgili hafıza/bağlam bilgisini alır, bu bilgilerle zenginleştirilmiş bir prompt oluşturarak OpenAI gibi bir LLM servisine gönderir ve aldığı yanıtı tekrar hafızayı güncelleyerek kullanıcıya döner.


# Modül ve Derslere Hızlı Erişim

* [Modül 1 Ders 1](/modul1_ders1/readme.md) : Stateless API
* [Modül 1 Ders 2](/modul1_ders2/readme.md) : Gateway Mimarisi
* [Modül 2 Ders 1](/modul2_ders1/readme.md) : RESTful Prensipleri
* [Modül 2 Ders 2](/modul2_ders2/readme.md) : REDIS Giriş
* [Modül 2 Ders 3](/modul2_ders3/readme.md) : Bağlam Depolama, FastAPI ve REDIS, Stateful
* [Modül 2 Ders 4](/modul2_ders4/readme.md) : LLM Bağlantısı ve /chat
* [Modül 3 Ders 1](/modul3_ders1/readme.md) : Docker Yapısını Hayata Geçirmek





## Başlarken: GitHub Codespaces ile Kurulum ve Çalıştırma

Bu proje, yerel kuruluma ihtiyaç duymadan, tamamen GitHub Codespaces üzerinde çalışmak üzere tasarlanmıştır.

### Ön Koşullar

1.  **GitHub Hesabı:** Codespaces özelliğini kullanabilen bir GitHub hesabı.
2.  **OpenAI API Anahtarı:** OpenAI'dan alınmış, `sk-...` ile başlayan geçerli bir API anahtarı.

### Adım Adım Kurulum

**1. Bu Depoyu Kendi Hesabınıza Alın**

   Bu projeyi kendi hesabınızda denemek için sağ üst köşedeki **`Fork`** butonuna tıklayarak kendi hesabınıza bir kopyasını oluşturun.

**2. OpenAI API Anahtarınızı Yapılandırın**

   API anahtarınız, projenin en önemli sırrıdır ve güvenli bir şekilde saklanmalıdır.
   - Fork'ladığınız deponuzun ana sayfasına gidin.
   - `Settings` > `Secrets and variables` > `Codespaces` yolunu izleyin.
   - `New repository secret` butonuna tıklayın.
   - **Name:** `OPENAI_API_KEY`
   - **Value:** `sk-...` ile başlayan kendi OpenAI API anahtarınızı yapıştırın.
   - `Add secret` diyerek kaydedin.

**3. Codespace'i Başlatın**

   - Deponuzun ana sayfasına dönün.
   - Yeşil renkli `<> Code` butonuna tıklayın.
   - `Codespaces` sekmesine geçin.
   - `Create codespace on main` butonuna tıklayın.

**4. Arkanıza Yaslanın ve Bekleyin**

   GitHub, sizin için bulutta bir geliştirme ortamı hazırlayacaktır. `.devcontainer` yapılandırması sayesinde tüm kurulumlar (Python kütüphaneleri dahil) otomatik olarak yapılacaktır.

**5. Servisleri Başlatın**
   
   Ortam hazır olduğunda, VS Code içindeki **TERMINAL**'i açın ve aşağıdaki kod hücrelerini sırayla çalıştırın.


## Proje Dosya Yapısı
Projenin tamamlanmış hali aşağıdaki dosya yapısına sahiptir:
<pre>
├── .devcontainer/
│   ├── devcontainer.json
│   └── post-create.sh
├── .github/workflows/
│   └── deploy.yml
├── api/
│   └── v1/
│       └── endpoints/
│           └── sessions.py
├── core/
│   └── config.py
├── schemas/
│   └── session_schema.py
├── services/
│   ├── openai_service.py
│   └── redis_service.py
├── .dockerignore
├── Dockerfile
├── main.py
├── README.md
└── requirements.txt

</pre>

<pre>
# Önce Redis veritabanını bir Docker konteyneri olarak başlatalım.
# Bu komut arka planda çalışmaya devam edecektir.
echo "Redis konteyneri başlatılıyor..."
docker run --name mcp-redis -p 6379:6379 -d redis
echo "Redis başlatıldı. 'docker ps' komutuyla kontrol edebilirsiniz."
</pre>

<pre>
# Şimdi FastAPI uygulamamızı uvicorn ile başlatalım.
# Bu komut çalışmaya devam edecek ve terminali meşgul edecektir.
# Uygulamanın loglarını bu terminalden takip edebilirsiniz.
echo "FastAPI sunucusu başlatılıyor... ([http://127.0.0.1:8000](http://127.0.0.1:8000))"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
</pre>


**6. Uygulamanıza Erişin ve Test Edin**

   Yukarıdaki `uvicorn` komutu çalıştığında, Codespaces sağ alt köşede **8000 portunun** kullanılabilir olduğuna dair bir bildirim gösterecektir.
   - VS Code'da `PORTS` sekmesine gidin (Genellikle Terminal'in yanındadır).
   - "8000" portu için listelenen "Forwarded Address" (Yönlendirilen Adres) URL'sini bulun. Bu URL, `https://...app.github.dev` şeklinde olacaktır.
   - Artık uygulamanız bu genel URL üzerinden erişilebilir durumda!


## API Kullanımı ve Test

Aşağıdaki kod hücrelerini çalıştırarak canlıdaki servisinizi test edebilirsiniz. Önce bir üstteki hücreden yönlendirilen URL'nizi alıp aşağıdaki `URL` değişkenine atamanız gerekmektedir.

<pre lang="python">
# Lütfen YONLENDIRILEN_URL kısmını kendi Codespace URL'niz ile değiştirin.
URL="[https://kullanici-adi-proje-adi-....app.github.dev](https://kullanici-adi-proje-adi-....app.github.dev)"

# Yeni bir oturum başlatalım ve dönen ID'yi bir değişkene atayalım
echo "Yeni oturum başlatılıyor..."
SESSION_RESPONSE=$(curl -s -X POST $URL/v1/sessions)
export SESSION_ID=$(echo $SESSION_RESPONSE | grep -o '"session_id":"[^"]*' | cut -d'"' -f4)

if [ -z "$SESSION_ID" ]; then
    echo "Hata: Oturum ID'si alınamadı!"
    echo "Dönen yanıt: $SESSION_RESPONSE"
else
    echo "Oturum Başlatıldı. ID: $SESSION_ID"
fi
</pre>