from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# === CONFIGURAÇÕES DA SUA INSTÂNCIA Z-API ===
ID_INSTANCIA = "3E23640FFCAC0EDC14473274D0A2B459"
TOKEN = "56100423CA70A6B650E3638D"

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Mensagem recebida:", data)

    if 'messages' in data and len(data['messages']) > 0:
        mensagem = data['messages'][0]
        texto_recebido = mensagem.get('text', {}).get('body', '')
        numero = mensagem.get('from')

        if numero and texto_recebido:
            print(f"Texto: {texto_recebido} | Número: {numero}")

            # === MONTAR E ENVIAR A RESPOSTA ===
            url = f"https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-text"
            payload = {
                "phone": numero,
                "message": f"Olá! Sua mensagem foi recebida com sucesso: *{texto_recebido}* 🤖"
            }

            try:
                r = requests.post(url, json=payload)
                print("Resposta enviada:", r.status_code, r.text)
            except Exception as e:
                print("Erro ao enviar resposta:", e)

    return jsonify({"message": "Processado"}), 200
