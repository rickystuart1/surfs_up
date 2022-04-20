#ctrl shift p to change interpreter to PythonData
from flask import Flask

app = Flask(__name__)

@app.route('/')

def hello_world():
    return 'Hello World'

