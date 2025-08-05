# Modül 2 - Ders 2 Pratik Uygulaması: Redis ile Bağlantı Testi

Bu klasördeki kodlar, eğitim serimizin "Bağlam Depolama Stratejileri" dersinin pratik uygulamasını içerir. Bu betiğin amacı, çalışan bir Redis veritabanına Python kullanarak bağlanmayı, karmaşık bir veri yapısını (Python listesi) JSON formatına çevirerek kaydetmeyi ve ardından bu veriyi geri okuyup tekrar Python listesine dönüştürmeyi göstermektir.

Bu, hafıza katmanımızı tam uygulamaya entegre etmeden önce yaptığımız bir kavram kanıtlama (proof-of-concept) testidir.

## Gereksinimler

1.  Bilgisayarınızda **Python**'ın kurulu olması.
2.  Bilgisayarınızda **Docker**'ın kurulu ve çalışır durumda olması.

## Kurulum ve Çalıştırma Adımları

**Adım 1: Redis Konteynerini Başlatın**

Uygulamanın bağlanacağı Redis veritabanını bir Docker konteyneri olarak başlatmamız gerekiyor. Bir terminal açın ve aşağıdaki komutu çalıştırın:

```bash
docker run --name mcp-redis-test -p 6379:6379 -d redis
```

**Adım 2: Test Betiğini Çalıştırın**

Artık her şey hazır. Aşağıdaki komutla Python betiğini çalıştırın:

```bash
python redis_test.py
```

**Beklenen Çıktı**

Terminalde aşağıdakine benzer bir çıktı görmelisiniz. Bu çıktı, verinin başarıyla Redis'e yazıldığını ve oradan doğru bir şekilde geri okunduğunu gösterir.

<pre>
'ssn_abc_123' için veri kaydediliyor...
Kaydedildi.

'ssn_abc_123' için veri okunuyor...
Okunan Veri:
[{'role': 'user', 'content': 'Merhaba'}, {'role': 'ai', 'content': 'Merhaba, nasıl yardımcı olabilirim?'}]
Geri okunan verinin tipi: <class 'list'>
Son mesajın içeriği: Merhaba, nasıl yardımcı olabilirim?
</pre>