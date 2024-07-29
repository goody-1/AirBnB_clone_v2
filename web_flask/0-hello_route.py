#!/usr/bin/python3
"""simple flask script

Returns:
    _type_: _description_
"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"


if __name__ == "__main__":
    # Start the Flask development server on 0.0.0.0:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
