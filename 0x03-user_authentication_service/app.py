#!/usr/bin/env python3
"""module constain app flask"""
from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/')
def pay_load():
    """return JSON payload"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    """main function"""
    app.run(host="0.0.0.0", port="5000")
