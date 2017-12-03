from app import db


class Item(db.Model):
    """材料"""
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    note = db.Column(db.Text, nullable=True, server_default=None)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP'))
    updated = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted = db.Column(db.TIMESTAMP, nullable=True, server_default=None)

    def __repr__(self):
        return '<%s%s %d: %s>' % (self.__class__.__name__, '(%s)' % self.__doc__ if self.__doc__ is not None else str(), self.id, self.name)
