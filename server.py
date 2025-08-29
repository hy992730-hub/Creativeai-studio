from flask import Flask, request, jsonify, send_from_directory
import requests, base64, os

app = Flask(__name__, static_folder=".")

HF_API_KEY = os.getenv("HF_API_KEY")  # Railway will keep your key safe

@app.route("/")
def home():
    # Serve your frontend
    return send_from_directory(".", "index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "")

    response = requests.post(
        "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2",
        headers={"Authorization": f"Bearer {HF_API_KEY}"},
        json={"inputs": prompt},
    )

    if response.status_code != 200:
        return jsonify({"error": "API Error"}), 500

    # Return image as Base64
    return base64.b64encode(response.content).decode("utf-8")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
