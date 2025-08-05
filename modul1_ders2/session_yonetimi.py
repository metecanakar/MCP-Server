import uuid
from flask import Flask, request, jsonify

# Flask uygulamasını başlat
app = Flask(__name__)

# --- ÜRETİM ORTAMI İÇİN UYGUN OLMAYAN NAİF ÇÖZÜM ---
# Konuşma geçmişlerini sunucunun belleğindeki basit bir
# Python sözlüğünde (dictionary) saklıyoruz.
# UYARI: Sunucu yeniden başladığında tüm veriler kaybolur
# ve birden fazla sunucu kopyasıyla çalışamaz.
sessions = {}

# --- BÖLÜM 1: STATELESS (DURUMSUZ) YAKLAŞIM ---
# Bu, ilk başta karşılaştığımız hafızasızlık problemini gösteren koddur.
# İncelemek için aşağıdaki kodun yorum satırlarını kaldırıp,
# üstteki "NAİF ÇÖZÜM" bölümünü yorum satırı yapabilirsiniz.
#
# @app.route('/chat', methods=['POST'])
# def handle_chat_stateless():
#     data = request.json
#     user_message = data.get('message', '')
#
#     if 'adım' in user_message.lower():
#         response_message = "Üzgünüm, adınızı bilmiyorum."
#     elif 'adım' not in user_message.lower() and ('ad' in user_message.lower() or 'ismim' in user_message.lower()):
#         response_message = f"Tanıştığıma memnun oldum! Size nasıl yardımcı olabilirim?"
#     else:
#         response_message = f"Mesajınızı aldım: '{user_message}'"
#
#     return jsonify({'response': response_message})


# --- BÖLÜM 2: NAİF STATEFUL (DURUMLU) ÇÖZÜM ---

@app.route('/chat', methods=['POST'])
def start_chat_session():
    """Yeni bir sohbet oturumu başlatır."""
    session_id = f"ssn_{uuid.uuid4()}"
    sessions[session_id] = {
        "history": [],
        "user_info": {}
    }
    
    # Kullanıcının ilk mesajını işle
    data = request.json
    user_message = data.get('message', '')
    
    sessions[session_id]["history"].append({"role": "user", "content": user_message})
    
    # İsim tespiti yap
    name = _extract_name(user_message)
    if name:
        sessions[session_id]["user_info"]["name"] = name
        response_message = f"Merhaba {name}! Tanıştığıma memnun oldum."
    else:
        response_message = "Merhaba! Oturumunuz başlatıldı."

    return jsonify({
        "response": response_message,
        "session_id": session_id
    })


@app.route('/chat/<session_id>', methods=['POST'])
def continue_chat_session(session_id: str):
    """Mevcut bir sohbet oturumuna devam eder."""
    if session_id not in sessions:
        return jsonify({"error": "Session not found"}), 404

    data = request.json
    user_message = data.get('message', '')
    
    sessions[session_id]["history"].append({"role": "user", "content": user_message})

    # Hafızayı test etme sorgusu
    if "adım neydi" in user_message.lower() or "adımı hatırlıyor musun" in user_message.lower():
        user_name = sessions[session_id]["user_info"].get("name")
        if user_name:
            response_message = f"Elbette, adınız {user_name}."
        else:
            response_message = "Üzgünüm, daha önce adınızı söylediğinizi hatırlamıyorum."
    else:
        # İsim tespiti yap
        name = _extract_name(user_message)
        if name:
            sessions[session_id]["user_info"]["name"] = name
            response_message = f"Adınızı {name} olarak güncelledim."
        else:
            response_message = "Mesajınızı aldım."
            
    sessions[session_id]["history"].append({"role": "assistant", "content": response_message})
    
    return jsonify({"response": response_message})


def _extract_name(message: str) -> str | None:
    """Mesaj içinden basit bir şekilde isim çıkarmaya çalışır."""
    words = message.lower().split()
    try:
        if "adım" in words:
            name_index = words.index("adım") + 1
            if name_index < len(words):
                return words[name_index].capitalize().replace('.', '')
        if "ismim" in words:
            name_index = words.index("ismim") + 1
            if name_index < len(words):
                return words[name_index].capitalize().replace('.', '')
    except ValueError:
        return None
    return None

if __name__ == '__main__':
    app.run(debug=True)