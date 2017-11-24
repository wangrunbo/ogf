import sys
import re
import requests
import json
from ..models import Class
from ..models import Attribute
from ..models import Gender
from ..models import CommandType
from ..models import Servant

commends = ['master', 'servant']

catch = sys.argv[1]

if catch == 'master':
    print('系统启动，开始加载基础信息...')

    # 职介信息
    print('职介信息开始加载...')

    data = ['Saber', 'Lancer', 'Archer', 'Rider', 'Caster', 'Assassin', 'Berserker', 'Avenger', 'Ruler', 'Shielder', 'Beast', 'Alterego', 'MoonCancer']

    sort = 0
    for name in iter(data):
        sort += 1
        Class(name=name, sort=sort)

        print(f'职介--{name}--加载完成！')

    print('职介信息加载完成！')

    # 阵营信息
    print('阵营信息开始加载...')

    data = ['天', '地', '人', '星', '兽']

    sort = 0
    for name in iter(data):
        sort += 1
        Class(name=name, sort=sort)

        print(f'阵营--{name}--加载完成！')

    print('阵营信息加载完成！')

    # 性别信息
    print('性别信息开始加载...')

    data = ['男性', '女性', '?', '-']

    sort = 0
    for name in iter(data):
        sort += 1
        Class(name=name, sort=sort)

        print(f'性别--{name}--加载完成！')

    print('性别信息加载完成！')

    # 指令卡信息
    print('指令卡信息开始加载...')

    data = ['Quick', 'Arts', 'Buster']

    sort = 0
    for name in iter(data):
        sort += 1
        Class(name=name, sort=sort)

        print(f'指令卡--{name}--加载完成！')

    print('指令卡信息加载完成！')

    print('基础信息加载完成，系统中止！')

elif catch == 'servant':
    print('系统启动，开始加载英灵数据...')

    url = 'http://fgowiki.com/guide/petdetail/%d'

    servant_id = 0
    while True:
        servant_id += 1

        print(f"英灵编号{servant_id}：开始加载...")

        html = requests.get(url=url % servant_id).content.decode('utf-8')

        try:
            data = re.search(r'^var datadetail = (\[.*?\]);$', html, re.M).group(1)
            data = json.loads(data, encoding='utf-8')[0]
        except AttributeError:
            print(f"英灵编号{servant_id}未找到，数据加载完成，共加载了{servant_id - 1}名英灵数据。")
            break

        # 性别
        if data['GENDER'] == '男性' or data['GENDER'] == '男性':
            gender = Gender.objects.get(name=data['GENDER'])
        elif re.search(r'\?', data['GENDER']):
            gender = Gender.objects.get(id=Gender.UNKNOWN)
        else:
            gender = Gender.objects.get(id=Gender.SKIP)

        # 宝具名
        np_name = re.match(r'^(.+?)(\(.+\))$', data['T_NAME'])
        np_name_zh = np_name.group(1)
        np_name_en = np_name.group(2)

        Servant(
            id=servant_id,
            name=data['NAME'],
            name_jp=data['NAME_JP'],
            name_en=data['NAME_EN'],
            classify=Class.objects.get(name=data['CLASS']),
            star=data['STAR'],
            cost=data['COST'],
            icon=f"http://file.fgowiki.fgowiki.com/fgo/head/{str(servant_id).zfill(3)}.jpg",
            attribute=Attribute.objects.get(name=data['CAMP']),
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
            np_type=CommandType.objects.get(name=data['T_PROP'])
        ).save()

        print(f"英灵--{data['NAME']}--编号{servant_id}：加载成功！")

else:
    print('指令未识别，请参考执行以下命令：')
    for commend in iter(commends):
        print(f' --{commend}\n')
