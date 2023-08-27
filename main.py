# Basic flask + p5.js server, using getting started examples from p5.js and flask

from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def home(name=None):
    return render_template('index.html', name=name)

if __name__ == '__main__':
    app.run(debug=True, port=8000)


