from flask_wtf import Form
from wtforms import widgets
from wtforms import SelectField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired


class CatchDataForm(Form):
    item = SelectMultipleField(
        label='数据',
        choices=[('英灵', '英灵'), ('概念礼装', '概念礼装'), ('材料', '材料')],
        validators=[DataRequired(message='请选择需要获取的数据！')]
    )
    channel = SelectField(
        label='途径',
        choices=[('fgowiki', 'fgowiki')],
        validators=[DataRequired(message='请选择数据获取途径！')]
    )
