from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class cosmic_print(FlaskForm):
    cosmic_id = StringField('cosmic_id')
    last_name = StringField('last_name', validators=[DataRequired()])
    first_name = StringField('first_name', validators=[DataRequired()])
    middle_name = StringField('middle_name')
    datetime = StringField('date')
    name_cosmic = StringField('name_cosmic', validators=[DataRequired()])
    submit = SubmitField('Отправить форму')


class cosmic_download(FlaskForm):
    submit = SubmitField('Посмотреть подробно')