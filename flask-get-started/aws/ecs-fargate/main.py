from flask import Flask, request
import launchflow as lf

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return f"Hello from {lf.project}/{lf.environment}"
