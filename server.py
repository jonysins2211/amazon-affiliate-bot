from flask import Flask
import os
from super_bot import send_deal_messages

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Amazon Affiliate Bot is running!"

@app.route('/run-bot')
def run_bot():
    send_deal_messages()
    return "📦 Bot executed and messages sent."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
