from flask import Flask, render_template, request, redirect, flash, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Strong secret key for sessions

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nand1n1@5002",
    database="us"
)
cursor = db.cursor()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['userid']
        mobile_number = request.form['mobile_number']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        # Check if password and confirm password match
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))

        # Check if the user ID already exists
        query = "SELECT * FROM userss WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('User ID already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        # Hash the password for security
        hashed_password = generate_password_hash(password)

        query = "INSERT INTO userss (user_id, mobile_number, password) VALUES (%s, %s, %s)"
        values = (user_id, mobile_number, hashed_password)

        try:
            cursor.execute(query, values)
            db.commit()
            flash('Registration successful! You can now login.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['userid']
        password = request.form['password']

        # Fetch the hashed password from the database
        query = "SELECT password FROM userss WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()

        # Check if user exists and verify the password
        if user and check_password_hash(user[0], password):
            session['user_id'] = user_id
            flash(f"Welcome {user_id}!", 'success')
            return redirect(url_for('welcome'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/welcome')
def welcome():
    if 'user_id' in session:
        return render_template('welcome.html', user_id=session['user_id'])  # Pass user_id to the template
    else:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
