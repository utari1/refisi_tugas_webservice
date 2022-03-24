# kelas/nim/nama
# kelas/nim/nama

import os

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

# tulis command CURL utk request end point ini lengkap dengan data body jsonnya
@app.route("/api/v1/login", methods=["POST"])
def login():
  # request sesuai spec sbg data body bukan parameter lihat contoh book_ws.db
  # pada def create line 50 dan parsingnya line 51
  # cari kedalam db user username dan password
  # jika ketemu maka update kolom token ybs dengen random string
  # response kan sbb
  # body {"token": "randomsetringnyaaahh"}, http code: 200
 
@auth.verify_token
def verify_token(token):
  # ambil value token
  # cari ke dalam table user, 
  # return usernamenya

# tulis command line CURL utk request end point ini lengkap dengan data body jsonnya
@app.route("/api/v2/users/info", methods=["POST"])
@auth.login_required
def info()
  # response-kan {"username": auth.current_user()}, http code: 200



