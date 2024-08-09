from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..auth.models import User
from .form import UpdateUserForm
from .util import delete_user, update_user

ADMIN_BP = Blueprint(
    "admin", __name__, url_prefix="/admin", template_folder="templates"
)


@ADMIN_BP.route("/", methods=["GET", "POST"])
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for("app.profile.profile"))
    user_all = User.query.all()
    users = [
        {
            "id": user.id,
            "username": user.username,
            "current_point": user.current_point,
            "monthly_point": user.monthly_point,
            "goal_point": user.goal_point,
            "is_admin": user.is_admin,
        }
        for user in user_all
    ]

    return render_template("admin.html", users=users)


@ADMIN_BP.route("/update", methods=["GET", "POST"])
@login_required
def update():
    if not current_user.is_admin:
        return redirect(url_for("app.update.update"))
    form = UpdateUserForm()
    if request.method == "POST":
        user_id = form.user_id.data
        data = {
            "username": form.username.data,
            "current_point": form.current_point.data,
            "monthly_point": form.monthly_point.data,
            "goal_point": form.goal_point.data,
            "is_admin": form.is_admin.data,
        }
        if form.password.data:
            data["password"] = form.password.data

        if user_id == current_user.id and not data["is_admin"]:
            flash("自分自身を管理者から外すことはできません", "danger")
            return redirect(url_for("app.admin.admin"))

        if update_user(user_id, data):
            flash("更新しました", "success")
        else:
            flash("更新に失敗しました", "danger")

        return redirect(url_for("app.admin.admin"))

    elif request.method == "GET":
        user_id = int(request.args.get("user_id"))
        user = User.query.get(user_id)
        if user:
            form.user_id.data = user.id
            form.username.data = user.username
            form.current_point.data = user.current_point
            form.monthly_point.data = user.monthly_point
            form.goal_point.data = user.goal_point
            form.is_admin.data = user.is_admin
            return render_template("admin_update.html", form=form)
        return redirect(url_for("app.admin.admin"))


@ADMIN_BP.route("/delete", methods=["POST"])
@login_required
def delete():
    if not current_user.is_admin:
        return redirect(url_for("app.profile.profile"))
    user_id = int(request.args.get("user_id"))
    if user_id == current_user.id:
        flash("自分自身を削除することはできません", "danger")
        return redirect(url_for("app.admin.admin"))

    if delete_user(user_id):
        flash("ユーザーが削除されました", "success")
    else:
        flash("ユーザーが見つかりませんでした", "danger")

    return redirect(url_for("app.admin.admin"))
