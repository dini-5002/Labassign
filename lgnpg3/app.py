from flask import Flask, render_template, request, redirect, flash, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os




app = Flask(__name__)
app.secret_key = os.urandom(24)  # Strong secret key for sessions
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
# Database connection setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nand1n1@5002",
    database="us"
)
cursor = db.cursor()

# Route for registration page
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

        # Insert user data into the MySQL database
        insert_query = "INSERT INTO userss (user_id, mobile_number, password) VALUES (%s, %s, %s)"
        values = (user_id, mobile_number, hashed_password)

        try:
            cursor.execute(insert_query, values)
            db.commit()
            flash('Registration successful! You can now login.', 'success')
            print("Data inserted successfully!")
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

# Route for login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['userid']
        password = request.form['password']

        # Query to select the hashed password for the user
        query = "SELECT password FROM userss WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()

        # Check if user exists and verify the password
        if user and check_password_hash(user[0], password):
            session['user_id'] = user_id
            flash(f"Welcome {user_id}!", 'success')
        else:
            flash('Invalid credentials, please try again.', 'danger')

    # Check if user is logged in to show welcome message
    logged_in = 'user_id' in session
    user_id = session.get('user_id', None)

    return render_template('login.html', logged_in=logged_in, user_id=user_id)


if __name__ == '__main__':
    app.run(debug=True)
