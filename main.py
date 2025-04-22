
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from sourcing_agent import source_candidates

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "🟢 AI WhatsApp Agent running..."

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.form.get("Body", "").lower().strip()
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg.startswith("find"):
        role = incoming_msg.replace("find", "").strip()
        if not role:
            msg.body("❌ Please mention the role after 'Find', e.g. 'Find Java Developer'")
        else:
            msg.body(f"✅ Sourcing started for: {role}...\n🔍 Searching LinkedIn company pages…")
            result = source_candidates(role)
            msg.body(f"Here are the shortlisted candidates:\n\n{result}")
    else:
        msg.body("👋 Type 'Find [Role]' to start sourcing.\nExample: Find Java Developer")

    return str(resp)

if __name__ == "__main__":
    app.run()
