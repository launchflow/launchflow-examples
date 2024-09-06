from flask import Flask, request
from infra import bucket

app = Flask("main")

@app.route("/", methods=["GET"])
def get_name():
    name = request.args.get("name")
    if not name:
        return "Please provide a name"
    try:
        name_bytes = bucket.download_file(f"{name}.txt")
        return name_bytes.decode("utf-8")
    except:
        return f"{name} was not found"

@app.route("/", methods=["POST"])
def post_name():
    name = request.args.get("name")
    if not name:
        return "Please provide a name"
    bucket.upload_from_string(name, f"{name}.txt")
    return "ok"
