import time
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask_mail import Mail, Message

DBUSER = 'clooper'
DBPASS = '123456'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'clooper'


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'testing.flexsin@gmail.com'
app.config['MAIL_PASSWORD'] = 'Flexsin123!@#'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.secret_key = 'foobarbaz'

# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_PORT = 465
# MAIL_USE_TLS = False
# MAIL_USE_SSL = True
# MAIL_USERNAME = 'testing.flexsin@gmail.com'
# MAIL_PASSWORD = 'Flexsin123!@#'
# ADMINS = ['rubychauhanhstpl@gmail.com']


db = SQLAlchemy(app)


class users(db.Model):

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(64), index=True)
    first_name = db.Column(db.String(64), index=True)
    middle_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    lcountrycode = db.Column(db.Integer)
    landline = db.Column(db.Integer)
    mcountrycode = db.Column(db.Integer)
    mobile = db.Column(db.Integer)
    landlord = db.Column(db.Boolean, default=False)
    tenant = db.Column(db.Boolean, default=False)
    tradesperson = db.Column(db.Boolean, default=False)
    homeowner = db.Column(db.Boolean, default=False)
    postcode = db.Column(db.String(), index=True)
    age = db.Column(db.String(), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    photo = db.Column(db.LargeBinary)
    # age_range = db.Column(choices=AGE, default=1)
    heared_about_us = db.Column(db.String(), index=True)

    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'name': self.name,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
        }
        if include_email:
            data['email'] = self.email
        return data

    def __repr__(self):
        return '<User %r>' % self.name

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response

def bad_request(message):
    return error_response(400, message)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    print("data..",data)
    if  'first_name' not in data or 'email' not in data or 'password' not in data:
        return bad_request('Must include First Name, email and password fields')
    if users.query.filter_by(email=data['email']).first():
        return bad_request('This email already used.please use a different email address')
    name = data.get('first_name').strip().replace(" ", "") + ' ' + data.get('middle_name').strip().replace(" ","") + ' ' + data.get('last_name').strip().replace(" ", "")
    name = (re.sub(' +', ' ', name)).title()
    user_data = users( email=data.get('email'),
                      first_name=data.get('first_name'),
                      middle_name=data.get('middle_name'),
                      last_name=data.get('last_name'),
                      name=name,
                      lcountrycode=data.get('lcountrycode'),
                      landline=data.get('landline'),
                      mcountrycode=data.get('mcountrycode'),
                      mobile=data.get('mobile'),
                      landlord=data.get('landlord'),
                      tenant=data.get('tenant'),
                      tradesperson=data.get('tradesperson'),
                      homeowner=data.get('homeowner'),
                      postcode=data.get('postcode'),
                      age=data.get('age'),
                      # photo=data.get('photo'),
                      heared_about_us=data.get('heared_about_us'),
                      password_hash = generate_password_hash(data.get('password')))
    db.session.add(user_data)
    db.session.commit()
    msg = Message('Signup', sender=app.config['MAIL_USERNAME'], recipients=[data['email']])
    msg.body = 'Thank you for sign up and welcome to Clooper.'
    mail.send(msg)
    response = jsonify({"message":"Record successfully added"})
    response.status_code = 201
    return response

if __name__ == '__main__':
    dbstatus = False
    while dbstatus == False:
        try:
            print("$$ db create all $$$$")
            db.create_all()
        except:
            time.sleep(2)
        else:
            dbstatus = True
    app.run(debug=True, host='localhost')
