# Modül 3 - Ders 2 Pratik Uygulaması: Açık Kaynak Modellerle Entegrasyon

Bu klasördeki kodlar, eğitim serimizin "Açık Kaynak Modellerle Entegrasyon" dersinin somut çıktısıdır. Bu derste, uygulamamızın beynini OpenAI'nin bulut servislerinden, kendi bilgisayarımızda çalışan güçlü bir açık kaynak modele (örneğin Llama 3) çeviriyoruz.

## Amaç

Bu dersin amacı, `openai` Python kütüphanesinin esnekliğini kullanarak, uygulamamızı herhangi bir OpenAI uyumlu API sunucusuna bağlayabilme yetkinliği kazanmaktır. Bunu, **Ollama** adında, açık kaynak modelleri yerel olarak çalıştırmayı son derece kolaylaştıran bir araç ile test edeceğiz.

## BÖLÜM A: YEREL YAPAY ZEKA SUNUCUSUNU KURMA (OLLAMA)

**Adım 1: Ollama'yı Kurun**

1.  [ollama.com](https://ollama.com/) adresine gidin ve işletim sisteminize uygun olan versiyonu indirip kurun.

Aşağıdaki komut, Ollama'nın kurulum betiğini indirip çalıştırarak komut satırı aracını Codespace ortamınıza kuracaktır.
```bash
curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
```

**Adım 2: Ollama'yı çalıştırın (sunucu tarafı):**

```bash
ollama serve
```

**Adım 3: Bir Model İndirin**

Kurulum bittikten sonra, bir terminal açın ve küçük ama yetenekli bir model olan `llama3`'ü indirmek için aşağıdaki komutu çalıştırın:
```bash
ollama pull llama3
```

**Adım 4: Küçük Bir Modeli İndirin**

Codespaces'in sınırlı kaynakları nedeniyle, llama3 yerine çok daha küçük ve CPU üzerinde daha hızlı çalışabilen tinyllama modelini indireceğiz.

```bash
ollama pull tinyllama
```


# BÖLÜM B: UYGULAMAMIZI YEREL SUNUCUYA BAĞLAMA

**Adım 5: .env Dosyasını Güncelleyin**

Bu klasördeki .env.example dosyasını .env olarak kopyalayın. İçeriğini, yerel sunucumuzun bilgilerini ve yeni model adını gösterecek şekilde aşağıdaki gibi güncelleyin.

<pre>
# .env dosyasının içeriği
OPENAI_API_KEY="sk-..."

# Yerel/Açık Kaynak Model Ayarları
OPEN_SOURCE_MODEL_BASE_URL="http://localhost:11434/v1"
OPEN_SOURCE_MODEL_API_KEY="ollama"
OPEN_SOURCE_MODEL_NAME="tinyllama" # <<<--- Model adını güncelledik!

</pre>


**Adım 6: Python Ortamını Hazırlayın**

Codespaces, .devcontainer yapılandırması sayesinde Python bağımlılıklarını genellikle otomatik kurar. Ancak emin olmak için aşağıdaki komutu çalıştırabilirsiniz:

```bash
pip install -r requirements.txt
```

**Adım 7: Yerel Model Servisini Test Edin**

Aşağıdaki komutla, sadece yerel modelle konuşan test betiğini çalıştırın. Unutmayın, yanıtın gelmesi yavaş olabilir!

```bash
python test_local_model_service.py
```

**Beklenen Çıktı**

Terminalde, Codespace'inizde çalışan tinyllama modelinden gelen bir yanıt görmelisiniz.

Yerel model servisinden (Ollama) yanıt bekleniyor...
AI Yanıtı: Hello! I am a large language model, trained by Google.
Bu, artık uygulamamızın beynini kendi kontrolümüzdeki bir modele başarıyla bağladığımız anlamına gelir.

<pre>
---
### **Güncellenmiş Dosyalar**

Bu senaryo için `modul3_ders2` klasörünüzdeki diğer tüm dosyalar (`main.py`, `services/`, `core/` vb.) daha önce verdiğim gibidir. Sadece `.env` dosyanızı yukarıdaki `README.md`'de belirtildiği gibi güncellemeniz yeterlidir.

Referans olması açısından, güncellenmesi gereken iki dosyanın içeriği aşağıdadır:

#### **Dosya: `.env.example`**
</pre>