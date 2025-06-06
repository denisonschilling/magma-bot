from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# 🔐 Z-API
TOKEN = '56100423CA70A6B6503E638D'
ID_INSTANCIA = '3E23640FFCAEC0DC14473274D0A2B459'
ZAPI_URL = f'https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-button-message'

# 🤖 Envia mensagem com botões interativos
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

# 🔍 Extração robusta
def extrair_dados(data):
    msg = (
        data.get('mensagem') or
        data.get('message') or
        data.get('text', {}).get('body') or
        data.get('text') or
        ""
    )
    telefone = (
        data.get('phone') or
        data.get('sender', {}).get('phone') or
        ""
    )
    chat_id = f"{telefone}@c.us" if telefone and "@c.us" not in telefone else telefone
    return msg.strip().lower(), chat_id

# 🚪 Rota principal
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📥 RECEBIDO:", json.dumps(data, indent=2, ensure_ascii=False))

    msg, chat_id = extrair_dados(data)

    if not chat_id:
        print("❌ ERRO: telefone/chat_id não encontrado.")
        return jsonify({"erro": "sem telefone"}), 400

    if not msg:
        print("❌ ERRO: mensagem vazia.")
        return jsonify({"erro": "sem mensagem"}), 400

    # Decide a resposta
    if msg == "1" or msg == "renovar":
        resposta = "🟢 Vamos renovar seu seguro! Me diga o CPF ou a placa do veículo."
    elif msg == "2" or msg == "cotar":
        resposta = "📋 Vamos cotar um novo seguro! Qual o tipo? (auto, residencial, empresarial...)"
    elif msg == "3" or msg == "assistencia":
        resposta = "🛠️ Assistência 24h acionada! Me diga seu endereço ou localização."
    else:
        enviar_com_botoes(chat_id)
        return jsonify({"status": "botões enviados"}), 200

    # Enviar resposta direta (sem botão)
    enviar_texto(chat_id, resposta)
    return jsonify({"status": "resposta enviada"}), 200

# 📨 Envio de texto simples
def enviar_texto(chat_id, texto):
    url = f"https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-text"
    payload = {
        "chatId": chat_id,
        "message": texto
    }
    response = requests.post(url, json=payload)
    print("✉️ Texto enviado:", response.status_code, response.text)

# 🔄 Status
@app.route("/status", methods=["GET"])
def status():
    return "✅ MAGMA BOT ONLINE!", 200
