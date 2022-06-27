from flask import Flask, jsonify

from random_receipt.receipt import generate


app = Flask(__name__)


@app.route("/api/receipt")
def generate_random_receipt():
    receipt = generate()
    return jsonify(receipt)


if __name__ == "__main__":
    app.run(debug=False)
