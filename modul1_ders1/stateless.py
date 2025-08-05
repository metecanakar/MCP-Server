# Gerekli Flask modüllerini içe aktarıyoruz
from flask import Flask, request, jsonify

# Flask uygulaması başlatılıyor
app = Flask(__name__)

# /chat adresine POST isteği gönderildiğinde çalışacak bir route tanımlanıyor
@app.route('/chat', methods=['POST'])
def handle_chat():
    # İstek (request) içerisindeki JSON verisini al
    data = request.json

    # JSON içinden 'message' adlı anahtarı al. Eğer yoksa varsayılan olarak boş string ver.
    user_message = data.get('message', '')

    # Bilgilendirici yorum:
    # Bu fonksiyon stateless olduğu için önceki konuşmaları hatırlayamaz.
    # Bu örnekte, 'adım' kelimesi mesajda geçiyorsa, adınızı hatırlayamam diyor.
    if 'adım' in user_message.lower():
        response_message = "Üzgünüm, adınızı hatırlamıyorum."
    else:
        # Kullanıcının mesajını geri dönen basit bir yanıt veriyoruz
        response_message = f"Mesajınızı aldım: '{user_message}'"

    # Yanıtı JSON formatında döndür
    return jsonify({'response': response_message})

# Eğer bu dosya doğrudan çalıştırılırsa uygulama 5000 portunda çalıştırılır
if __name__ == '__main__':
    app.run(port=5000)
