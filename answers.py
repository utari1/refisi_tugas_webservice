# kelas/nim/nama
# kelas/nim/nama

import os, random, string

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify
import json 
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import QueryableAttribute

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "user.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme='Bearer')

class User(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    token = db.Column(db.String(225), unique=True, nullable=True, primary_key=False)
    #db.create_all()

#curl -i http://127.0.0.1:7001/addUser -X POST -H 'Content-Type: application/json' -d '{"username":"nim", "password":123}'
@app.route("/addUser", methods=["POST"])
def add_user():
  username = request.json['username']
  password = request.json['password']

  newUsers = User(username=username, password=password)
  db.session.add(newUsers)
  db.session.commit() 
  return jsonify({
    'msg': 'berhasil tambah user',
    'username': username,
    'password' : password,
    'status': 200 
    })

#curl -i http://127.0.0.1:7001/api/v1/login -X POST -H 'Content-Type: application/json' -d '{"username":"19090051", "password": "123"}'
#curl -i http://127.0.0.1:7001/api/v1/login -X POST -H 'Content-Type: application/json' -d '{"username":"19090089", "password": "123"}'
@app.route("/api/v1/login", methods=["POST"])
def login():
  username = request.json['username']
  password = request.json['password']

  user = User.query.filter_by(username=username, password=password).first()

  if user:
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    User.query.filter_by(username=username, password=password).update({'token': token})
    db.session.commit()

    return jsonify({
      'msg': 'Login berhasil',
      'username': username,
      'token': token,
      'status': 200 
      })

  else:
    return jsonify({
      'msg': 'Login gagal',
      'status': 401,
      })

#curl -i http://127.0.0.1:7001/api/v2/users/info -X POST -H 'Content-Type: application/json'
@app.route("/api/v2/users/info", methods=["POST"])
def info():
  token = request.values.get('token')
  user = User.query.filter_by(token=token).first()
  if user:
      return jsonify({
        'msg': 'get data user berhasil',
        'username': user.username,
        'status': 200
        })
  else:
      return jsonify({
        'msg': 'token salah'
        })

if __name__ == '__main__':
   app.run(debug = True, port=7001)