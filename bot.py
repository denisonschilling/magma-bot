from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ID_INSTANCIA = '3E23640FFCAEC0DC14473274D0A2B459'
TOKEN = '56100423CA70A6B6503E638D'
URL_BASE = f'https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}'

def enviar_texto(chat_id, texto):
    payload = {"chatId": chat_id, "message": texto}
    try:
        r = requests.post(f"{URL_BASE}/send-text", json=payload)
        print("🔵 ENVIO TEXTO:", r.status_code, r.text)
    except Exception as e:
        print("❌ Erro ao enviar texto:", e)

def enviar_botoes(chat_id):
    payload = {
        "chatId": chat_id,
        "content": "Escolha uma opção abaixo:",
        "title": "Atendimento Magma X",
        "footer": "Estamos prontos pra te atender!",
        "buttons": [
            {"id": "1", "text": "1️⃣ Renovar"},
            {"id": "2", "text": "2️⃣ Cotar novo"},
            {"id": "3", "text": "3️⃣ Assistência 24h"}
        ]
    }
    try:
        r = requests.post(f"{URL_BASE}/send-button-message", json=payload)
        print("🔵 ENVIO BOTÕES:", r.status_code, r.text)
    except Exception as e:
        print("❌ Erro ao enviar botões:", e)

def interpretar(msg):
    msg = str(msg).strip().lower()
    if msg == "1":
        return "🟢 Vamos renovar seu seguro! Me passe seu CPF ou placa."
    elif msg == "2":
        return "📋 Vamos cotar um novo seguro! Qual tipo? (auto, residencial, empresarial...)"
    elif msg == "3":
        return "🛠️ Assistência 24h acionada! Informe o endereço ou localização."
    else:
        return None

def extrair_mensagem(data):
    if isinstance(data.get("text"), dict):
        if "mensagem" in data["text"]:
            return data["text"]["mensagem"]
        if "body" in data["text"]:
            return data["text"]["body"]
        # Se tiver só um valor no dict
        if len(data["text"].values()) == 1:
            return list(data["text"].values())[0]
    if isinstance(data.get("text"), str):
        return data["text"]
    if isinstance(data.get("mensagem"), str):
        return data["mensagem"]
    if isinstance(data.get("message"), str):
        return data["message"]
    return ""

def extrair_telefone(data):
    telefone = (
        data.get("phone") or
        data.get("telefone") or
        (data.get("sender") or {}).get("phone") or
        data.get("chatId") or ""
    )
    telefone = str(telefone).replace("-grupo", "").replace("@c.us", "").strip()
    # Agora só remove espaço, mas não bloqueia mais nada
    return telefone

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("\n📥 JSON recebido:", data)

    # ---- IGNORA GRUPO ----
    if data.get("isGroup") or (isinstance(data.get("telefone"), str) and "-grupo" in data.get("telefone")):
        print("🚫 Grupo detectado, ignorado.")
        return jsonify({"status": "ignorado grupo"}), 200

    msg = extrair_mensagem(data)
    telefone = extrair_telefone(data)
    chat_id = telefone + "@c.us" if telefone else ""
    print(f"💬 Mensagem recebida: '{msg}'")
    print(f"📱 chat_id: {chat_id}")

    # Se telefone é muito curto, apenas loga e retorna ok (não tenta enviar pra Z-API)
    if len(telefone) < 12:
        print("⚠️ Telefone curto ou inválido! Não vou enviar nada porque WhatsApp não entrega para números curtos. Informe seu DDD completo no disparo.")
        return jsonify({"status": "telefone curto/ok"}), 200

    resposta = interpretar(msg)
    if resposta:
        enviar_texto(chat_id, resposta)
        print("✅ Enviado TEXTO para", chat_id)
    else:
        enviar_botoes(chat_id)
        print("✅ Enviado BOTÕES para", chat_id)

    return jsonify({"status": "ok"}), 200

@app.route("/status", methods=["GET"])
def status():
    return "MAGMA BOT RODANDO, VIVO, SEM ERRO", 200
