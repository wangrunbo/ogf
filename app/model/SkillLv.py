from app import db


class SkillLv(db.Model):
    """技能升级材料"""
    __tablename__ = 'skill_lv'

    id = db.Column(db.Integer, primary_key=True)
    servant_id = db.Column(db.Integer, db.ForeignKey('servants.id'), nullable=False)
    level = db.Column(db.SmallInteger, nullable=False)
    item = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    note = db.Column(db.Text, nullable=True, server_default=None)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP'))
    updated = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted = db.Column(db.TIMESTAMP, nullable=True, server_default=None)

    servant = db.relationship('Servant', backref='skill_lv')

    def __repr__(self):
        return '<%s%s %d: %s>' % (self.__class__.__name__, f'({self.__doc__})' if self.__doc__ is not None else str(), self.id, f'{self.servant.name} Lv {self.level}')
