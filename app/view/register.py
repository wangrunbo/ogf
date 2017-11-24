from datetime import datetime, timedelta
from flask import Blueprint, request, session, render_template, redirect, make_response, abort, url_for, jsonify
from app import app, db
from app.model import User, UserStatus
from app.form import UserForm
from app.util.security import ts
from app.util.mail import send_register_mail
from app.locale.session import SESSION

register = Blueprint('register', __name__, url_prefix='/register')


@register.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()

    if form.validate_on_submit():
        user = User(
            uid=User.new_uid(),
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
            secret_key=User.new_secret_key(),
            user_status_id=UserStatus.INACTIVE,
            registration_ip=request.remote_addr
        )

        db.session.add(user)
        db.session.commit()

        send_register_mail(user)

        session[SESSION.REGISTER.MAIL] = user.email

        return redirect(url_for('register.complete'))

    return render_template('register/index.html', form=form)


@register.route('/complete', methods=['GET'], defaults={'token': None})
@register.route('/<token>/complete', methods=['GET'])
def complete(token):
    if token:
        session.pop(SESSION.REGISTER.MAIL, None)

        try:
            secret_key = ts.loads(token, salt=app.config['TOKEN_SALT'], max_age=86400)
        except:
            abort(404)
        else:
            user = User.query.filter_by(secret_key=secret_key, user_status_id=UserStatus.INACTIVE).first_or_404()

            user.user_status_id = UserStatus.GENERAL
            user.secret_key = User.new_secret_key()

            db.session.add(user)
            db.session.commit()

            return render_template('register/complete.html')
    else:
        email = session.get(SESSION.REGISTER.MAIL)

        if not email:
            abort(404)

        return render_template('register/activate.html', email=email)


@register.route('/send-confirm-mail', methods=['GET'])
def send_confirm_mail():
    time = datetime.now()

    user = User.query.filter(
        User.email == session.get(SESSION.REGISTER.MAIL),
        User.user_status_id == UserStatus.INACTIVE
    ).first()

    if not user:
        session.pop(SESSION.REGISTER.MAIL_SENT_TIME, None)

        return make_response(jsonify(False))

    if time - session.get(SESSION.REGISTER.MAIL_SENT_TIME, time - timedelta(seconds=30)) > timedelta(seconds=25):
        session[SESSION.REGISTER.MAIL_SENT_TIME] = time

        send_register_mail(user)

    return make_response(jsonify(True))
