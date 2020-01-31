from flask import Flask, redirect, url_for, jsonify, request, render_template, session
from flask_pymongo import PyMongo

import smtplib
from email.message import EmailMessage
import bcrypt
import random as rnd
import re


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/general_db'
app.secret_key = 'SomethingKey'
mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def main_page():
    return render_template('main_page.html')

@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    return render_template('login_page.html')

@app.route('/logout_page', methods=['GET'])
def logout_page():
    session.clear()
    return redirect(url_for('main_page'))

@app.route('/register_page', methods=['GET', 'POST'])
def register_page():
    return render_template('register_page.html')

@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        form_data = request.form
        user_name = (form_data['name'])
        user_email = (form_data["email"])
        user_pass = (form_data["passcode"])
        user_auth = False
        if user_name and user_email and user_pass:
            user_pass = user_pass.encode('utf-8')
            salt = bcrypt.gensalt(5)
            hashed = bcrypt.hashpw(user_pass, salt)
            authenticate = ''
            signs = '1234567890'
            while len(authenticate) < 4:
                authenticate += signs[rnd.randint(0, len(signs) - 1)]
            try:
                email_from = 'somevalue'
                email_pass = 'somevalue'
                email_to = 'somevalue'
                message = EmailMessage()
                message['Subject'] = f'Welcome to Learnguage'
                message['From'] = f'{email_from}'
                message['To'] = f'{email_to}'
                message.set_content(f'''
Hello, {user_name}. Welcome to our service !
Please authenticate your account with this code:
                   {authenticate}
                ''')
                server = smtplib.SMTP('smtp.office365.com', 25)
                server.connect('smtp.office365.com', 587)
                server.starttls()
                server.login(email_from, email_pass)
                server.send_message(message)
                server.quit()

                new_user = mongo.db.general_db.insert({'name': user_name, 'email': user_email, 'password': hashed,\
                                                       'authorized': user_auth, 'auth_code': authenticate})
                session['username'] = user_name
            except Exception:
                return render_template('error_page.html', error_code='registration')
            finally:
                return redirect(url_for('main_page'))
        else:
            return 'Oops something went wrong'
    else:
        return 'Oops something went wrong'

if __name__ == '__main__':
    app.run('127.0.0.1', 8333, debug=True)