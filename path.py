import os


DIR_NAME = {
    'APP': 'app',
    'TMP': 'tmp',
    'IMAGE': {
        'SERVANT_ICON': 'servant'
    }
}


ROOT = os.path.dirname(os.path.abspath(__file__))

APP = os.path.join(ROOT, DIR_NAME['APP'])

TMP = os.path.join(APP, DIR_NAME['TMP'])

STATIC = os.path.join(APP, 'static')

IMAGE = os.path.join(STATIC, 'img')

SERVANT_ICON = os.path.join(IMAGE, DIR_NAME['IMAGE']['SERVANT_ICON'])

if __name__ == '__main__':
    print(ROOT, APP)
