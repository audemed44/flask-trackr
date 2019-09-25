from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class AddToListForm(FlaskForm):
    media_id = HiddenField('Media_ID')
    media = HiddenField('Media')
    score = StringField('Score', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Completed', 'Completed'), ('Watching', 'Watching'), ('Dropped', 'Dropped'),('Plan to Watch','Plan to Watch'), ('On Hold','On Hold')])
    submit = SubmitField('Add to List')
    def validate_score(self, score):
        if float(score) > 10.0 or float(score) < 0.0:
            raise ValidationError('Score must be between 0 to 10')
     