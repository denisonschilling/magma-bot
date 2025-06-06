from flask import Flask, request, jsonify

app = Flask(__name__)

# Token de segurança da conta (Client-Token lá da Z-API)
EXPECTED_TOKEN = "F9eddb1f0692041b9abc8e8ec7f622657S"

@app.route("/", methods=["POST"])
def webhook():
    token = request.headers.get("client-token")
    if token != EXPECTED_TOKEN:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad request"}), 400

    # Verifica se é mensagem recebida
    message_data = data.get("message", {})
    if message_data:
        phone = message_data.get("phone", "")
        text = message_data.get("text", "").lower()

        if "oi" in text:
            return jsonify({
                "phone": phone,
                "message": "Olá! Aqui é o Magma Bot. Como posso te ajudar hoje?"
            })

    return jsonify({"message": "Recebido com sucesso"}), 200
