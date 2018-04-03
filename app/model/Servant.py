from app import db
from .StageLv import StageLv
from .SkillLv import SkillLv


class Servant(db.Model):
    """英灵"""
    __tablename__ = 'servants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_jp = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(150), nullable=False)
    class_id = db.Column(db.SmallInteger, db.ForeignKey('class.id'), nullable=False)
    star = db.Column(db.SmallInteger, nullable=False)
    cost = db.Column(db.SmallInteger, nullable=False)
    icon = db.Column(db.String(255), nullable=False)
    attribute_id = db.Column(db.SmallInteger, db.ForeignKey('attributes.id'), nullable=False)
    atk = db.Column(db.Integer, nullable=False)
    max_atk = db.Column(db.Integer, nullable=False)
    atk_90 = db.Column(db.Integer, nullable=False)
    atk_100 = db.Column(db.Integer, nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    max_hp = db.Column(db.Integer, nullable=False)
    hp_90 = db.Column(db.Integer, nullable=False)
    hp_100 = db.Column(db.Integer, nullable=False)
    quick = db.Column(db.SmallInteger, nullable=False)  # Quick卡数
    arts = db.Column(db.SmallInteger, nullable=False)  # Arts卡数
    buster = db.Column(db.SmallInteger, nullable=False)  # Buster卡数
    hits_quick = db.Column(db.SmallInteger, nullable=False)
    hits_arts = db.Column(db.SmallInteger, nullable=False)
    hits_buster = db.Column(db.SmallInteger, nullable=False)
    hits_ex = db.Column(db.SmallInteger, nullable=False)
    # hits_np = db.Column(db.SmallInteger, nullable=False)
    illustrator = db.Column(db.String(100), nullable=False)  # 画师
    cv = db.Column(db.String(100), nullable=False)
    alignment = db.Column(db.String(10), nullable=False)  # 属性
    gender_id = db.Column(db.SmallInteger, db.ForeignKey('genders.id'), nullable=False)  # 性别
    region = db.Column(db.String(30), nullable=False)  # 地域
    height = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.String(100), nullable=False)
    crit_generation = db.Column(db.String(30), nullable=False)  # 掉星率
    death_rate = db.Column(db.String(30), nullable=False)  # 即死率
    crit_absorption = db.Column(db.String(30), nullable=False)  # 暴击权重
    np_charge_quick = db.Column(db.String(30), nullable=False)  # NP获取率(Quick)
    np_charge_arts = db.Column(db.String(30), nullable=False)  # NP获取率(Arts)
    np_charge_buster = db.Column(db.String(30), nullable=False)  # NP获取率(Buster)
    np_charge_ex = db.Column(db.String(30), nullable=False)  # NP获取率(EX)
    np_charge_np = db.Column(db.String(30), nullable=False)  # NP获取率(宝具)
    np_charge_def = db.Column(db.String(30), nullable=False)  # NP获取率(防御)
    origin = db.Column(db.String(100), nullable=False)
    growth_curve = db.Column(db.Integer, nullable=False)
    np_name = db.Column(db.String(100), nullable=False)  # 宝具名
    # np_name_jp = db.Column(db.String(100), nullable=False)  # 宝具名(日文)
    np_name_en = db.Column(db.String(200), nullable=False)
    np_rank = db.Column(db.String(30), nullable=False)  # 宝具等级
    np_classification = db.Column(db.String(30), nullable=False)  # 宝具类型
    np_type_id = db.Column(db.SmallInteger, db.ForeignKey('command_types.id'), nullable=True)  # 宝具卡色
    qp_stage1 = db.Column(db.Integer, nullable=False, server_default='0')
    qp_stage2 = db.Column(db.Integer, nullable=False, server_default='0')
    qp_stage3 = db.Column(db.Integer, nullable=False, server_default='0')
    qp_stage4 = db.Column(db.Integer, nullable=False, server_default='0')
    qp_skill2 = db.Column(db.Integer, nullable=False, server_default='0')
    qp_skill3 = db.Column(db.Integer, nullable=False, server_default='0')
    qp_skill4 = db.Column(db.Integer, nullable=False, server_default='0')
    qp_skill5 = db.Column(db.Integer, nullable=False, server_default='0')
    qp_skill6 = db.Column(db.Integer, nullable=False, server_default='0')
    qp_skill7 = db.Column(db.Integer, nullable=False, server_default='0')
    qp_skill8 = db.Column(db.Integer, nullable=False, server_default='0')
    qp_skill9 = db.Column(db.Integer, nullable=False, server_default='0')
    qp_skill10 = db.Column(db.Integer, nullable=False, server_default='0')
    note = db.Column(db.Text, nullable=True, server_default=None)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP'))
    updated = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted = db.Column(db.TIMESTAMP, nullable=True, server_default=None)

    cls = db.relationship('Class', backref='servants')
    attribute = db.relationship('Attribute', backref='servants')
    gender = db.relationship('Gender', backref='servants')
    np_type = db.relationship('CommandType', backref='typed_np_servants')

    def __repr__(self):
        return '<%s%s %d: %s>' % (self.__class__.__name__, '(%s)' % self.__doc__ if self.__doc__ is not None else str(), self.id, self.name)

    @property
    def stage_completed(self):
        """
        灵基再临资料登录完成数
        :return: int
        """
        completed = 0

        for stage in range(1, 5):
            if StageLv.query.filter_by(servant=self, stage=stage).count() > 0:
                completed += 1

        return completed

    @property
    def skill_completed(self):
        """
        技能升级资料登录完成数
        :return: int
        """
        completed = 0

        for level in range(2, 10):
            if SkillLv.query.filter_by(servant=self, level=level).count() > 0:
                completed += 1

        return completed

    @staticmethod
    def validate(data):
        """
        输入数据验证
        :param dict data:
        :return: bool, dict
        """
        is_valid = True
        errors = {}

        return is_valid, errors
    
    def edit(self, data):
        """
        基本信息更新
        :param dict data: 
        :return: self
        """
        if 'name' in data:
            self.name = data['name']

        if 'name_jp' in data:
            self.name_jp = data['name_jp']

        if 'name_en' in data:
            self.name_en = data['name_en']

        if 'class_id' in data:
            self.class_id = data['class_id']

        if 'star' in data:
            self.star = data['star']

        if 'cost' in data:
            self.cost = data['cost']

        if 'attribute_id' in data:
            self.attribute_id = data['attribute_id']

        if 'atk' in data:
            self.atk = data['atk']

        if 'max_atk' in data:
            self.max_atk = data['max_atk']

        if 'atk_90' in data:
            self.atk_90 = data['atk_90']

        if 'atk_100' in data:
            self.atk_100 = data['atk_100']

        if 'hp' in data:
            self.hp = data['hp']

        if 'max_hp' in data:
            self.max_hp = data['max_hp']

        if 'hp_90' in data:
            self.hp_90 = data['hp_90']

        if 'hp_100' in data:
            self.hp_100 = data['hp_100']

        if 'quick' in data:
            self.quick = data['quick']

        if 'arts' in data:
            self.arts = data['arts']

        if 'buster' in data:
            self.buster = data['buster']

        if 'hits_quick' in data:
            self.hits_quick = data['hits_quick']

        if 'hits_arts' in data:
            self.hits_arts = data['hits_arts']

        if 'hits_buster' in data:
            self.hits_buster = data['hits_buster']

        if 'hits_ex' in data:
            self.hits_ex = data['hits_ex']

        if 'illustrator' in data:
            self.illustrator = data['illustrator']

        if 'cv' in data:
            self.cv = data['cv']

        if 'alignment' in data:
            self.alignment = data['alignment']

        if 'gender_id' in data:
            self.gender_id = data['gender_id']

        if 'region' in data:
            self.region = data['region']

        if 'height' in data:
            self.height = data['height']

        if 'weight' in data:
            self.weight = data['weight']

        if 'crit_generation' in data:
            self.crit_generation = data['crit_generation']

        if 'death_rate' in data:
            self.death_rate = data['death_rate']

        if 'crit_absorption' in data:
            self.crit_absorption = data['crit_absorption']

        if 'np_charge_quick' in data:
            self.np_charge_quick = data['np_charge_quick']

        if 'np_charge_arts' in data:
            self.np_charge_arts = data['np_charge_arts']

        if 'np_charge_buster' in data:
            self.np_charge_buster = data['np_charge_buster']

        if 'np_charge_ex' in data:
            self.np_charge_ex = data['np_charge_ex']

        if 'np_charge_np' in data:
            self.np_charge_np = data['np_charge_np']

        if 'np_charge_def' in data:
            self.np_charge_def = data['np_charge_def']

        if 'origin' in data:
            self.origin = data['origin']

        if 'growth_curve' in data:
            self.growth_curve = data['growth_curve']

        db.session.add(self)
        db.session.commit()

        return self
