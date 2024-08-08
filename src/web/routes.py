import logging

from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

from web.admin.routes import ADMIN_BP
from web.api.routes import API_BP
from web.auth.routes import AUTH_BP
from web.com_list.routes import COMLIST_BP
from web.profile.routes import PROFILE_BP
from web.simulation.routes import SIMULATION_BP
from web.update.routes import UPDATE_BP

APP_BP = Blueprint("app", __name__)

# ログイン用のエンドポイントを追加する
APP_BP.register_blueprint(AUTH_BP)

APP_BP.register_blueprint(ADMIN_BP)
APP_BP.register_blueprint(PROFILE_BP)
APP_BP.register_blueprint(UPDATE_BP)
APP_BP.register_blueprint(SIMULATION_BP)

APP_BP.register_blueprint(COMLIST_BP)
APP_BP.register_blueprint(API_BP)


@APP_BP.route("/")
def index():
    # ログ出力の方法
    logging.debug("トップページにアクセスされました")
    # return render_template("index.html")
    return redirect(url_for("app.simulation.simulation"))


@APP_BP.route("/secret")
@login_required  # 画面デザイン中はコメントアウトしておくとよい (編集するたびにログインが切れてしまうため)
def secret():
    logging.debug("シークレットページにアクセスされました")
    # テンプレート内で直接 current_user を使わずに外から明示的に渡してあげると、画面デザ
    # イン時にダミーデータを渡すことができて便利

    # 例: 画面デザイン中
    # return render_template(
    #     "secret.html",
    #     user=User(
    #         username="test_user",
    #         hashed_password="dummy_value",
    #     ),
    # )

    # 画面デザイン完了後、動作確認中
    return render_template("secret.html", user=current_user)
