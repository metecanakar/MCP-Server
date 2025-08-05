import redis
import json
import uuid

def run_redis_test():
    """
    Redis'e bağlanır, örnek bir konuşma geçmişini JSON olarak kaydeder
    ve ardından geri okuyarak doğruluğunu test eder.
    """
    try:
        # Adım 1: Redis sunucusuna bağlan
        # decode_responses=True, Redis'ten gelen yanıtları (byte yerine)
        # otomatik olarak UTF-8 string'e çevirir.
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        
        # Bağlantıyı test etmek için ping at
        r.ping()
        print("Redis sunucusuna başarıyla bağlanıldı.")

    except redis.exceptions.ConnectionError as e:
        print(f"HATA: Redis sunucusuna bağlanılamadı: {e}")
        print("Lütfen Docker üzerinde Redis konteynerinin çalıştığından emin olun.")
        return

    # Örnek verilerimizi oluşturalım
    session_id = f"ssn_{uuid.uuid4()}"
    conversation_history = [
        {"role": "user", "content": "Merhaba"},
        {"role": "ai", "content": "Merhaba, nasıl yardımcı olabilirim?"}
    ]

    # Adım 2: Veriyi Redis'e kaydet
    print(f"\n'{session_id}' için veri kaydediliyor...")
    try:
        # Python list/dict yapısını doğrudan saklayamayız.
        # Bu yüzden onu JSON formatında bir string'e çeviriyoruz (serialization).
        json_history = json.dumps(conversation_history)
        
        # r.set komutu ile anahtar-değer çiftini kaydediyoruz.
        r.set(session_id, json_history)
        print("Kaydedildi.")
    except Exception as e:
        print(f"HATA: Veri kaydedilirken bir sorun oluştu: {e}")
        return


    # Adım 3: Veriyi Redis'ten geri oku
    print(f"\n'{session_id}' için veri okunuyor...")
    try:
        # r.get ile anahtarımızı kullanarak değeri (JSON string'ini) alıyoruz.
        retrieved_data_str = r.get(session_id)
        
        if retrieved_data_str is None:
            print(f"HATA: '{session_id}' için veri bulunamadı.")
            return

        # Gelen JSON string'ini tekrar kullanılabilir bir Python listesine çeviriyoruz (deserialization).
        retrieved_conversation = json.loads(retrieved_data_str)
        
        print("Okunan Veri:")
        print(retrieved_conversation)
        
        # Geri dönüştürmenin başarılı olduğunu teyit edelim
        print(f"Geri okunan verinin tipi: {type(retrieved_conversation)}")
        
        # İçindeki veriye erişebildiğimizi de test edelim
        if retrieved_conversation and isinstance(retrieved_conversation, list) and len(retrieved_conversation) > 0:
            last_message = retrieved_conversation[-1].get("content", "Mesaj içeriği bulunamadı")
            print(f"Son mesajın içeriği: {last_message}")

    except Exception as e:
        print(f"HATA: Veri okunurken bir sorun oluştu: {e}")
        return

if __name__ == '__main__':
    run_redis_test()