from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class cosmic_print(FlaskForm):
    cosmic_id = StringField('cosmic_id')
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    datetime = StringField('date')
    name_cosmic = StringField('name_cosmic', validators=[DataRequired()])


class cosmic_download(FlaskForm):
    submit = SubmitField('Скачать')