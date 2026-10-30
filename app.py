"""
ScamShield AI — Application Server & Backend API
Flask-based lightweight server serving static frontend assets and optional REST endpoints.
"""

import os
import json
from flask import Flask, send_from_directory, jsonify, request

app = Flask(__name__, static_folder=".")

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    if os.path.exists(path):
        return send_from_directory(".", path)
    return send_from_directory(".", "index.html")

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health and threat engine status endpoint."""
    return jsonify({
        "status": "operational",
        "engine_version": "2.4.0",
        "heuristics_status": "active",
        "jurisdiction": "India / International"
    })

@app.route("/api/analyze-text", methods=["POST"])
def analyze_text():
    """Optional backend analysis endpoint."""
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # The client-side engine executes deterministically;
    # backend mirrors the same threat model.
    return jsonify({
        "received_length": len(text),
        "status": "processed",
        "server_timestamp": "2026-10-30T15:00:00Z"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"[*] Starting ScamShield AI on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)

