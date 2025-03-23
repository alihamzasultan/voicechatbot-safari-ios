from flask import Flask, render_template, request, jsonify
import whisper
import os

app = Flask(__name__)

# Load Whisper model onc
model = whisper.load_model("base")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    audio_path = "temp_audio.wav"
    audio_file.save(audio_path)

    try:
        result = model.transcribe(audio_path)
        os.remove(audio_path)  # Clean up temp file
        return jsonify({"text": result["text"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # Allows access from other devices
