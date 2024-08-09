from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user

SIMULATION_BP = Blueprint(
    "simulation", __name__, url_prefix="/simulation", template_folder="templates"
)


@SIMULATION_BP.route("/", methods=["GET"])
def simulation():
    # if current_user.is_authenticated:
    #     init_data = {
    #         "current_point": current_user.current_point,
    #         "monthly_point": current_user.monthly_point,
    #         "goal_point": current_user.goal_point,
    #     }
    #     is_authenticated = True
    # else:
    #     init_data = {
    #         "current_point": 0,
    #         "monthly_point": 0,
    #         "goal_point": 0,
    #     }
    #     is_authenticated = False
    # return render_template("simulation.html", init_data=init_data, is_authenticated=is_authenticated)

    return redirect(url_for("app.index"))
