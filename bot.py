from flask import Flask, request, jsonify

app = Flask(__name__)

# Substitua isso pelo token real da conta (client-token)
EXPECTED_TOKEN = "F9eddb1f0692041b9abc8e8ec7f622657S"

@app.route("/", methods=["POST"])
def webhook():
    token = request.headers.get("client-token")
    if token != EXPECTED_TOKEN:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    message = data.get("message", {}).get("text", "")
    phone = data.get("message", {}).get("phone", "")

    if "oi" in message.lower():
        resposta = {
            "phone": phone,
            "message": "Olá! Aqui é o Magma Bot. Como posso te ajudar hoje?"
        }
        return jsonify(resposta)

    return jsonify({"message": "Recebido com sucesso"})
