from app.infra import postgres
from app.models import Base, StorageUser
from app.schemas import ListUsersResponse, UserResponse
from flask import Flask, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

app = Flask(__name__)

db = SQLAlchemy(
    app,
    model_class=Base,
    engine_options=postgres.sqlalchemy_engine_options(),
)

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def list_users():
    storage_users = db.session.execute(select(StorageUser)).scalars().all()
    return jsonify(
        ListUsersResponse.from_storage(storage_users).model_dump(mode="json")
    )


@app.route("/", methods=["POST"])
def create_user():
    data = request.json
    storage_user = StorageUser(email=data["email"], name=data["name"])
    db.session.add(storage_user)
    db.session.commit()
    return jsonify(UserResponse.from_storage(storage_user).model_dump(mode="json"))


@app.route("/<int:user_id>", methods=["GET"])
def read_user(user_id: int):
    storage_user = db.session.get(StorageUser, user_id)
    if storage_user is None:
        abort(404, "User not found")
    return jsonify(UserResponse.from_storage(storage_user).model_dump(mode="json"))


@app.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id: int):
    storage_user = db.session.get(StorageUser, user_id)
    if storage_user is None:
        abort(404, "User not found")
    data = request.json
    storage_user.name = data["name"]
    db.session.commit()
    return jsonify(UserResponse.from_storage(storage_user).model_dump(mode="json"))


@app.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    storage_user = db.session.get(StorageUser, user_id)
    if storage_user is None:
        abort(404, "User not found")
    db.session.delete(storage_user)
    db.session.commit()
    return jsonify(UserResponse.from_storage(storage_user).model_dump(mode="json"))


if __name__ == "__main__":
    app.run(debug=True)
