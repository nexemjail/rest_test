from flask import Flask


app = Flask(__name__)

users = {
    'allah': 'jesus',
    'jesus': 'god',
}


@app.route('/')
def index():
    return 'Allah'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9000')