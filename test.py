from datetime import datetime, timedelta
import time

class Te:
    """aaa"""
    id = 1
    name = 'tas'

    def __repr__(self):
        return '<%s%s %d: %s>' % (
        self.__class__.__name__, f'({self.__doc__})' if self.__doc__ is not None else str(), self.id, self.name)

t = Te()
a = 1

print(f'Hello {a}')
