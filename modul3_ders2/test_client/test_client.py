import requests
import json

# Sunucunuzun çalıştığı ana adresi buraya girin.
# Eğer Codespaces kullanıyorsanız, yönlendirilen (forwarded) URL'yi yapıştırın.
BASE_URL = "http://127.0.0.1:8000"
# Örnek Codespaces URL'si: "https://kullanici-adi-proje-adi-....app.github.dev"

def start_conversation():
    """Yeni bir sohbet oturumu başlatır ve sohbet döngüsünü çalıştırır."""
    session_id = None
    try:
        # 1. Adım: Yeni bir oturum başlatmak için sunucuya istek at
        print("Yeni bir sohbet oturumu başlatılıyor...")
        response = requests.post(f"{BASE_URL}/v1/sessions")

        # Sunucudan gelen yanıtı kontrol et
        if response.status_code == 200:
            session_id = response.json().get("session_id")
            if not session_id:
                print("HATA: Sunucudan geçerli bir session_id alınamadı.")
                return
            print(f"Oturum başarıyla başlatıldı. ID: {session_id}")
            print("Sohbete başlayabilirsiniz. Çıkmak için 'çıkış' yazın.")
            print("-" * 50)
        else:
            print(f"HATA: Oturum başlatılamadı. Durum Kodu: {response.status_code}")
            print(f"Yanıt: {response.text}")
            return

        # 2. Adım: Kullanıcı ile sohbet döngüsü
        chat_loop(session_id)

    except requests.exceptions.ConnectionError:
        print("\nHATA: Sunucuya bağlanılamadı.")
        print(f"Lütfen '{BASE_URL}' adresinde sunucunun çalıştığından emin olun.")
    
    finally:
        # 3. Adım: Program bittiğinde oturumu temizle
        if session_id:
            end_session(session_id)


def chat_loop(session_id: str):
    """Kullanıcıdan sürekli girdi alır ve sunucuya gönderir."""
    while True:
        try:
            user_input = input("Siz: ")
            if user_input.lower() in ["çıkış", "cikis", "quit", "exit"]:
                print("Sohbet sonlandırılıyor...")
                break

            # Kullanıcıdan alınan mesajı JSON formatında hazırla
            payload = {"message": user_input}
            
            # Sunucunun /chat endpoint'ine isteği gönder
            response = requests.post(f"{BASE_URL}/v1/sessions/{session_id}/chat", json=payload)

            if response.status_code == 200:
                ai_response = response.json().get("response")
                print(f"AI : {ai_response}")
            else:
                # Sunucudan gelen hata mesajını göster
                print(f"HATA: Sunucudan yanıt alınamadı. Durum Kodu: {response.status_code}")
                print(f"Detay: {response.text}")

        except KeyboardInterrupt:
            print("\nSohbet sonlandırılıyor...")
            break
        except Exception as e:
            print(f"Beklenmedik bir hata oluştu: {e}")
            break


def end_session(session_id: str):
    """Sunucudaki oturumu sonlandırır."""
    try:
        print("-" * 50)
        print(f"Sunucudaki {session_id} oturumu temizleniyor...")
        response = requests.delete(f"{BASE_URL}/v1/sessions/{session_id}")
        
        if response.status_code == 204:
            print("Oturum başarıyla temizlendi. Hoşça kalın!")
        else:
            print(f"UYARI: Oturum temizlenemedi. Durum Kodu: {response.status_code}")
            print(f"Detay: {response.text}")
            
    except requests.exceptions.ConnectionError:
        # Bu aşamada sunucu zaten kapanmış olabilir, bu yüzden sadece bir uyarı veriyoruz.
        print("UYARI: Oturum temizlenirken sunucuya bağlanılamadı.")


if __name__ == "__main__":
    start_conversation()
