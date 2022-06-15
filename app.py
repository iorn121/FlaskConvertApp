from flask import Flask

test = Flask(__name__)


@test.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    test.run()
