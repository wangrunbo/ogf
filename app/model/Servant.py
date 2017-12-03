from app import db


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
    qp_stage1 = db.Column(db.Integer, nullable=False)
    qp_stage2 = db.Column(db.Integer, nullable=False)
    qp_stage3 = db.Column(db.Integer, nullable=False)
    qp_stage4 = db.Column(db.Integer, nullable=False)
    qp_skill2 = db.Column(db.Integer, nullable=False)
    qp_skill3 = db.Column(db.Integer, nullable=False)
    qp_skill4 = db.Column(db.Integer, nullable=False)
    qp_skill5 = db.Column(db.Integer, nullable=False)
    qp_skill6 = db.Column(db.Integer, nullable=False)
    qp_skill7 = db.Column(db.Integer, nullable=False)
    qp_skill8 = db.Column(db.Integer, nullable=False)
    qp_skill9 = db.Column(db.Integer, nullable=False)
    qp_skill10 = db.Column(db.Integer, nullable=False)
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
