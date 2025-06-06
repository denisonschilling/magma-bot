from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# 🔐 Z-API
TOKEN = '56100423CA70A6B6503E638D'
ID_INSTANCIA = '3E23640FFCAEC0DC14473274D0A2B459'
ZAPI_URL = f'https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-button-message'

# 🤖 Envia botões interativos
def enviar_com_botoes(chat_id):
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
    print("🚀 Enviando botões para:", chat_id)
    response = requests.post(ZAPI_URL, json=payload)
    print("📨 Resposta da Z-API:", response.status_code, response.text)

# ✉️ Envia texto comum
def enviar_texto(chat_id, texto):
    url = f'https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-text'
    payload = {
        "chatId": chat_id,
        "message": texto
    }
    print("➡️ Enviando texto para:", chat_id)
    response = requests.post(url, json=payload)
    print("📨 Resposta da Z-API:", response.status_code, response.text)

# 🧠 Interpretação de mensagem
def interpretar_mensagem(msg):
    if msg == "1" or msg == "renovar":
        return "🟢 Vamos renovar seu seguro! Me diga o CPF ou a placa do veículo."
    elif msg == "2" or msg == "cotar":
        return "📋 Vamos cotar um novo seguro! Qual o tipo? (auto, residencial, empresarial...)"
    elif msg == "3" or msg == "assistencia":
        return "🛠️ Assistência 24h acionada! Me diga seu endereço ou localização."
    else:
        return None

# 💡 Nova função segura de extração
def extrair_dados(data):
    # Extrai mensagem
    msg_raw = (
        data.get('mensagem') or
        data.get('message') or
        data.get('text') or
        ""
    )
    msg = ""
    if isinstance(msg_raw, dict):
        msg = msg_raw.get("body") or ""
    elif isinstance(msg_raw, str):
        msg = msg_raw
    else:
        msg = ""

    msg = msg.strip().lower() if isinstance(msg, str) else ""

    # Extrai telefone
    telefone = (
        data.get('phone') or
        data.get('sender', {}).get('phone') or
        data.get('chatId') or ""
    )

    chat_id = telefone if "@c.us" in telefone else f"{telefone}@c.us" if telefone else ""
    return msg, chat_id

# 🚪 Rota principal
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 RECEBIDO:", json.dumps(data, indent=2, ensure_ascii=False))

    msg, chat_id = extrair_dados(data)

    if not msg or not chat_id:
        print("❌ ERRO: Dados incompletos.")
        return jsonify({"erro": "dados insuficientes"}), 400

    resposta = interpretar_mensagem(msg)

    if resposta:
        enviar_texto(chat_id, resposta)
    else:
        enviar_com_botoes(chat_id)

    return jsonify({"status": "ok"}), 200

# 🔄 Status
@app.route("/status", methods=["GET"])
def status():
    return "✅ MAGMA BOT ONLINE e sem erro!", 200
