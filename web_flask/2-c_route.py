#!/usr/bin/python3
"""simple flask script

Returns:
    _type_: _description_
"""
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def display_hbnb():
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def display_c_text(text):
    text = text.replace("_", " ")
    return f"C {escape(text)}"


if __name__ == "__main__":
    # Start the Flask development server on 0.0.0.0:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
