from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    email = StringField(
        label='メール',
        validators=[DataRequired(message='メールを入力してください')]
    )
    password = PasswordField(
        label='パスワード',
        validators=[DataRequired(message='パスワードを入力してください')]
    )
