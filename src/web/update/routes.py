from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..models import DB
from .form import UpdateProfileForm

UPDATE_BP = Blueprint(
    "update", __name__, url_prefix="/update", template_folder="templates"
)


@UPDATE_BP.route("/", methods=["GET", "POST"])
@login_required
def update():
    form = UpdateProfileForm()
    user = current_user

    if request.method == "POST":
        # なんかうまくいかない
        # if form.validate_on_submit():
        #     pass
        user.current_point = form.current_point.data
        user.monthly_point = form.monthly_point.data
        user.goal_point = form.goal_point.data
        DB.session.commit()
        return redirect(url_for("app.profile.profile"))  # 修正されたエンドポイント名
    elif request.method == "GET":
        form.current_point.data = user.current_point
        form.monthly_point.data = user.monthly_point
        form.goal_point.data = user.goal_point
    return render_template("update.html", form=form, username=user.username)
