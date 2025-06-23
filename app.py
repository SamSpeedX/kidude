from flask import Flask, jsonify
import threading
from firewall import start_monitoring
from botwatcher import start_bot_watcher
from detector import run_detection

app = Flask(__name__)

@app.route("/start", methods=["GET"])
def start_protection():
    threading.Thread(target=start_monitoring, daemon=True).start()
    threading.Thread(target=start_bot_watcher, daemon=True).start()
    return jsonify({"status": "Protection started"})

@app.route("/analyze", methods=["GET"])
def analyze_logs():
    suspicious = run_detection()
    return jsonify({"suspicious_logs": suspicious})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
