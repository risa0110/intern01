from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..auth.models import User
from ..models import DB

PROFILE_BP = Blueprint(
    "profile", __name__, url_prefix="/profile", template_folder="templates"
)


@PROFILE_BP.route("/", methods=["GET", "POST"])
@login_required
def profile():
    user = {
        "username": current_user.username,
        "current_point": current_user.current_point,
        "monthly_point": current_user.monthly_point,
        "goal_point": current_user.goal_point,
    }

    return render_template("profile.html", user=user)
