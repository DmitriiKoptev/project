from flask import Blueprint, render_template

ii = Blueprint('index_info', __name__)

@ii.route("/")
@ii.route("/index")
def index():
    return render_template('index.html')

@ii.route("/info")
def info():
    return render_template('info.html')