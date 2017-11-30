import os


ROOT = os.path.dirname(os.path.abspath(__file__))

APP = os.path.join(ROOT, 'app')

TMP = os.path.join(APP, 'tmp')


if __name__ == '__main__':
    print(ROOT, APP)
