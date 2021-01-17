from flask import Flask, render_template

app = Flask(__name__)
# Secret key should be changed in the development
app.config['SECRET_KEY'] = 'gPo4xFh0KnZsUbf2cOXAC9RxdBA2VSEI'


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/logout/')
def logout():
    pass
