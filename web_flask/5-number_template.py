#!/usr/bin/python3
"""simple flask script
"""
from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """returns Hello HBNB!"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def display_hbnb():
    """returns HBNB"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def display_c_text(text):
    """display “C ” followed by the value of the text variable"""
    text = text.replace("_", " ")
    return f"C {escape(text)}"


@app.route("/python/<text>", strict_slashes=False)
@app.route("/python", strict_slashes=False, defaults={"text": "is cool"})
def display_python_text(text):
    """display “Python ”, followed by the value of the text variable"""
    text = text.replace("_", " ")
    return f"Python {escape(text)}"


@app.route("/number/<int:n>", strict_slashes=False)
def display_integer(n):
    """display “n is a number” only if n is an integer"""
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def template_integer(n):
    """display a HTML page only if n is an integer"""
    return render_template("5-number.html", n=n)


if __name__ == "__main__":
    # Start the Flask development server on 0.0.0.0:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
