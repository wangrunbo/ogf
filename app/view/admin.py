import os
import time
import re
import requests

from flask import Blueprint, request, render_template, redirect, url_for, json
from app import db
from app.model import *
from app.util import validator
from app.util.components import console_out
import path

admin = Blueprint('admin', __name__)


@admin.route('/')
def index():
    return render_template('admin/index.html')


@admin.route('/servant/', methods=['GET'])
def servant_list():
    page = request.args.get('p', 1, int)
    search = request.args.get('s')

    pagination = Servant.query.paginate(page=page, per_page=20, error_out=False)
    servants = pagination.items

    return render_template('admin/servant/index.html', servants=servants, pagination=pagination)


@admin.route('/servants/<servant_id>/edit/', methods=['GET'])
def servant_edit(servant_id):
    """

    :param servant_id:
    :return:
    """
    servant = Servant.query.get_or_404(servant_id)

    return render_template(
        'admin/servant/edit.html',
        servant=servant,
        stage_lv=[[stage_lv for stage_lv in servant.stage_lv if stage_lv.stage == lv] for lv in range(1, 5)],
        skill_lv=[[skill_lv for skill_lv in servant.skill_lv if skill_lv.stage == lv] for lv in range(2, 11)],
        classes=Class.query.all(),
        attributes=Attribute.query.all(),
        genders=Gender.query.all(),
        command_types=CommandType.query.all(),
        items=Item.query.all()
    )


@admin.route('/servants/<servant_id>/upload_icon/', methods=['POST'])
def servant_upload_icon(servant_id):
    servant = Servant.query.get_or_404(servant_id)
    return 'servant upload icon'


@admin.route('/servants/<servant_id>/edit/basic', methods=['POST'])
def servant_edit_basic(servant_id):
    servant = Servant.query.get_or_404(servant_id)
    data = {
        'name': request.form('name'),
        'name_jp': request.form('name_jp'),
        'name_en': request.form('name_en'),
        'class_id': request.form('class_id'),
        'star': request.form('star'),
        'cost': request.form('cost'),
        'attribute_id': request.form('attribute_id'),
        'atk': request.form('atk'),
        'max_atk': request.form('max_atk'),
        'atk_90': request.form('atk_90'),
        'atk_100': request.form('atk_100'),
        'hp': request.form('hp'),
        'max_hp': request.form('max_hp'),
        'hp_90': request.form('hp_90'),
        'hp_100': request.form('hp_100'),
        'quick': request.form('quick'),
        'arts': request.form('arts'),
        'buster': request.form('buster'),
        'hits_quick': request.form('hits_quick'),
        'hits_arts': request.form('hits_arts'),
        'hits_buster': request.form('hits_buster'),
        'hits_ex': request.form('hits_ex'),
        'illustrator': request.form('illustrator'),
        'cv': request.form('cv'),
    }

    # TODO validation

    return redirect(url_for('admin.servant_edit', servant_id=servant_id), 200)


@admin.route('/craft-essence/')
def craft_essence_list():
    return render_template('admin/craft_essence/index.html')


@admin.route('/item/')
def item_list():
    return render_template('admin/item/index.html')


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
    # CREATE DATABASE fgo DEFAULT CHARACTER SET utf8;
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
            'Avenger', 'Ruler', 'Shielder', 'Beast', 'Alterego', 'MoonCancer', 'Foreigner'
        ])

        for i in range(0, Class.query.count()):
            next(data)

        for name in data:
            if loaded:
                loaded = False
                console_out('职介数据开始加载...', console_file)

            db.session.add(Class(name))
            console_out('职介--%s--加载完成！' % name, console_file)

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
            console_out('阵营--%s--加载完成！' % name, console_file)

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
            console_out('性别--%s--加载完成！' % name, console_file)

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
            console_out('指令卡--%s--加载完成！' % name, console_file)

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

            console_out('关卡数据加载完成，共加载了%d份关卡数据！' % count, console_file)

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
                    console_out("材料编号%d未找到。" % data_id, console_file)
                    break

                db.session.add(Item(
                    id=data_id,
                    name=data['NAME'],
                    icon='http://file.fgowiki.fgowiki.com/mobile/images/Item/%s' % data['ICO'],
                    description=data['ABOUT']
                ))

                count += 1

                console_out("材料--%s：加载成功！" % data['NAME'], console_file)

            db.session.commit()

            console_out('材料数据加载完成，共加载了%d份材料数据！' % count, console_file)

        # 加载概念礼装数据
        if '概念礼装' in item:
            console_out('开始加载概念礼装数据...', console_file)
            count = 0

            url = 'http://fgowiki.com/guide/equipdetail/%d'

            data_id = 0
            while True:
                data_id += 1

                if CraftEssence.query.get(data_id) is not None:
                    continue

                html = requests.get(url=url % data_id, timeout=timeout).content.decode('utf-8')

                try:
                    data = re.search(r'^var datadetail = (\[.*?\]);$', html, re.M).group(1)
                    data = json.loads(data, encoding='utf-8')[0]
                except IndexError:
                    console_out("材料编号%d未找到。" % data_id, console_file)
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

                console_out("概念礼装--%s：加载成功！" % data['NAME_CN'], console_file)

            db.session.commit()

            console_out('概念礼装数据加载完成，共加载了%d件概念礼装数据！' % count, console_file)

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

                console_out("英灵编号%d：开始加载..." % data_id, console_file)

                html = requests.get(url=url % data_id, timeout=timeout).content.decode('utf-8')

                try:
                    data = re.search(r'^var datadetail = (\[.*?\]);$', html, re.M).group(1)
                    data = json.loads(data, encoding='utf-8')[0]
                except AttributeError:
                    console_out("英灵编号%d未找到。" % data_id, console_file)
                    break

                # 职介
                data['CLASS'] = data['CLASS'].replace('Grand', '').replace(' ', '')
                if data['CLASS'].startswith('Beast'):
                    data['CLASS'] = 'Beast'

                # 性别
                if data['Gender'] == '男性':
                    gender = Gender.query.get(Gender.MALE)
                elif data['Gender'] == '女性':
                    gender = Gender.query.get(Gender.FEMALE)
                elif re.search(r'\?', data['Gender']):
                    gender = Gender.query.get(Gender.UNKNOWN)
                else:
                    gender = Gender.query.get(Gender.SKIP)

                # 宝具名
                if data['T_NAME'] == '':
                    np_name_zh = ''
                    np_name_en = ''
                else:
                    np_name = re.match(r'^(.+?)(?:（(.+)）)?$', data['T_NAME'])
                    np_name_zh = np_name.group(1)
                    np_name_en = np_name.group(2)

                # QP消耗
                qp_stage = ['0'] * 5 if data['Berak_QP_Arr'] == '' else data['Berak_QP_Arr'].split('|')
                qp_skill = ['0'] * 9 if data['Skill_QP_Arr'] == '' else data['Skill_QP_Arr'].split('|')

                servant = Servant(
                    id=data_id,
                    name=data['NAME'],
                    name_jp=data['NAME_JP'],
                    name_en=data['NAME_EN'],
                    cls=Class.query.filter_by(name=data['CLASS']).one(),
                    star=data['STAR'],
                    cost=data['COST'] if data['COST'] else 0,
                    icon="http://file.fgowiki.fgowiki.com/fgo/head/%s.jpg" % str(data_id).zfill(3),
                    attribute=Attribute.query.filter_by(name=data['Camp']).one(),
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
                    hits_quick=data['QuiHit'] if data['QuiHit'] else 0,
                    hits_arts=data['ArtHit'] if data['ArtHit'] else 0,
                    hits_buster=data['BusHit'] if data['BusHit'] else 0,
                    hits_ex=data['EXHit'] if data['EXHit'] else 0,
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
                    growth_curve=data['Circle'] if data['Circle'] else 0,
                    np_name=np_name_zh,
                    np_name_en=np_name_en if np_name_en is not None else '',
                    np_rank=data['T_LEVEL'],
                    np_classification=data['T_TYPE'],
                    np_type=CommandType.query.filter_by(name=data['T_PROP']).one() if data['T_PROP'] != '' else None,
                    qp_stage1=int(qp_stage[0].replace('QP', '').replace(',', '')),
                    qp_stage2=int(qp_stage[1].replace('QP', '').replace(',', '')),
                    qp_stage3=int(qp_stage[2].replace('QP', '').replace(',', '')),
                    qp_stage4=int(qp_stage[3].replace('QP', '').replace(',', '')),
                    qp_skill2=int(qp_skill[0].replace('QP', '').replace(',', '')),
                    qp_skill3=int(qp_skill[1].replace('QP', '').replace(',', '')),
                    qp_skill4=int(qp_skill[2].replace('QP', '').replace(',', '')),
                    qp_skill5=int(qp_skill[3].replace('QP', '').replace(',', '')),
                    qp_skill6=int(qp_skill[4].replace('QP', '').replace(',', '')),
                    qp_skill7=int(qp_skill[5].replace('QP', '').replace(',', '')),
                    qp_skill8=int(qp_skill[6].replace('QP', '').replace(',', '')),
                    qp_skill9=int(qp_skill[7].replace('QP', '').replace(',', '')),
                    qp_skill10=int(qp_skill[8].replace('QP', '').replace(',', ''))
                )

                # 宝具效果
                np_effects = {
                    'effects': data['T_Text_Arr'].split('-'),
                    'lv': [v.split('|') for v in data['T_Num_Arr'].split('-')]
                }

                servant.np_effects = [
                    NpEffect(
                        effect=np_effects['effects'][i],
                        lv1=np_effects['lv'][i][0],
                        lv2=np_effects['lv'][i][1] if len(np_effects['lv'][i]) == 5 else np_effects['lv'][i][0],
                        lv3=np_effects['lv'][i][2] if len(np_effects['lv'][i]) == 5 else np_effects['lv'][i][0],
                        lv4=np_effects['lv'][i][3] if len(np_effects['lv'][i]) == 5 else np_effects['lv'][i][0],
                        lv5=np_effects['lv'][i][4] if len(np_effects['lv'][i]) == 5 else np_effects['lv'][i][0]
                    )
                    for i in range(0, min(len(np_effects['effects']), len(np_effects['lv'])))
                ]

                # 固有技能
                servant.active_skills = []

                sort = 1
                while True:
                    skill_name = data.get('SKILL_R%d' % sort, '')
                    skill_level = data.get('SKILL_L%d' % sort, '')
                    skill_cd = data.get('SKILL_C%d' % sort, '')
                    skill_icon = data.get('SKILL_P%d' % sort, '')
                    skill_effect = data.get('SKILL_E%d' % sort, '')
                    skill_lv = data.get('S%dLV' % sort, '')

                    if skill_name == skill_level == skill_cd == skill_icon == skill_effect == skill_lv == '':
                        break

                    active_skill = ActiveSkill(
                        name=skill_name,
                        level=skill_level,
                        cool_down=skill_cd,
                        icon='http://file.fgowiki.fgowiki.com/mobile/images/Skill/%s' % skill_icon,
                        sort=sort
                    )

                    skill_effects = {
                        'effects': skill_effect.split('&'),
                        'lv': [v.split('|') for v in skill_lv.split('-')]
                    }

                    active_skill.effects = [
                        SkillEffect(
                            effect=skill_effects['effects'][i],
                            lv1=skill_effects['lv'][i][0],
                            lv2=skill_effects['lv'][i][1] if len(skill_effects['lv'][i]) == 10 else skill_effects['lv'][i][0],
                            lv3=skill_effects['lv'][i][2] if len(skill_effects['lv'][i]) == 10 else skill_effects['lv'][i][0],
                            lv4=skill_effects['lv'][i][3] if len(skill_effects['lv'][i]) == 10 else skill_effects['lv'][i][0],
                            lv5=skill_effects['lv'][i][4] if len(skill_effects['lv'][i]) == 10 else skill_effects['lv'][i][0],
                            lv6=skill_effects['lv'][i][5] if len(skill_effects['lv'][i]) == 10 else skill_effects['lv'][i][0],
                            lv7=skill_effects['lv'][i][6] if len(skill_effects['lv'][i]) == 10 else skill_effects['lv'][i][0],
                            lv8=skill_effects['lv'][i][7] if len(skill_effects['lv'][i]) == 10 else skill_effects['lv'][i][0],
                            lv9=skill_effects['lv'][i][8] if len(skill_effects['lv'][i]) == 10 else skill_effects['lv'][i][0],
                            lv10=skill_effects['lv'][i][9] if len(skill_effects['lv'][i]) == 10 else skill_effects['lv'][i][0],
                            sort=i
                        )
                        for i in range(0, min(len(skill_effects['effects']), len(skill_effects['lv'])))
                    ]

                    servant.active_skills.append(active_skill)

                    sort += 1

                # 职介技能
                servant.passive_skills = []

                sort = 1
                while True:
                    skill_name = data.get('CSKILL_R%d' % sort, '')
                    skill_level = data.get('CSKILL_L%d' % sort, '')
                    skill_effect = data.get('CSKILL_E%d' % sort, '')
                    skill_icon = data.get('CSKILL_P%d' % sort, '')

                    if skill_name == skill_level == skill_effect == skill_icon == '':
                        break

                    servant.passive_skills.append(PassiveSkill(
                        name=skill_name,
                        level=skill_level,
                        effect=skill_effect,
                        icon='http://file.fgowiki.fgowiki.com/mobile/images/Skill/%s' % skill_icon,
                        sort=sort
                    ))

                    sort += 1

                db.session.add(servant)

                count += 1

                console_out("英灵--%s--编号%d：加载成功！" % (data['NAME'], data_id), console_file)

            db.session.commit()

            console_out('英灵数据加载完成，共加载了%d名英灵数据！' % count, console_file)

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
