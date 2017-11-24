from sqlalchemy import desc
from app import db


class Class(db.Model):
    """职介"""
    __tablename__ = 'class'

    Saber = 1
    Lancer = 2
    Archer = 3
    Rider = 4
    Caster = 5
    Assassin = 6
    Berserker = 7
    Avenger = 8
    Ruler = 9
    Shielder = 10
    Beast = 11
    Alterego = 12
    MoonCancer = 13

    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    sort = db.Column(db.Integer, nullable=False, unique=True)

    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP'))
    updated = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted = db.Column(db.TIMESTAMP, nullable=True, server_default=None)

    def __init__(self, name):
        self.name = name
        self.sort = self.last_sort + 1

    def __repr__(self):
        return '<%s%s %d: %s>' % (self.__class__.__name__, f'({self.__doc__})' if self.__doc__ is not None else str(), self.id, self.name)

    @property
    def last_sort(self):
        entity = self.__class__.query.order_by(desc('sort')).first()

        if entity:
            return entity.sort
        else:
            return 0
