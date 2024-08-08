from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class UpdateProfileForm(FlaskForm):
    current_point = IntegerField(
        "Current Point", validators=[DataRequired(), NumberRange(min=0)]
    )
    monthly_point = IntegerField(
        "Monthly Point", validators=[DataRequired(), NumberRange(min=0)]
    )
    goal_point = IntegerField(
        "Goal Point", validators=[DataRequired(), NumberRange(min=0)]
    )
    submit = SubmitField("更新")
