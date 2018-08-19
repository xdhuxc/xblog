from flask import Flask

xapp = Flask(__name__)


@xapp.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    xapp.run()
