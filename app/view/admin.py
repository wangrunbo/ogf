import requests
import re
import os
import time

from flask import Blueprint, request, render_template, redirect, url_for, json
from app import db
from app.model import *
from app.util import validator
from app.util.components import console_out
import path

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


@admin.route('/system/data/', methods=['GET'])
def system_data():
    """
    系统数据
    :return:
    """
    return render_template('admin/system/data.html')


@admin.route('/system/data/create-db/', methods=['POST'])
def create_db():
    """
    生成数据库
    :return:
    """
    db.create_all()

    return redirect(url_for('admin.system_data'))


@admin.route('/system/data/generate/', methods=['POST'])
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
                validator.Rules.Required('请选择需要加载的数据', data=['英灵', '概念礼装', '材料', '关卡'])
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
    timeout = 30

    console_file = os.path.join(path.TMP, 'console_' + request.form['token'])

    console_out('系统启动...', console_file)

    try:
        console_out('开始加载基础数据...', console_file)

        # 加载职介数据
        loaded = True  # 数据是否已全部加载
        console_out('检查职介数据...', console_file)

        data = iter([
            'Saber', 'Lancer', 'Archer', 'Rider', 'Caster', 'Assassin', 'Berserker',
            'Avenger', 'Ruler', 'Shielder', 'Beast', 'Alterego', 'MoonCancer'
        ])

        for i in range(0, Class.query.count()):
            next(data)

        for name in data:
            if loaded:
                loaded = False
                console_out('职介数据开始加载...', console_file)

            db.session.add(Class(name))
            console_out(f'职介--{name}--加载完成！', console_file)

        if loaded:
            console_out('完成！', console_file)
        else:
            db.session.commit()
            console_out('职介数据加载完成！', console_file)

        # 加载阵营数据
        loaded = True  # 数据是否已全部加载
        console_out('检查阵营数据...', console_file)

        data = iter(['天', '地', '人', '星', '兽'])

        for i in range(0, Attribute.query.count()):
            next(data)

        for name in data:
            if loaded:
                loaded = False
                console_out('阵营数据开始加载...', console_file)

            db.session.add(Attribute(name))
            console_out(f'阵营--{name}--加载完成！', console_file)

        if loaded:
            console_out('完成！', console_file)
        else:
            db.session.commit()
            console_out('阵营数据加载完成！', console_file)

        # 加载性别数据
        loaded = True  # 数据是否已全部加载
        console_out('检查性别数据...', console_file)

        data = iter(['男性', '女性', '?', '-'])

        for i in range(0, Gender.query.count()):
            next(data)

        for name in data:
            if loaded:
                loaded = False
                console_out('性别数据开始加载...', console_file)

            db.session.add(Gender(name))
            console_out(f'性别--{name}--加载完成！', console_file)

        if loaded:
            console_out('完成！', console_file)
        else:
            db.session.commit()
            console_out('性别数据加载完成！', console_file)

        # 加载指令卡数据
        loaded = True  # 数据是否已全部加载
        console_out('检查指令卡数据...', console_file)

        data = iter(['Quick', 'Arts', 'Buster'])

        for i in range(0, CommandType.query.count()):
            next(data)

        for name in data:
            if loaded:
                loaded = False
                console_out('指令卡数据开始加载...', console_file)

            db.session.add(CommandType(name))
            console_out(f'指令卡--{name}--加载完成！', console_file)

        if loaded:
            console_out('完成！', console_file)
        else:
            db.session.commit()
            console_out('指令卡数据加载完成！', console_file)

        console_out('基础数据加载完成！', console_file)

        # 加载关卡数据
        if '关卡' in item:
            console_out('开始加载关卡数据...', console_file)
            count = 0

            console_out(f'关卡数据加载完成，共加载了{count}份关卡数据！', console_file)

        # 加载材料数据
        if '材料' in item:
            console_out('开始加载材料数据...', console_file)
            count = 0

            # 原数据清除
            Item.query.delete()

            url = 'http://fgowiki.com/guide/materialdetail/%d'

            data_id = 0
            while True:
                data_id += 1

                html = requests.get(url=url % data_id, timeout=timeout).content.decode('utf-8')

                try:
                    data = re.search(r'^var datadetail = (\[.*?\]);$', html, re.M).group(1)
                    data = json.loads(data, encoding='utf-8')[0]
                except IndexError:
                    console_out(f"材料编号{data_id}未找到。", console_file)
                    break

                db.session.add(Item(
                    id=data_id,
                    name=data['NAME'],
                    icon='http://file.fgowiki.fgowiki.com/mobile/images/Item/%s' % data['ICO'],
                    description=data['ABOUT']
                ))

                count += 1

                console_out(f"材料--{data['NAME']}：加载成功！", console_file)

            db.session.commit()

            console_out(f'材料数据加载完成，共加载了{count}份材料数据！', console_file)

        # 加载概念礼装数据
        if '概念礼装' in item:
            console_out('开始加载概念礼装数据...', console_file)
            count = 0

            url = 'http://fgowiki.com/guide/equipdetail/%d'

            data_id = 0
            while True:
                data_id += 1

                html = requests.get(url=url % data_id, timeout=timeout).content.decode('utf-8')

                try:
                    data = re.search(r'^var datadetail = (\[.*?\]);$', html, re.M).group(1)
                    data = json.loads(data, encoding='utf-8')[0]
                except IndexError:
                    console_out(f"材料编号{data_id}未找到。", console_file)
                    break

                db.session.add(CraftEssence(
                    id=data_id,
                    name=data['NAME_CN'],
                    star=data['STAR'],
                    icon='http://fgowiki.com/fgo/equip/%s.jpg' % str(data_id).zfill(3),
                    image='http://file.fgowiki.fgowiki.com/fgo/card/equip/%sA.jpg' % str(data_id).zfill(3),
                    atk=data['LV1_ATK'],
                    max_atk=data['LVMAX_ATK'],
                    hp=data['LV1_HP'],
                    max_hp=data['LVMAX_HP'],
                    effect=data['SKILL_E'],
                    max_effect=data['SKILLMAX_E'],
                    effect_icon='http://file.fgowiki.fgowiki.com/mobile/images/Skill/%s' % data['ICO'],
                    description=data['INTRO']
                ))

                count += 1

                console_out(f"概念礼装--{data['NAME_CN']}：加载成功！", console_file)

            db.session.commit()

            console_out(f'概念礼装数据加载完成，共加载了{count}件概念礼装数据！', console_file)

        # 加载英灵数据
        if '英灵' in item:
            console_out('开始加载英灵数据...', console_file)
            count = 0

            url = 'http://fgowiki.com/guide/petdetail/%d'

            data_id = 0
            while True:
                data_id += 1

                if Servant.query.get(data_id) is not None:
                    continue

                console_out(f"英灵编号{data_id}：开始加载...", console_file)

                html = requests.get(url=url % data_id, timeout=timeout).content.decode('utf-8')

                try:
                    data = re.search(r'^var datadetail = (\[.*?\]);$', html, re.M).group(1)
                    data = json.loads(data, encoding='utf-8')[0]
                except AttributeError:
                    console_out(f"英灵编号{data_id}未找到。", console_file)
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
                    id=data_id,
                    name=data['NAME'],
                    name_jp=data['NAME_JP'],
                    name_en=data['NAME_EN'],
                    cls=Class.query.filter_by(name=data['CLASS']).one(),
                    star=data['STAR'],
                    cost=data['COST'],
                    icon="http://file.fgowiki.fgowiki.com/fgo/head/%s.jpg" % str(data_id).zfill(3),
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

                console_out(f"英灵--{data['NAME']}--编号{data_id}：加载成功！", console_file)

            db.session.commit()

            console_out(f'英灵数据加载完成，共加载了{count}名英灵数据！', console_file)

    except requests.exceptions.ConnectionError:
        console_out('连接超时！', console_file)

    except Exception as e:
        console_out('异常：' + str(e), console_file)

    else:
        console_out('数据加载完成！', console_file)

    console_out('系统中止！', console_file)

    return json.jsonify(error_messages)


@admin.route('/system/data/generate/status/', methods=['POST'])
def generate_console():
    timeout = 60

    line = int(request.form['line'])
    console_file = os.path.join(path.TMP, 'console_' + request.form['token'])

    if request.args.get('d') == '1':
        os.remove(console_file)

        return json.jsonify(None)
    else:
        start_time = time.time()

        while True:
            # 超时
            if time.time() - start_time > timeout:
                os.remove(console_file)

                return json.jsonify(None)

            if os.path.exists(console_file):
                with open(console_file, 'r', encoding='utf-8') as file:
                    output = file.readlines()

                    if len(output) > line:
                        return json.jsonify({
                            'line': len(output),
                            'messages': [message[:-1] for message in output[line::]]
                        })
