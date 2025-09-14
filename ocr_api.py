from flask import Flask, request, jsonify
import dots.ocr as dots

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({'error': 'no file uploaded'}), 400

    f = request.files['file']
    text = dots.read(f.stream)
    return jsonify({'text': text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
