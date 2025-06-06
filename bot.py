from flask import Flask, request, jsonify
import re
import requests

# Configuration for Z-API (placeholders for instance ID and token)
ZAPI_INSTANCE_ID = "YOUR_INSTANCE_ID"
ZAPI_TOKEN = "YOUR_INSTANCE_TOKEN"
ZAPI_BASE_URL = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}"

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    """Webhook endpoint to receive and respond to WhatsApp messages via Z-API."""
    try:
        # Parse the incoming JSON data
        data = request.get_json(force=True, silent=True)
    except Exception as e:
        print(f"Error parsing incoming JSON: {e}")
        # Return a 200 response with error info (to avoid webhook retrying on error)
        return jsonify({"success": False, "error": "invalid_json"}), 200

    if not data:
        print("No data received in webhook")
        return jsonify({"success": False, "error": "no_data"}), 200

    # Extract the sender's phone number or chat ID from possible fields
    phone = None
    if "phone" in data:
        phone = data["phone"]
    elif "telefone" in data:
        phone = data["telefone"]
    elif "sender" in data and isinstance(data["sender"], dict) and "phone" in data["sender"]:
        phone = data["sender"]["phone"]
    elif "chatId" in data:
        phone = data["chatId"]

    # Determine if the message is from a group and should be ignored
    if data.get("isGroup") or (isinstance(phone, str) and ("-grupo" in phone.lower() or "@g.us" in phone)):
        print(f"Ignoring group message from {phone}")
        return jsonify({"success": True, "message": "ignored_group"}), 200

    # Normalize phone to chat_id format for individual WhatsApp chats
    digits = re.sub(r"\D", "", str(phone))  # remove any non-digit characters
    if len(digits) < 11:
        # Log a warning if the phone number seems incomplete (e.g., missing country/area code)
        print(f"Warning: phone number appears incomplete ({phone})")
    chat_id = digits + "@c.us" if digits else None

    if not chat_id:
        # If we couldn't determine a chat ID, log and respond without error
        print("No valid phone/chat ID found, cannot send reply")
        return jsonify({"success": False, "error": "no_phone"}), 200

    # Extract the message text from the various possible fields
    message_text = ""
    try:
        if "text" in data:
            text_field = data["text"]
            if isinstance(text_field, str):
                message_text = text_field
            elif isinstance(text_field, dict):
                # Check common keys in text dict
                if "mensagem" in text_field:
                    message_text = text_field["mensagem"]
                elif "body" in text_field:
                    message_text = text_field["body"]
                else:
                    # Fallback: take the first value in the dict if keys are unknown
                    message_text = next(iter(text_field.values()), "")
            else:
                # If text field is present but not a str or dict (unlikely), convert to string
                message_text = str(text_field)
        elif "mensagem" in data:
            message_text = data["mensagem"]
        elif "message" in data:
            message_text = data["message"]
    except Exception as e:
        # Log any error during message extraction and default to empty text
        print(f"Error extracting message text: {e}")
        message_text = ""

    # Ensure message_text is a clean string
    if not isinstance(message_text, str):
        message_text = str(message_text) if message_text is not None else ""
    message_text = message_text.strip()

    # Decide on the response based on the message content
    reply_text = None
    interactive = False
    if message_text == "1":
        reply_text = "Mensagem de renovação de seguro"
    elif message_text == "2":
        reply_text = "Mensagem de cotação de seguro"
    elif message_text == "3":
        reply_text = "Mensagem de assistência 24h"
    else:
        # For any other input, prepare an interactive menu with buttons
        interactive = True
        reply_text = ("Por favor, escolha uma das opções: "
                      "1-Renovação de Seguro, 2-Cotação de Seguro, 3-Assistência 24h.")

    # Log the received message and the response that will be sent
    print(f"Received from {chat_id}: '{message_text}' -> Responding: '{reply_text}'")

    # Send the response through Z-API (using appropriate endpoint)
    try:
        if interactive:
            # Prepare payload for interactive buttons (button list)
            buttons = [
                {"id": "1", "label": "Renovação de Seguro"},
                {"id": "2", "label": "Cotação de Seguro"},
                {"id": "3", "label": "Assistência 24h"}
            ]
            payload = {
                "phone": digits,  # numeric phone string without formatting
                "message": "Escolha uma opção:",  # prompt message for the buttons
                "buttonList": {"buttons": buttons}
            }
            # Call Z-API endpoint to send a message with buttons
            requests.post(f"{ZAPI_BASE_URL}/send-button-list", json=payload)
        else:
            # Prepare payload for a simple text message
            payload = {
                "phone": digits,
                "message": reply_text
            }
            # Call Z-API endpoint to send a plain text message
            requests.post(f"{ZAPI_BASE_URL}/send-text", json=payload)
    except Exception as e:
        # Log errors if the API call fails, but do not crash
        print(f"Error sending message to {chat_id}: {e}")

    # Always return a 200 OK response to acknowledge the webhook
    return jsonify({"success": True}), 200

# Example: Running the Flask app (not needed if deployed on a server)
if __name__ == "__main__":
    app.run(debug=False, port=5000)
