from app import db


class NpEffect(db.Model):
    """宝具效果"""
    __tablename__ = 'np_effects'

    id = db.Column(db.Integer, primary_key=True)
    servant_id = db.Column(db.Integer, db.ForeignKey('servants.id'), nullable=False)
    effect = db.Column(db.Text, nullable=False)
    lv1 = db.Column(db.String(100), nullable=True)
    lv2 = db.Column(db.String(100), nullable=True)
    lv3 = db.Column(db.String(100), nullable=True)
    lv4 = db.Column(db.String(100), nullable=True)
    lv5 = db.Column(db.String(100), nullable=True)

    note = db.Column(db.Text, nullable=True, server_default=None)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP'))
    updated = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted = db.Column(db.TIMESTAMP, nullable=True, server_default=None)

    servant = db.relationship('Servant', backref='np_effects')

    def __repr__(self):
        return '<%s%s %d: %s>' % (self.__class__.__name__, '(%s)' % self.__doc__ if self.__doc__ is not None else str(), self.id, self.effect)
