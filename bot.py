from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Z-API Config
TOKEN = '56100423CA70A6B6503E638D'
ID_INSTANCIA = '3E23640FFCAEC0DC14473274D0A2B459'
ZAPI_TEXT_URL = f'https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-text'
ZAPI_BUTTON_URL = f'https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-button-message'

# Envia texto
def enviar_texto(chat_id, texto):
    payload = {"chatId": chat_id, "message": texto}
    requests.post(ZAPI_TEXT_URL, json=payload)

# Envia botões
def enviar_botoes(chat_id):
    payload = {
        "chatId": chat_id,
        "content": "📋 Escolha uma opção abaixo:",
        "title": "Atendimento Magma X",
        "footer": "Estamos prontos pra te atender!",
        "buttons": [
            {"id": "renovar", "text": "1️⃣ Renovar"},
            {"id": "cotar", "text": "2️⃣ Cotar novo"},
            {"id": "assistencia", "text": "3️⃣ Assistência 24h"}
        ]
    }
    requests.post(ZAPI_BUTTON_URL, json=payload)

# Interpreta mensagem
def interpretar(msg):
    msg = msg.lower().strip()
    if msg == "1" or msg == "renovar":
        return "🟢 Vamos renovar seu seguro! Me diga o CPF ou a placa do veículo."
    elif msg == "2" or msg == "cotar":
        return "📋 Vamos cotar um novo seguro! Qual o tipo? (auto, residencial, empresarial...)"
    elif msg == "3" or msg == "assistencia":
        return "🛠️ Assistência 24h acionada! Me diga seu endereço ou localização."
    return None

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📥 DADOS:", json.dumps(data, indent=2, ensure_ascii=False))

    # Ignora grupos
    if data.get("isGroup") is True:
        print("🚫 Grupo detectado. Ignorado.")
        return jsonify({"status": "ignorado grupo"}), 200

    # Extrai mensagem
    raw_msg = data.get("mensagem") or data.get("message") or ""
    if isinstance(raw_msg, dict):
        msg = raw_msg.get("body", "")
    else:
        msg = raw_msg

    msg = msg.strip().lower() if isinstance(msg, str) else ""

    # Extrai telefone/chatId
    telefone = (
        data.get('phone') or
        data.get('sender', {}).get('phone') or
        data.get('chatId') or ""
    )
    chat_id = telefone if "@c.us" in telefone else f"{telefone}@c.us" if telefone else ""

    if not msg or not chat_id:
        print("❌ ERRO: dados incompletos")
        return jsonify({"erro": "dados incompletos"}), 400

    resposta = interpretar(msg)
    if resposta:
        enviar_texto(chat_id, resposta)
    else:
        enviar_botoes(chat_id)

    return jsonify({"status": "ok"}), 200

@app.route("/status", methods=["GET"])
def status():
    return "✅ MAGMA BOT VIVO, LIGADO E RESPONDENDO", 200
