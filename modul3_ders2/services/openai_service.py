import os, requests, json
from typing import List, Dict, Optional

OLLAMA_URL  = os.getenv("OLLAMA_API_URL", "http://127.0.0.1:11434")
CHAT_EP     = f"{OLLAMA_URL}/api/chat"
TAGS_EP     = f"{OLLAMA_URL}/api/tags"
SHOW_EP     = f"{OLLAMA_URL}/api/show"

# Kendi istediğiniz öncelik sırası; /api/tags ile doğrulanacak
MODEL_CANDIDATES = [
    os.getenv("OLLAMA_MODEL", "tinyllama:latest"),
    "tinyllama:latest", "tinyllama"
]

# İstenen üst sınırlar (sunucuya göre kısılacak)
DESIRED_NUM_CTX     = int(os.getenv("DESIRED_NUM_CTX", "2048"))
DESIRED_NUM_PREDICT = int(os.getenv("DESIRED_NUM_PREDICT", "256"))
NUM_THREAD          = int(os.getenv("OLLAMA_NUM_THREADS", "0"))  # 0 → Ollama karar verir

def _pick_model() -> str:
    r = requests.get(TAGS_EP, timeout=5)
    r.raise_for_status()
    existing = {m["model"] for m in r.json().get("models", [])}
    for m in MODEL_CANDIDATES:
        if m in existing:
            return m
    raise RuntimeError(f"Uygun model etiketi bulunamadı. Mevcut: {sorted(existing)}")

def _get_ctx_train(model: str) -> int:
    r = requests.post(SHOW_EP, json={"name": model}, timeout=10)
    r.raise_for_status()
    details = r.json().get("details", {})
    # Ollama SHOW çıktısında doğrudan n_ctx_train olmayabilir; ama metadata’da varsa yakalar.
    # Çoğu TinyLlama gguf'unda 2048. Güvenli varsayılan:
    return int(details.get("context_length") or 2048)

def _warmup(model: str, num_ctx: int) -> None:
    try:
        # generate ile mini ısınma (chat yerine)
        payload = {
            "model": model,
            "prompt": "ping",
            "stream": False,
            "options": {"num_ctx": max(512, min(num_ctx, 1024)), "num_predict": 8}
        }
        requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=20).raise_for_status()
    except Exception:
        pass

def get_ai_response(history: List[Dict[str, str]]) -> Optional[str]:
    """
    history: [{"role":"user","content":"..."}, {"role":"assistant","content":"..."}]
    """
    try:
        model = _pick_model()
        ctx_train = _get_ctx_train(model)  # TinyLlama → 2048
        num_ctx = min(DESIRED_NUM_CTX, ctx_train)  # 4096 isterseniz bile 2048’e kısar
    except Exception as e:
        print(f"Model/ctx tespiti hatası: {e}")
        return None

    # Sistem mesajını kısa tutun (TinyLlama bağlamı küçük)
    system_msg = {"role": "system", "content": "You are a helpful assistant."}
    messages = [system_msg] + history

    # İlk çağrıdan önce sıcak başlatma (runner yükte kalsın)
    _warmup(model, num_ctx)

    options = {"num_ctx": num_ctx, "num_predict": DESIRED_NUM_PREDICT}
    if NUM_THREAD > 0:
        options["num_thread"] = NUM_THREAD

    payload = {"model": model, "messages": messages, "stream": False, "options": options}

    try:
        r = requests.post(CHAT_EP, json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        return data.get("message", {}).get("content")
    except Exception as e:
        # Hata durumunda kısaltılmış geçmiş ve daha küçük num_predict ile bir deneme daha
        print(f"Ollama /api/chat hatası: {e} – küçültüp tekrar deniyorum...")
        short = []
        total = 0
        for m in reversed(messages):
            c = len(m.get("content",""))
            if total + c > 2000:  # kaba sınır
                break
            short.append(m); total += c
        short = list(reversed(short))
        payload["messages"] = short
        payload["options"]["num_predict"] = min(128, DESIRED_NUM_PREDICT)
        try:
            r2 = requests.post(CHAT_EP, json=payload, timeout=120)
            r2.raise_for_status()
            return r2.json().get("message", {}).get("content")
        except Exception as e2:
            print(f"Ollama ikinci deneme de başarısız: {e2}")
            return None
