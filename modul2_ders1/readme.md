
# Modül 2 - Ders 1 Pratik Uygulaması: API Tasarımı ve Dokümantasyonu

Bu klasör, eğitim serimizin "API Tasarımı" dersinin somut çıktısını içermektedir. Bu aşamada henüz çalışan bir sunucu kodlamadık, bunun yerine sunucumuzun nasıl davranması gerektiğini tanımlayan resmi bir "sözleşme" yazdık.

Bu sözleşme, endüstri standardı olan **OpenAPI 3.0** formatında (`mcp-api.yaml` dosyası) yazılmıştır.

## İçerik

* `mcp-api.yaml`: Uygulamamızın tüm endpoint'lerini, beklenen istek ve yanıt formatlarını (veri modellerini) ve açıklamalarını içeren ana spesifikasyon dosyası.
* `index.html`: `mcp-api.yaml` dosyasını okuyup, onu şık ve interaktif bir web sayfasına dönüştüren basit bir görüntüleyici.
* `README.md`: Bu dosya.

## İnteraktif Dokümantasyonu Görüntüleme

Bu API tasarımını canlı bir web sayfasında görmek için aşağıdaki adımları izleyin. Bu, yazdığımız YAML dosyasının ne kadar güçlü olduğunu ve geliştiricilere nasıl yardımcı olduğunu görmenin en iyi yoludur.

### Yöntem 1: VS Code Live Server Eklentisi (En Kolay)

1.  Eğer kullanmıyorsanız, Visual Studio Code'a "Live Server" eklentisini kurun.
2.  VS Code'da bu `modul2_ders1` klasörünü açın.
3.  `index.html` dosyasına sağ tıklayın ve `Open with Live Server` seçeneğini seçin.
4.  Tarayıcınızda otomatik olarak interaktif API dokümantasyonu açılacaktır.

### Yöntem 2: Python'un Dahili Web Sunucusu

1.  Bir terminal açın ve `cd` komutuyla bu `modul2_ders1` klasörünün içine gelin.
2.  Aşağıdaki komutu çalıştırarak basit bir web sunucusu başlatın:
    ```bash
    # Python 3 için
    python -m http.server
    ```
3.  Tarayıcınızı açın ve `http://localhost:8000` adresine gidin. Karşınıza interaktif API dokümantasyonu çıkacaktır.

Bu dokümantasyon sayfası, FastAPI'nin daha sonra bizim için otomatik olarak üreteceği `/docs` sayfasının temelini oluşturur.

Not : Ekranın altında, terminal yanında ports geçerek açık portlara erişebilirsiniz. 

[← Ana Sayfaya Dön](../README.md)