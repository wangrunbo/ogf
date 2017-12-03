from app import db


class SkillEffect(db.Model):
    """固有技能效果"""
    __tablename__ = 'skill_effects'

    id = db.Column(db.Integer, primary_key=True)
    active_skill_id = db.Column(db.Integer, db.ForeignKey('active_skills.id'), nullable=False)
    effect = db.Column(db.Text, nullable=False)
    lv1 = db.Column(db.String(10), nullable=True)
    lv2 = db.Column(db.String(10), nullable=True)
    lv3 = db.Column(db.String(10), nullable=True)
    lv4 = db.Column(db.String(10), nullable=True)
    lv5 = db.Column(db.String(10), nullable=True)
    lv6 = db.Column(db.String(10), nullable=True)
    lv7= db.Column(db.String(10), nullable=True)
    lv8 = db.Column(db.String(10), nullable=True)
    lv9 = db.Column(db.String(10), nullable=True)
    lv10 = db.Column(db.String(10), nullable=True)
    sort = db.Column(db.SmallInteger, nullable=False)

    note = db.Column(db.Text, nullable=True, server_default=None)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP'))
    updated = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted = db.Column(db.TIMESTAMP, nullable=True, server_default=None)

    skill = db.relationship('ActiveSkill', backref='effects')

    def __repr__(self):
        return '<%s%s %d: %s>' % (self.__class__.__name__, '(%s)' % self.__doc__ if self.__doc__ is not None else str(), self.id, self.effect)
