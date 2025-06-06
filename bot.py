from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad request"}), 400

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
