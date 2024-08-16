from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
import pyrebase
import os
from datetime import datetime
from src.manjulika import chatmanjulika
from src.doraemon import chatdoraemon
from dotenv import load_dotenv
import json
import re

load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24)  


firebaseConfig=json.loads(os.getenv("FirebaseConfig"))
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('welcome'))  

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user  
            return redirect(url_for('welcome'))
        except Exception as e:
            flash("Sign in failed: " + str(e), 'error')
            return redirect(url_for('home'))
    else:
        return "Invalid request method for this route"


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if 'user' in session:
        return redirect(url_for('welcome'))  # If user is already logged in, redirect to chat page

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            auth.send_email_verification(user['idToken'])  # Send verification email
            db.child("users").child(name).set({"email": email, "chat_history": []})
            session['user'] = user  
            flash("Sign up successful. Verification email sent.", 'success')
            return redirect(url_for('welcome'))  
        except Exception as e:
            flash("Sign up failed: " + str(e), 'error')
            return redirect(url_for('home'))
    else:
        return "Invalid request method for this route"



@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if 'user' in session:
        return redirect(url_for('welcome'))  

    if request.method == "POST":
        email = request.form['email']
        try:
            auth.send_password_reset_email(email)
            flash("Password reset email sent. Please check your email inbox.", 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash("Failed to send password reset email: " + str(e), 'error')
            return redirect(url_for('forgot_password'))
    else:
        return render_template('resetpwd.html')
    

def sanitize_email(email):
  
    return re.sub(r'[@\.#$\[\]]', '_', email)

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html')

@app.route('/manjulika', methods=['GET', 'POST'])
def manjulika():
    if 'user' not in session:
        flash("You must be logged in to access the chat.", 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        user_input = request.form['user_input']
        response = chatmanjulika(user_input)
        user_email = session['user']['email']
        sanitized_email = sanitize_email(user_email)

        db.child("manjulikachat").child(sanitized_email).child("conversations").push({
            "user_email": user_email,
            "user_input": user_input,
            "manjulika_response": response,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        return response
    else:
        return render_template('chat.html')

@app.route('/doraemon', methods=['GET', 'POST'])
def doraemon():
    if 'user' not in session:
        flash("You must be logged in to access the chat.", 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        user_input = request.form['user_input']
        response = chatdoraemon(user_input)
        user_email = session['user']['email']
        sanitized_email = sanitize_email(user_email)

        db.child("doraemonchat").child(sanitized_email).child("conversations").push({
            "user_email": user_email,
            "user_input": user_input,
            "manjulika_response": response,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        return response
    else:
        return render_template('chat2.html')



if __name__ == '__main__':
    app.run(debug=True)