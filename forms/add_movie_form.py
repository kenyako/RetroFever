from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, IntegerField
from wtforms.validators import DataRequired


class AddMovie(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    about = TextAreaField('Description', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    duration = StringField('Duration (minutes)', validators=[DataRequired()])
    director = StringField('Director', validators=[DataRequired()])
    production = StringField('Production', validators=[DataRequired()])
    premiere = StringField('Premiere Date', validators=[DataRequired()])
    budget = StringField('Budget (In millions $)',
                         validators=[DataRequired()])

    image = FileField('Movie Cover', validators=[DataRequired()])
    submit = SubmitField('Commit')
