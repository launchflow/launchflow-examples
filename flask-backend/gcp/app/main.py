import launchflow as lf
from app.infra import (
    cloud_run_service,
    cloudsql_postgres,
    gcs_bucket,
    memorystore_redis,
)
from app.models import Base, StorageUser
from app.schemas import ListUsersResponse, UserResponse
from flask import Flask, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, text

app = Flask(__name__)

db = SQLAlchemy(
    app,
    model_class=Base,
    engine_options=cloudsql_postgres.sqlalchemy_engine_options(),
)

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def read_root():
    return f"Hello from {lf.environment}"


@app.route("/service_info", methods=["GET"])
def service_info():
    if lf.is_deployment():
        return cloud_run_service.outputs().to_dict()
    return {"message": "Running locally"}


@app.route("/test_redis", methods=["GET"])
def test_redis():
    # Test the Redis connection by setting and getting a key
    redis_client = memorystore_redis.redis()
    redis_client.set("key", "value")
    return redis_client.get("key")


@app.route("/test_db", methods=["GET"])
def test_db():
    # Test the database connection by executing a simple query
    result = db.session.execute(text("SELECT 1")).fetchone()
    return {"result": result[0]}


@app.route("/test_storage", methods=["GET"])
def test_storage():
    # Test the storage bucket connection by uploading and downloading a file
    gcs_bucket.upload_from_string("test.txt", "Hello, world!")
    return gcs_bucket.download_file("test.txt").decode("utf-8")


"""
Example CRUD routes for a user resource
"""


@app.route("/users", methods=["GET"])
def list_users():
    storage_users = db.session.execute(select(StorageUser)).scalars().all()
    return jsonify(
        ListUsersResponse.from_storage(storage_users).model_dump(mode="json")
    )


@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    storage_user = StorageUser(email=data["email"], name=data["name"])
    db.session.add(storage_user)
    db.session.commit()
    return jsonify(UserResponse.from_storage(storage_user).model_dump(mode="json"))


@app.route("/users/<int:user_id>", methods=["GET"])
def read_user(user_id: int):
    storage_user = db.session.get(StorageUser, user_id)
    if storage_user is None:
        abort(404, "User not found")
    return jsonify(UserResponse.from_storage(storage_user).model_dump(mode="json"))


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id: int):
    storage_user = db.session.get(StorageUser, user_id)
    if storage_user is None:
        abort(404, "User not found")
    data = request.json
    storage_user.name = data["name"]
    db.session.commit()
    return jsonify(UserResponse.from_storage(storage_user).model_dump(mode="json"))


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    storage_user = db.session.get(StorageUser, user_id)
    if storage_user is None:
        abort(404, "User not found")
    db.session.delete(storage_user)
    db.session.commit()
    return jsonify(UserResponse.from_storage(storage_user).model_dump(mode="json"))
