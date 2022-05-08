from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class DishsForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    content = TextAreaField("Состав")
    proteins = StringField('белки', validators=[DataRequired()])
    fats = StringField('жиры', validators=[DataRequired()])
    carbohydrates = StringField('углеводы', validators=[DataRequired()])
    calories = StringField('калории', validators=[DataRequired()])
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')
