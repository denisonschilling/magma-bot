from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# ===== CONFIGURAÇÕES =====
TOKEN = '56100423CA70A6B6503E638D'
ID_INSTANCIA = '3E23640FFCAEC0DC14473274D0A2B459'
ZAPI_TEXT_URL = f'https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-text'
ZAPI_BUTTON_URL = f'https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-button-message'

# ===== FUNÇÕES DE ENVIO =====
def enviar_texto(chat_id, texto):
    payload = {"chatId": chat_id, "message": texto}
    print(f"➡️ Enviando texto para {chat_id}: {texto}")
    try:
        r = requests.post(ZAPI_TEXT_URL, json=payload)
        print("🔵 RESPOSTA ENVIO:", r.status_code, r.text)
    except Exception as e:
        print("❌ Falha no envio de texto:", e)

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
    print(f"➡️ Enviando botões para {chat_id}")
    try:
        r = requests.post(ZAPI_BUTTON_URL, json=payload)
        print("🔵 RESPOSTA BOTÕES:", r.status_code, r.text)
    except Exception as e:
        print("❌ Falha no envio de botões:", e)

# ===== LÓGICA DE INTERPRETAÇÃO =====
def interpretar(msg):
    msg = msg.lower().strip()
    if msg == "1" or msg == "renovar":
        return "🟢 Vamos renovar seu seguro! Me diga o CPF ou a placa do veículo."
    elif msg == "2" or msg == "cotar":
        return "📋 Vamos cotar um novo seguro! Qual o tipo? (auto, residencial, empresarial...)"
    elif msg == "3" or msg == "assistencia":
        return "🛠️ Assistência 24h acionada! Me diga seu endereço ou localização."
    return None

# ===== EXTRAÇÃO SEGURA DOS DADOS =====
def extrair_mensagem(data):
    # Tenta pegar mensagem nos jeitos mais comuns
    try:
        # Exemplo do seu JSON: "text": {"mensagem": "1"}
        if isinstance(data.get("text"), dict):
            if "mensagem" in data["text"]:
                return data["text"]["mensagem"]
            if "body" in data["text"]:
                return data["text"]["body"]
        # Mensagem direta
        if isinstance(data.get("mensagem"), str):
            return data["mensagem"]
        if isinstance(data.get("message"), str):
            return data["message"]
        if isinstance(data.get("text"), str):
            return data["text"]
    except Exception as e:
        print("❌ Falha ao extrair mensagem:", e)
    return ""

def extrair_telefone(data):
    # Usa todos os campos possíveis, sempre responde pra quem enviou
    telefone = (
        data.get("phone") or
        data.get("telefone") or
        (data.get("sender") or {}).get("phone") or
        data.get("chatId") or ""
    )
    # Remove sufixo "-grupo" se vier em grupos
    telefone = str(telefone).replace("-grupo", "")
    chat_id = telefone if "@c.us" in telefone else f"{telefone}@c.us" if telefone else ""
    return chat_id

# ===== ROTA PRINCIPAL =====
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📥 JSON RECEBIDO:\n", json.dumps(data, indent=2, ensure_ascii=False))

    # Ignora grupos de qualquer forma
    if data.get("isGroup") is True or (isinstance(data.get("telefone"), str) and "-grupo" in data.get("telefone")):
        print("🚫 Grupo detectado. Ignorando.")
        return jsonify({"status": "ignorado grupo"}), 200

    msg = extrair_mensagem(data)
    chat_id = extrair_telefone(data)
    print(f"💬 Mensagem extraída: {msg}")
    print(f"📱 chat_id extraído: {chat_id}")

    # Falta de dados
    if not msg or not chat_id or len(chat_id) < 10:
        print("❌ ERRO: Dados incompletos ou inválidos")
        return jsonify({"erro": "dados incompletos ou inválidos"}), 400

    resposta = interpretar(msg)
    if resposta:
        enviar_texto(chat_id, resposta)
        return jsonify({"status": "texto enviado"}), 200
    else:
        enviar_botoes(chat_id)
        return jsonify({"status": "botoes enviados"}), 200

@app.route("/status", methods=["GET"])
def status():
    return "✅ MAGMA BOT VIVO, LIGADO, RESPONDENDO E PRONTO PRA VENDER", 200
