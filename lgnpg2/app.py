from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# In-memory storage for demonstration purposes
users = {}

# Route for registration page
@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['userid']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        # Check if the passwords match
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))

        # Hash the password for security
        hashed_password = generate_password_hash(password)

        # Save the user data (for demo purposes, using in-memory storage)
        users[user_id] = hashed_password
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('register'))  # Redirect to the same page for demo

    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)
