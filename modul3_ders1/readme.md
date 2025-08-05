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