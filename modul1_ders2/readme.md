# Modül 1 - Ders 1 & 2 Pratik Uygulaması: Hafızasızlık Problemi

Bu klasördeki kodlar, eğitim serimizin başındaki temel bir problemi göstermek için tasarlanmıştır: HTTP'nin durumsuz (stateless) doğası ve bunun yapay zeka sohbetleri için yarattığı "hafızasızlık" sorunu.

`session_yonetimi.py` dosyası, bu problemi gösteren ve ardından global bir dictionary kullanarak çok basit (ama üretim ortamı için uygun olmayan) bir çözüm sunan minimal bir Flask uygulaması içerir.

## Kurulum ve Çalıştırma

Bu uygulamayı çalıştırmak için bilgisayarınızda Python'ın kurulu olması yeterlidir.

1.  **Terminali Açın:**
    Bu `modul1_ders2` klasörünün içinde bir terminal açın.

2.  **Sanal Ortam Oluşturun ve Aktive Edin:**
    ```bash
    # Sanal ortam oluştur
    python -m venv venv

    # Sanal ortamı aktive et (Windows için)
    # venv\Scripts\activate
    
    # Sanal ortamı aktive et (macOS/Linux için)
    source venv/bin/activate
    ```

3.  **Bağımlılıkları Kurun:**
    Gerekli olan tek kütüphane Flask'tır.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Uygulamayı Çalıştırın:**
    ```bash
    flask --app app run
    ```
    Uygulama artık `http://127.0.0.1:5000` adresinde çalışıyor olacaktır.

## Test Adımları

Yeni bir terminal açarak aşağıdaki `curl` komutlarıyla uygulamanın "hafızasını" test edebilirsiniz.

**1. Yeni bir sohbet başlatın ve adınızı söyleyin:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"message": "Merhaba, benim adım Ayşe."}' http://127.0.0.1:5000/chat
(http://127.0.0.1:5000/chat)
```

**2. Hafızasını test edin:**
ssn_... yazan yeri bir önceki adımda aldığınız session_id ile değiştirin.

```bash
curl -X POST -H "Content-Type: application/json" -d '{"message": "Benim adım neydi?"}' http://127.0.0.1:5000/chat/ssn
(http://127.0.0.1:5000/chat/ssn)_...
```

Uygulama size "Elbette, adınız Ayşe." şeklinde bir yanıt vermelidir. Bu, naif de olsa, durum bilgisinin sunucuda tutulduğunu gösterir.

