from flask import Blueprint, render_template

mat = Blueprint('materials', __name__)

@mat.route("/materials")
def materials():
    return render_template('materials.html')