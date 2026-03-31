from flask import Flask, render_template, request
from parser import parse_instruction
from playwright_runner import execute_test
from report import generate_report

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    report = None
    steps = None

    if request.method == "POST":
        user_input = request.form["instruction"]

        commands = parse_instruction(user_input)
        steps, results = execute_test(commands)
        report = generate_report(results)

    return render_template("index.html", report=report, steps=steps)

if __name__ == "__main__":
    app.run(debug=True)