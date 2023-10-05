from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

# Create and configure MySQL database connection
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1328",
    database="myca4"
)

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor()

        # Check if the username already exists in the database
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            # Create a new user and add them to the database
            hashed_password = generate_password_hash(password)
            cursor.execute('INSERT INTO user (username, password) VALUES (%s, %s)',
                           (username, hashed_password))
            db.commit()

            flash('Signup successful! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor()

        # Retrieve user from the database by username
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        user_row = cursor.fetchone()

        if user_row and check_password_hash(user_row[2], password):  # Assuming password hash is in the third column
            user = User(*user_row)

            # Store the user's ID in the session to track the login state
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return 'Welcome to the Dashboard'
    else:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
