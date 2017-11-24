from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from app.util.validator import Unique
from app.model.User import User


class UserForm(FlaskForm):
    email = StringField(
        label='メール',
        validators=[
            DataRequired(message='メールを入力してください'),
            Email(message='メールの形式が間違っています'),
            Unique(User, User.email, message='該当ユーザー名が存在しています')
        ]
    )
    username = StringField(
        label='ユーザー名',
        validators=[
            DataRequired(message='ユーザー名を入力してください'),
            Unique(User, User.username, message='該当ユーザー名が存在しています')
        ]
    )
    password = PasswordField(
        label='パスワード',
        validators=[DataRequired(message='パスワードを入力してください')]
    )
    password_confirm = PasswordField(
        label='パスワード確認',
        validators=[
            DataRequired(message='パスワードをもう一度入力してください'),
            EqualTo('password', message='パスワードが一致しません')
        ]
    )
