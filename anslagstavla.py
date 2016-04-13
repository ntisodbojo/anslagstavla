from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/v1/busstop')
def busstop():
    return "10:11"

@app.route('/api/v1/menu')
def menu():
    return "{'huvudalternativ':'korv','Vehet':'curry'}"

@app.route('/api/v1/messages')
def messages():
    return "meddelanden"


if __name__ == '__main__':
    app.run(port=5005)
