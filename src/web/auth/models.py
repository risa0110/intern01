from flask_login import UserMixin

from ..models import DB


class User(DB.Model, UserMixin):
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(128), unique=True)
    hashed_password = DB.Column(DB.String(256))
    current_point = DB.Column(DB.Integer, default=0)
    monthly_point = DB.Column(DB.Integer, default=0)
    goal_point = DB.Column(DB.Integer, default=0)
    is_admin = DB.Column(DB.Boolean, default=False)

    def __init__(self, username: str, hashed_password: str):
        self.username = username
        self.hashed_password = hashed_password
        if username == "admin":
            self.is_admin = True
