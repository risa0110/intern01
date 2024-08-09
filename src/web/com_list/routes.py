from flask import (
    Blueprint,
    render_template,
    request,
)
from flask_login import current_user

from .util import filter_products_by_int, get_json_data, sort_products

COMLIST_BP = Blueprint(
    "comlist", __name__, url_prefix="/com_list", template_folder="templates"
)


@COMLIST_BP.route("/", methods=["GET", "POST"])
def com_list():
    products = get_json_data()["content"]
    products_max_point = max(int(product["points"]) for product in products)
    min_points = request.form.get("min_points", "0")
    max_points = request.form.get("max_points")

    if request.method == "POST":
        min_points_tmp = int(min_points) if min_points else 0
        max_points_tmp = int(max_points) if max_points else products_max_point

        products = filter_products_by_int(
            products, "points", min_points_tmp, max_points_tmp
        )

    elif request.method == "GET":
        max_points_query = request.args.get("max_points")
        max_points = max_points_query
        max_points_tmp = (
            int(max_points_query) if max_points_query else products_max_point
        )

        products = filter_products_by_int(products, "points", 0, max_points_tmp)

    products = sort_products(products)

    return render_template(
        "product.html",
        products=products,
        min_points=min_points,
        max_points=max_points,
        is_authenticated=current_user.is_authenticated,
    )
