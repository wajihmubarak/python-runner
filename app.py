from flask import Flask, request, jsonify
import io
import contextlib

app = Flask(__name__)

# الصفحة الرئيسية (تشغل HTML)
@app.route('/')
def home():
    with open("index.html", encoding="utf-8") as f:
        return f.read()

# تشغيل كود بايثون
@app.route('/run', methods=['POST'])
def run_code():
    code = request.json.get("code")

    # حماية بسيطة
    forbidden = ["import os", "import sys", "open(", "__", "eval", "exec"]
    if any(x in code for x in forbidden):
        return jsonify({"output": "❌ كود غير مسموح"})

    output = io.StringIO()

    try:
        with contextlib.redirect_stdout(output):
            exec(code)

        return jsonify({"output": output.getvalue()})

    except Exception as e:
        return jsonify({"output": str(e)})

# تشغيل السيرفر
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
