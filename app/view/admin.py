from flask import Blueprint, request, render_template
from app.form import CatchDataForm

admin = Blueprint('admin', __name__)


@admin.route('/')
def index():
    return 'index'


@admin.route('/system/')
def system():
    return render_template('admin/system/index.html')


@admin.route('/system/catch-data', methods=['GET', 'POST'])
def catch_data():
    """
    获取数据
    :return:
    """
    form = CatchDataForm(item='英灵')

    if request.method == 'POST':
        catch = request.json

    return render_template('admin/system/catch_data.html', form=form)
