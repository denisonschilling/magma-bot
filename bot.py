from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TOKEN = 'SEU_TOKEN_AQUI'
ID_INSTANCIA = 'SUA_INSTANCIA_ID_AQUI'

@app.route('/', methods=['POST'])
def receber_msg():
    dados = request.get_json()
    if dados and 'message' in dados:
        msg = dados['message'].strip()
        telefone = dados['phone']
        
        resposta = interpretar_resposta(msg)
        enviar_resposta(telefone, resposta)
    
    return jsonify({'status': 'ok'})

def interpretar_resposta(msg):
    if msg == "1":
        return "🔁 Ok! Vamos renovar seu seguro. Me diga seu CPF."
    elif msg == "2":
        return "📄 Certo! Vamos cotar um novo seguro. Me diga o tipo: auto, residencial, etc."
    elif msg == "3":
        return "🚨 Assistência 24h? Já estou encaminhando. Me diga seu endereço ou localização."
    else:
        return "Olá! Responda com:\n1️⃣ Renovar\n2️⃣ Cotar\n3️⃣ Assistência"

def enviar_resposta(telefone, texto):
    url = f"https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-text"
    payload = {
        "phone": telefone,
        "message": texto
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    pass  # Render vai cuidar disso
