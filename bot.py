from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# === CONFIGURAÇÕES Z-API ===
ID_INSTANCIA = "3E23640FFCAC0EDC14473274D0A2B459"
TOKEN = "56100423CA70A6B650E3638D"
URL_ENVIO = f"https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-text"

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Mensagem recebida:", data)

    if data and 'messages' in data:
        for mensagem in data['messages']:
            texto = mensagem.get('text', {}).get('body', '')
            numero = mensagem.get('from')

            if numero and texto:
                print(f"[BOT] Texto: {texto} | De: {numero}")

                payload = {
                    "phone": numero,
                    "message": f"Olá! Recebi sua mensagem: *{texto}* 😎"
                }

                headers = {
                    "Content-Type": "application/json"
                }

                try:
                    response = requests.post(URL_ENVIO, json=payload, headers=headers)
                    print("Resposta Z-API:", response.status_code, response.text)
                except Exception as e:
                    print("Erro ao responder:", str(e))

    return jsonify({"message": "Mensagem processada"}), 200
