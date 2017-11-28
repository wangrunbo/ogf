import requests
import re

from flask import Blueprint, request, render_template, redirect, url_for, json
from app import db
from app.model import *
from app.util import validator


admin = Blueprint('admin', __name__)


@admin.route('/')
def index():
    return 'index'


@admin.route('/system/', methods=['GET', 'POST'])
def system():
    """
    系统设定
    :return:
    """
    return render_template('admin/system/index.html')


@admin.route('/system/data', methods=['GET'])
def system_data():
    """
    系统数据
    :return:
    """
    return render_template('admin/system/data.html')


@admin.route('/system/data/create-db', methods=['POST'])
def create_db():
    """
    生成数据库
    :return:
    """
    db.create_all()

    return redirect(url_for('admin.system_data'))


@admin.route('/system/data/generate', methods=['POST'])
def generate_data():
    """
    加载数据
    :return:
    """
    # TODO 检查是否有人正在同时加载

    item = request.form.to_dict(flat=False).get('item')
    channel = request.form.get('channel')

    # Validation
    error_messages = validator.validate({
        'item': {
            'data': item,
            'rules': [
                validator.Rules.Required('请选择需要加载的数据', data=['英灵', '概念礼装', '材料'])
            ]
        },
        'channel': {
            'data': channel,
            'rules': [
                validator.Rules.Required('请选择加载数据途径', data=['fgowiki'])
            ]
        }
    })

    if error_messages is not None:
        return json.jsonify(error_messages)

    # 开始加载
    print('系统启动...')
    print('开始加载基础信息...')

    try:
        # 加载职介信息
        print('职介信息开始加载...')

        data = iter([
            'Saber', 'Lancer', 'Archer', 'Rider', 'Caster', 'Assassin', 'Berserker',
            'Avenger', 'Ruler', 'Shielder', 'Beast', 'Alterego', 'MoonCancer'
        ])

        for i in range(0, Class.query.count()):
            next(data)

        for name in data:
            db.session.add(Class(name))

            print(f'职介--{name}--加载完成！')

        db.session.commit()

        print('职介信息加载完成！')

        # 加载阵营信息
        print('阵营信息开始加载...')

        data = iter(['天', '地', '人', '星', '兽'])

        for i in range(0, Attribute.query.count()):
            next(data)

        for name in data:
            db.session.add(Attribute(name))

            print(f'阵营--{name}--加载完成！')

        db.session.commit()

        print('阵营信息加载完成！')

        # 加载性别信息
        print('性别信息开始加载...')

        data = iter(['男性', '女性', '?', '-'])

        for i in range(0, Gender.query.count()):
            next(data)

        for name in data:
            db.session.add(Gender(name))

            print(f'性别--{name}--加载完成！')

        db.session.commit()

        print('性别信息加载完成！')

        # 加载指令卡信息
        print('指令卡信息开始加载...')

        data = iter(['Quick', 'Arts', 'Buster'])

        for i in range(0, CommandType.query.count()):
            next(data)

        for name in data:
            db.session.add(CommandType(name))

            print(f'指令卡--{name}--加载完成！')

        db.session.commit()

        print('指令卡信息加载完成！')

        print('基础信息加载完成！')

        # 加载英灵数据
        if '英灵' in item:
            print('开始加载英灵数据...')

            url = 'http://fgowiki.com/guide/petdetail/%d'

            servant_id = 0
            count = 0
            while True:
                servant_id += 1

                if Servant.query.get(servant_id) is not None:
                    continue

                print(f"英灵编号{servant_id}：开始加载...")

                html = requests.get(url=url % servant_id).content.decode('utf-8')

                try:
                    data = re.search(r'^var datadetail = (\[.*?\]);$', html, re.M).group(1)
                    data = json.loads(data, encoding='utf-8')[0]
                except AttributeError:
                    print(f"英灵编号{servant_id}未找到。")
                    break

                # 性别
                if data['GENDER'] == '男性':
                    gender = Gender.query.get(Gender.MALE)
                elif data['GENDER'] == '女性':
                    gender = Gender.query.get(Gender.FEMALE)
                elif re.search(r'\?', data['GENDER']):
                    gender = Gender.query.get(id=Gender.UNKNOWN)
                else:
                    gender = Gender.query.get(id=Gender.SKIP)

                # 宝具名
                np_name = re.match(r'^(.+?)(\(.+\))$', data['T_NAME'])
                np_name_zh = np_name.group(1)
                np_name_en = np_name.group(2)

                db.session.add(Servant(
                    id=servant_id,
                    name=data['NAME'],
                    name_jp=data['NAME_JP'],
                    name_en=data['NAME_EN'],
                    cls=Class.query.filter_by(name=data['CLASS']).one(),
                    star=data['STAR'],
                    cost=data['COST'],
                    icon=f"http://file.fgowiki.fgowiki.com/fgo/head/{str(servant_id).zfill(3)}.jpg",
                    attribute=Attribute.query.filter_by(name=data['CAMP']).one(),
                    atk=data['LV1_ATK'],
                    max_atk=data['LVMAX4_ATK'],
                    atk_90=data['LV90_ATK'],
                    atk_100=data['LV100_ATK'],
                    hp=data['LV1_HP'],
                    max_hp=data['LVMAX4_HP'],
                    hp_90=data['LV90_HP'],
                    hp_100=data['LV100_HP'],
                    quick=data['CARD_QUICK'],
                    arts=data['CARD_ARTS'],
                    buster=data['CARD_BUSTER'],
                    hits_quick=data['QuiHit'],
                    hits_arts=data['ArtHit'],
                    hits_buster=data['BusHit'],
                    hits_ex=data['EXHit'],
                    illustrator=data['ILLUST'],
                    cv=data['CV'],
                    alignment=data['Attributes'],
                    gender=gender,
                    region=data['Region'],
                    height=data['Height'],
                    weight=data['Weight'],
                    crit_generation=data['Crit'],
                    death_rate=data['Death'],
                    crit_absorption=data['CritPr'],
                    np_charge_quick=data['TdPointQ'],
                    np_charge_arts=data['TdPointA'],
                    np_charge_buster=data['TdPointB'],
                    np_charge_ex=data['TdPointEx'],
                    np_charge_np=data['InitiativeNp'],
                    np_charge_def=data['Passive'],
                    origin=data['Origin'],
                    growth_curve=data['Circle'],
                    np_name=np_name_zh,
                    np_name_en=np_name_en,
                    np_rank=data['T_LEVEL'],
                    np_classification=data['T_TYPE'],
                    np_type=CommandType.query.filter_by(name=data['T_PROP']).one()
                ))

                count += 1

                print(f"英灵--{data['NAME']}--编号{servant_id}：加载成功！")

            db.session.commit()

            print(f'英灵数据加载完成，共加载了{count}名英灵数据')

        if '概念礼装' in item:
            print('开始加载概念礼装数据...')

        if '材料' in item:
            print('开始加载材料数据...')

    except Exception as e:
        error_messages = str(e)

        print('异常：' + error_messages)

    else:
        print('数据加载完成！')

    print('系统中止！')

    return json.jsonify(error_messages)



