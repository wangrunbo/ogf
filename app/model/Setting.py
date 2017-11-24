import json
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from app import db
from .ValueType import ValueType


class Setting(db.Model):
    """定数"""
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), nullable=False, unique=True)
    value_type_id = db.Column(db.SmallInteger, db.ForeignKey('value_types.id'), nullable=False)
    _value = db.Column('value', db.Text, nullable=True, server_default=None)
    comment = db.Column(db.Text, nullable=False)

    note = db.Column(db.Text, nullable=True, server_default=None)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP'))
    updated = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted = db.Column(db.TIMESTAMP, nullable=True, server_default=None)

    type = db.relationship('ValueType', backref='settings')

    def __init__(self, key, value, value_type_id=None, comment=''):
        self.key = key
        self.value = value
        if value_type_id is not None:
            self.value_type_id = value_type_id
        self.comment = comment

    def __repr__(self):
        return '<%s%s %d: %s>' % (self.__class__.__name__, f'({self.__doc__})' if self.__doc__ is not None else str(), self.id, self.key)

    @hybrid_property
    def value(self):
        if self._value is None:
            value = None
        elif self.value_type_id == ValueType.NUM:
            try:
                value = int(self._value)
            except ValueError:
                value = float(self._value)
        elif self.value_type_id == ValueType.BOOL:
            value = bool(self._value)
        elif self.value_type_id == ValueType.DATETIME:
            value = datetime.strptime(self._value, '%Y-%m-%d %H:%M:%S')
        elif self.value_type_id == ValueType.LIST or self.value_type_id == ValueType.DICT:
            value = json.loads(self._value)
        else:
            value = self._value

        return value

    @value.setter
    def value(self, value):
        value_type = type(value)
        if value_type is int or value_type is float:
            self.value_type_id = ValueType.NUM
            self._value = str(value)
        elif value_type is str:
            self.value_type_id = ValueType.STRING
            self._value = str(value)
        elif value_type is bool:
            self.value_type_id = ValueType.BOOL
            self._value = str(value)
        elif value_type is datetime:
            self.value_type_id = ValueType.DATETIME
            self._value = value.strftime('%Y-%m-%d %H:%M:%S')
        elif value_type is list:
            self.value_type_id = ValueType.LIST
            self._value = json.dumps(value)
        elif value_type is dict:
            self.value_type_id = ValueType.DICT
            self._value = json.dumps(value)
        else:
            self._value = None

    @staticmethod
    def get(var):
        return Setting.query.filter_by(key=var).one().value
