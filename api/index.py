from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/api/convert')
def converter():
    pass
    args = request.args
@app.route('/api/normalize')
def round():
    pass
    args = request.args
