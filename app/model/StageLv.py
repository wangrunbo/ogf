from app import db


class StageLv(db.Model):
    """灵基再临材料"""
    __tablename__ = 'stage_lv'

    id = db.Column(db.Integer, primary_key=True)
    servant_id = db.Column(db.Integer, db.ForeignKey('servants.id'), nullable=False)
    stage = db.Column(db.SmallInteger, nullable=False)
    item = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    note = db.Column(db.Text, nullable=True, server_default=None)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP'))
    updated = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted = db.Column(db.TIMESTAMP, nullable=True, server_default=None)

    servant = db.relationship('Servant', backref='stage_lv')

    def __repr__(self):
        return '<%s%s %d: %s>' % (self.__class__.__name__, '(%s)' % self.__doc__ if self.__doc__ is not None else str(), self.id, '%s 阶段 %d' % (self.servant.name, self.stage))
