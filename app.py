from flask import Flask, request, jsonify, render_template
from parser import parse_instruction

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/parse", methods=["POST"])
def parse():
    data = request.get_json(silent=True) or {}
    text = data.get("instruction", "")
    steps = parse_instruction(text)
    return jsonify({"steps": steps})


if __name__ == "__main__":
    app.run(debug=True)
