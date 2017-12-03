from app import db


class CraftEssence(db.Model):
    """概念礼装"""
    __tablename__ = 'craft_essences'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    star = db.Column(db.SmallInteger, nullable=False)
    icon = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    atk = db.Column(db.Integer, nullable=False)
    max_atk = db.Column(db.Integer, nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    max_hp = db.Column(db.Integer, nullable=False)
    effect = db.Column(db.Text, nullable=False)
    max_effect = db.Column(db.Text, nullable=False)
    effect_icon = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    note = db.Column(db.Text, nullable=True, server_default=None)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP'))
    updated = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted = db.Column(db.TIMESTAMP, nullable=True, server_default=None)

    def __repr__(self):
        return '<%s%s %d: %s>' % (self.__class__.__name__, '(%s)' % self.__doc__ if self.__doc__ is not None else str(), self.id, self.name)
