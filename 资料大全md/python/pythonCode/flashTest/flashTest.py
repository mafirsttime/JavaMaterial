from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route('/hello')
def hello_world1():
    return 'Hello mah!'

@app.route('/helloParam')
def hello_world1():
    return 'Hello mah!'


if __name__ == '__main__':
    app.run()



