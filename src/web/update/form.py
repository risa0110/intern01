from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UpdateProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    current_point = StringField("Current Point", validators=[DataRequired()])
    monthly_point = StringField("Monthly Point", validators=[DataRequired()])
    goal_point = StringField("Goal Point", validators=[DataRequired()])
    submit = SubmitField("更新")
