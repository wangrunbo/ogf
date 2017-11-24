from flask import Blueprint, render_template

mypage = Blueprint('mypage', __name__, url_prefix='/mypage')


@mypage.route('/information')
def timeline():
    # 做些处理
    return 'mypage info'
