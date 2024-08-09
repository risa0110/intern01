from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, ReadOnly


class UpdateUserForm(FlaskForm):
    user_id = IntegerField("User ID", validators=[ReadOnly()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Optional()])
    current_point = IntegerField(
        "Current Point", validators=[DataRequired(), NumberRange(min=0)]
    )
    monthly_point = IntegerField(
        "Monthly Point", validators=[DataRequired(), NumberRange(min=0)]
    )
    goal_point = IntegerField(
        "Goal Point", validators=[DataRequired(), NumberRange(min=0)]
    )
    is_admin = BooleanField("Admin")
    submit = SubmitField("更新")
