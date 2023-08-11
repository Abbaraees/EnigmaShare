from flask_wtf import FlaskForm
from wtforms import StringField, FileField, TextAreaField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired



class CreateMessageForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    receiver = StringField("Receiver's username", validators=[DataRequired()])
    file = FileField('Image file', validators=[DataRequired()])
    allow_encryption = BooleanField('Set Encryption')
    encryption_key = PasswordField('Encryption Key')
    submit = SubmitField("Send")
