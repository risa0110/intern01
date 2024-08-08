from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from ..auth.models import User
from ..models import DB

API_BP = Blueprint("api", __name__, url_prefix="/api", template_folder="templates")


@API_BP.route("/users", methods=["GET"])
@login_required
def get_users():
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403

    users = User.query.all()
    data = [
        {
            "id": user.id,
            "username": user.username,
            "current_point": user.current_point,
            "monthly_point": user.monthly_point,
            "goal_point": user.goal_point,
            "is_admin": user.is_admin,
        }
        for user in users
    ]
    return jsonify(data)


@API_BP.route("/users/<int:user_id>", methods=["GET"])
@login_required
def get_user(user_id):
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = {
        "id": user.id,
        "username": user.username,
        "current_point": user.current_point,
        "monthly_point": user.monthly_point,
        "goal_point": user.goal_point,
        "is_admin": user.is_admin,
    }
    return jsonify(data)


@API_BP.route("/users", methods=["POST"])
@login_required
def create_user():
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403

    data = request.json
    username = data.get("username")
    hashed_password = generate_password_hash(data.get("password"))

    user = User(username, hashed_password)

    try:
        DB.session.add(user)
        DB.session.commit()
    except IntegrityError:
        DB.session.rollback()
        return jsonify({"message": "Username already exists"}), 400

    return jsonify({"message": "User created successfully"}), 201


@API_BP.route("/users/<int:user_id>", methods=["PUT"])
@login_required
def update_user(user_id):
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403

    data = request.json
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    new_username = data.get("username")
    if new_username:
        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({"message": "Username already exists"}), 400

    user.username = data.get("username", user.username)
    if "password" in data:
        user.hashed_password = generate_password_hash(data["password"])
    user.current_point = data.get("current_point", user.current_point)
    user.monthly_point = data.get("monthly_point", user.monthly_point)
    user.goal_point = data.get("goal_point", user.goal_point)
    user.is_admin = data.get("is_admin", user.is_admin)

    DB.session.commit()
    return jsonify({"message": "User updated successfully"})


@API_BP.route("/users/<int:user_id>", methods=["DELETE"])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    if user.id == current_user.id:
        return jsonify({"message": "Cannot delete yourself"}), 400

    DB.session.delete(user)
    DB.session.commit()
    return jsonify({"message": "User deleted successfully"})


@API_BP.route("/profile", methods=["GET"])
@login_required
def get_profile():
    user = current_user
    data = {
        "username": user.username,
        "current_point": user.current_point,
        "monthly_point": user.monthly_point,
        "goal_point": user.goal_point,
    }
    return jsonify(data)


@API_BP.route("/profile", methods=["PUT"])
@login_required
def update_profile():
    data = request.json
    user = current_user

    # new_username = data.get("username")
    # if new_username:
    #     existing_user = User.query.filter_by(username=new_username).first()
    #     if existing_user and existing_user.id != user.id:
    #         return jsonify({"message": "Username already exists"}), 400

    # user.username = new_username if new_username else user.username
    # if "password" in data:
    #     user.password = generate_password_hash(data["password"])
    user.current_point = data.get("current_point", user.current_point)
    user.monthly_point = data.get("monthly_point", user.monthly_point)
    user.goal_point = data.get("goal_point", user.goal_point)

    DB.session.commit()
    return jsonify({"message": "Your profile updated successfully"})
