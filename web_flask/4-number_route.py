#!/usr/bin/python3
"""
Script that starts a Flask web app with routes:
>>  '/' | '/hbnb' | '/c/<text>' | '/python/<text>' | '/number/<n>'
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Displays 'Hello HBNB!'"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Displays 'HBNB'"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_is_no_joke(text):
    """Displays 'C' followed by the value of the text variable"""
    return "C {}".format(' '.join(text.split('_')))


@app.route('/python/', defaults={'text': 'is cool'})
@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text):
    """Displays 'Python' followed by the value of the text variable"""
    return "Python {}".format(' '.join(text.split('_')))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Displays 'n is a number' only if n is an integer"""
    return "{} is a number".format(n)


if __name__ == '__main__':
    app.run()
