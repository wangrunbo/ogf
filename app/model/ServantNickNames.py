from app import db


class ServantNickName(db.Model):
    """固有技能"""
    __tablename__ = 'servant_nick_names'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    servant_id = db.Column(db.Integer, db.ForeignKey('servants.id'), nullable=False)

    note = db.Column(db.Text, nullable=True, server_default=None)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP'))
    updated = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted = db.Column(db.TIMESTAMP, nullable=True, server_default=None)

    servant = db.relationship('Servant', backref='nick_names')

    def __repr__(self):
        return '<%s%s %d: %s>' % (self.__class__.__name__, f'({self.__doc__})' if self.__doc__ is not None else str(), self.id, self.name)
