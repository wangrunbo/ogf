from app import db


class PassiveSkill(db.Model):
    """职介技能"""
    __tablename__ = 'passive_skills'

    id = db.Column(db.Integer, primary_key=True)
    servant_id = db.Column(db.Integer, db.ForeignKey('servants.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(10), nullable=False)  # 固有等级
    effect = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(255), nullable=False)
    sort = db.Column(db.SmallInteger, nullable=False)

    note = db.Column(db.Text, nullable=True, server_default=None)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP'))
    updated = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted = db.Column(db.TIMESTAMP, nullable=True, server_default=None)

    servant = db.relationship('Servant', backref='passive_skills')

    def __repr__(self):
        return '<%s%s %d: %s>' % (self.__class__.__name__, '(%s)' % self.__doc__ if self.__doc__ is not None else str(), self.id, self.name)

    @classmethod
    def next_sort(cls, servant_id):
        return cls.query.filter_by(servant_id=servant_id).count() + 1

    @staticmethod
    def validate(data):
        """
        输入数据验证
        :param dict|list data:
        :return: bool, dict
        """
        is_valid = True
        errors = {}

        return is_valid, errors

    @classmethod
    def edit(cls, data, servant_id):
        """

        :param dict|list  data:
        :param servant_id:
        :return:
        """
        multiple = type(data) is list

        if not multiple:
            data = [data]

        for sort, passive_skill_data in enumerate(data, start=1):
            if passive_skill_data['id'] is None:
                passive_skill = cls(servant_id=servant_id)

                if not multiple:
                    passive_skill.sort = cls.next_sort(servant_id)
            else:
                passive_skill = cls.query.get_or_404(passive_skill_data['id'])

            if 'name' in passive_skill_data:
                passive_skill.name = passive_skill_data['name']

            if 'level' in passive_skill_data:
                passive_skill.level = passive_skill_data['level']

            if 'effect' in passive_skill_data:
                passive_skill.cool_down = passive_skill_data['effect']

            if 'icon' in passive_skill_data:
                passive_skill.icon = passive_skill_data['icon']

            if multiple:
                passive_skill.sort = sort

            db.session.add(passive_skill)

        db.session.commit()
