from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..auth.models import User
from ..models import DB

ADMIN_BP = Blueprint(
    "admin", __name__, url_prefix="/admin", template_folder="templates"
)


@ADMIN_BP.route("/", methods=["GET", "POST"])
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for("app.profile.profile"))
    users = User.query.all()
    me=current_user
    username=me.username
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

    return render_template("admin.html", data=data)


@ADMIN_BP.route("/delete/<user_id>", methods=["POST"])
@login_required
def delete(user_id):
    if not current_user.is_admin:
        return render_template("user.html"), 403

    user = User.query.filter_by(id=user_id).first()
    if user and user.id != current_user.id:
        DB.session.delete(user)
        DB.session.commit()
    return redirect(url_for("app.admin.admin"))
