from flaskApp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Headmen.query.get(int(user_id))

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    works = db.Column(db.Integer, nullable=False)
    group = db.Column(db.Integer, nullable=False)
    subject =  db.Column(db.String(64), nullable=False)
    priority =  db.Column(db.Integer)

    def __repr__(self):
        return f"Student({self.username}, {self.group})"

class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(64), nullable=False)
    string = db.Column(db.String(64), nullable=False)
    groups = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"Subject {self.string}"
    
class Headmen(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"Headman {self.username}"