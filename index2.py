from flask import Flask

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<User %s>" % self.name

#db.create_all()

#创建User对象并插入数据库
admin = User('admin')
db.session.add(admin)
db.session.commit()

#查询
users = User.query.all()

print(users)

