from app import db
from .SkillEffect import SkillEffect


class ActiveSkill(db.Model):
    """固有技能"""
    __tablename__ = 'active_skills'

    id = db.Column(db.Integer, primary_key=True)
    servant_id = db.Column(db.Integer, db.ForeignKey('servants.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(10), nullable=False)  # 固有等级
    cool_down = db.Column(db.Integer, nullable=False)
    icon = db.Column(db.String(255), nullable=False)
    sort = db.Column(db.SmallInteger, nullable=False)

    note = db.Column(db.Text, nullable=True, server_default=None)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP'))
    updated = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted = db.Column(db.TIMESTAMP, nullable=True, server_default=None)

    servant = db.relationship('Servant', backref='active_skills')

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

        for sort, active_skill_data in enumerate(data, start=1):
            if active_skill_data['id'] is None:
                active_skill = cls(servant_id=servant_id)

                if not multiple:
                    active_skill.sort = cls.next_sort(servant_id)
            else:
                active_skill = cls.query.get_or_404(active_skill_data['id'])

            if 'name' in active_skill_data:
                active_skill.name = active_skill_data['name']

            if 'level' in active_skill_data:
                active_skill.level = active_skill_data['level']

            if 'cool_down' in active_skill_data:
                active_skill.cool_down = active_skill_data['cool_down']

            if 'icon' in active_skill_data:
                active_skill.icon = active_skill_data['icon']

            if multiple:
                active_skill.sort = sort

            if 'effects' in active_skill_data:
                for sort, skill_effect_data in enumerate(active_skill_data['effects'], start=1):
                    if skill_effect_data['id'] is None:
                        skill_effect = SkillEffect(active_skill=active_skill)

                        if len(active_skill_data['effects']) == 1:
                            skill_effect.sort = SkillEffect.next_sort(active_skill)
                    else:
                        skill_effect = SkillEffect.query.get_or_404()

                    skill_effect.effect = skill_effect_data['skill']
                    skill_effect.lv1 = skill_effect_data['lv1']
                    skill_effect.lv2 = skill_effect_data['lv2']
                    skill_effect.lv3 = skill_effect_data['lv3']
                    skill_effect.lv4 = skill_effect_data['lv4']
                    skill_effect.lv5 = skill_effect_data['lv5']
                    skill_effect.lv6 = skill_effect_data['lv6']
                    skill_effect.lv7 = skill_effect_data['lv7']
                    skill_effect.lv8 = skill_effect_data['lv8']
                    skill_effect.lv9 = skill_effect_data['lv9']
                    skill_effect.lv10 = skill_effect_data['lv10']

                    if len(active_skill_data['effects']) > 1:
                        skill_effect.sort = sort

                    db.session.add(skill_effect)

            db.session.add(active_skill)

        db.session.commit()
