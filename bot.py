from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Z-API Config (mantenha suas credenciais originais)
TOKEN = 'SEU_TOKEN_ZAPI' # Substitua pelo seu token real
ID_INSTANCIA = 'SEU_ID_INSTANCIA' # Substitua pelo seu ID real
ZAPI_TEXT_URL = f'https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-text'
ZAPI_BUTTON_URL = f'https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-button-message'

# Envia texto
def enviar_texto(chat_id, texto ):
    payload = {"chatId": chat_id, "message": texto}
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(ZAPI_TEXT_URL, json=payload, headers=headers)
        response.raise_for_status() # Verifica erros HTTP
        print(f"✅ Texto enviado para {chat_id}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao enviar texto para {chat_id}: {e}")

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
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(ZAPI_BUTTON_URL, json=payload, headers=headers)
        response.raise_for_status() # Verifica erros HTTP
        print(f"✅ Botões enviados para {chat_id}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao enviar botões para {chat_id}: {e}")

# Interpreta mensagem
def interpretar(msg):
    msg = msg.lower().strip()
    if msg == "1" or "renovar" in msg:
        return "🟢 Vamos renovar seu seguro! Me diga o CPF ou a placa do veículo."
    elif msg == "2" or "cotar" in msg:
        return "📋 Vamos cotar um novo seguro! Qual o tipo? (auto, residencial, empresarial...)"
    elif msg == "3" or "assistencia" in msg or "assistência" in msg:
        return "🛠️ Assistência 24h acionada! Me diga seu endereço ou localização."
    return None

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📥 DADOS RECEBIDOS:", json.dumps(data, indent=2, ensure_ascii=False))

    # Ignora grupos e status de mensagem
    if data.get("isGroup") is True or data.get("isStatusReply") is True:
        print("🚫 Grupo ou Status Reply detectado. Ignorado.")
        return jsonify({"status": "ignorado grupo/status"}), 200

    # --- Extrai Mensagem --- 
    msg = ""
    # Verifica se é callback de botão (estrutura 
