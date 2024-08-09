from werkzeug.security import generate_password_hash

from ..auth.models import User
from ..models import DB


def update_user(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return False

    new_username = data.get("username")
    if new_username:
        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user and existing_user.id != user_id:
            return False

    user.username = data.get("username", user.username)
    if "password" in data:
        user.hashed_password = generate_password_hash(data["password"])
    user.current_point = data.get("current_point", user.current_point)
    user.monthly_point = data.get("monthly_point", user.monthly_point)
    user.goal_point = data.get("goal_point", user.goal_point)
    user.is_admin = data.get("is_admin", user.is_admin)

    DB.session.commit()
    return True


def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return False

    DB.session.delete(user)
    DB.session.commit()
    return True
