# Modül 3 - Ders 3 Pratik Uygulaması: GitHub Actions ile Otomatik Dağıtım (CI/CD)

Bu klasördeki talimatlar ve yapılandırma dosyaları, eğitim serimizin "CI/CD Temelleri" dersinin pratiğidir. Bu aşamada, bir önceki derste manuel olarak yaptığımız tüm dağıtım sürecini, `git push` komutuyla tetiklenen tam otomatik bir iş akışına dönüştüreceğiz.

## Amaç

Bu dersin amacı, kodda yapılan her değişikliğin ardından manuel işlem gerektirmeden, güvenilir ve tekrarlanabilir bir şekilde uygulamanın canlıya alınmasını sağlamaktır. Bu, modern DevOps'un temel bir prensibidir.

## Ön Koşullar

1.  **Önceki Dersin Tamamlanmış Olması:** `modul3_ders2`'deki adımları başarıyla tamamlamış ve projenizi bir kere manuel olarak dağıtmış olmanız.
2.  **GitHub Deposu:** Proje kodlarınızın tamamının bir GitHub deposunda bulunması.
3.  **Google Cloud CLI (`gcloud`):** Bilgisayarınızda `gcloud`'nin kurulu ve yetkilendirilmiş olması (sadece ilk kurulum için gerekli).

## Otomatik Dağıtım (CI/CD) Kurulum Adımları

Bu kurulum tek seferliktir. Bir kere yaptıktan sonra, her `git push` işlemi dağıtımı otomatik olarak tetikleyecektir.

### BÖLÜM A: GÜVENLİ KİMLİK DOĞRULAMA KURULUMU

GitHub'ın sizin adınıza Google Cloud'a dağıtım yapabilmesi için güvenli bir kimlik oluşturmamız gerekiyor.

**Adım 1: Google Cloud'da Service Account Oluşturma**

Bir "robot kullanıcı" (Service Account) oluşturup ona gerekli izinleri vereceğiz.
*`[PROJE_ID]` yazan yeri kendi GCP Proje ID'niz ile değiştirin.*

```bash
# Proje ID'nizi bir değişkene atayın
export PROJECT_ID="[PROJE_ID]"

# Yeni bir service account oluşturun
gcloud iam service-accounts create github-actions-deployer \
  --display-name="GitHub Actions Deployer" \
  --project=$PROJECT_ID

# Gerekli rolleri (izinleri) service account'a atayın
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

```

**Adım 2: Service Account İçin JSON Anahtarı Oluşturma**

Bu robot kullanıcının kimlik kartı olan JSON anahtarını oluşturalım. Bu komut, gcp-credentials.json adında bir dosyayı bilgisayarınıza indirecektir. Bu dosyayı GİZLİ tutun ve asla GitHub'a göndermeyin!

```bash
gcloud iam service-accounts keys create gcp-credentials.json \
  --iam-account="github-actions-deployer@$PROJECT_ID.iam.gserviceaccount.com"
```


**Adım 3: Anahtarı GitHub Secrets'a Ekleme**

<ol>
<li>GitHub deponuzun ana sayfasına gidin.
<li>Settings > Secrets and variables > Actions yolunu izleyin.
<li>New repository secret butonuna tıklayın.
<li>Name: GCP_SA_KEY
<li>Value: Bilgisayarınıza inen gcp-credentials.json dosyasının tüm içeriğini kopyalayıp bu alana yapıştırın.
<li>Add secret diyerek kaydedin.
<li>Tekrar New repository secret butonuna tıklayın.
<li>Name: GCP_PROJECT_ID
<li>Value: Kendi Google Cloud Proje ID'nizi girin.
<li>Add secret diyerek kaydedin.
</ol>

# BÖLÜM B: GITHUB ACTIONS WORKFLOW'UNU ÇALIŞTIRMA

**Adım 4: Workflow Dosyasını Projeye Ekleyin**

Projenizin ana dizininde .github/workflows/ adında bir klasör yapısı oluşturun ve içine deploy.yml dosyasını ekleyin. (Bu klasördeki tüm kodlar aşağıda verilmiştir.)

**Adım 5: Kodda Bir Değişiklik Yapın ve git push Yapın**

Otomasyonu test etmek için kodda küçük bir değişiklik yapalım. Örneğin, main.py dosyasındaki hoş geldiniz mesajını güncelleyin:

<pre lang="python">
# main.py içindeki @app.get("/") fonksiyonu
def read_root():
    return {"status": "OK", "message": "Uygulamam artık otomatik dağıtılıyor! Harika!"}
Şimdi bu değişikliği git ile kaydedip GitHub'a gönderin:
</pre>


```bash
git add .
git commit -m "feat: Add CI/CD workflow for automatic deployment"
git push origin main
```

**Adım 6: Sihri İzleyin!**

GitHub deponuzda "Actions" sekmesine gidin.

Deploy to Cloud Run ad
