from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
import pyrebase
import os
from src.manjulika import chatmanjulika

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set secret key for session


firebaseConfig={"apiKey": "AIzaSyCJw0mOOFOh6vxUeFp_a3w5SUOdOeS9eWY", "authDomain": "manjulikaai.firebaseapp.com", "databaseURL": "https://manjulikaai-default-rtdb.firebaseio.com", "projectId": "manjulikaai", "storageBucket": "manjulikaai.appspot.com", "messagingSenderId": "321800617494", "appId": "1:321800617494:web:8a831fe1611769baf4bf37", "measurementId": "G-EZVQ39H1EY"}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('chat'))  # If user is already logged in, redirect to chat page

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user  # Store user in session
            # Redirect to chat page upon successful login
            return redirect(url_for('chat'))
        except Exception as e:
            flash("Sign in failed: " + str(e), 'error')
            return redirect(url_for('home'))
    else:
        return "Invalid request method for this route"


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if 'user' in session:
        return redirect(url_for('chat'))  # If user is already logged in, redirect to chat page

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            auth.send_email_verification(user['idToken'])  # Send verification email
            db.child("users").child(name).set({"email": email, "chat_history": []})
            session['user'] = user  # Store user in session
            flash("Sign up successful. Verification email sent.", 'success')
            return redirect(url_for('chat'))  # Redirect to chat page after signup
        except Exception as e:
            flash("Sign up failed: " + str(e), 'error')
            return redirect(url_for('home'))
    else:
        return "Invalid request method for this route"


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if 'user' in session:
        return redirect(url_for('chat'))  # If user is already logged in, redirect to chat page

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


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user' not in session:
        flash("You must be logged in to access the chat.", 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        user_input = request.form['user_input']
        response = chatmanjulika(user_input)
        return response
    else:
        return render_template('chat.html')


if __name__ == '__main__':
    app.run(debug=True)
