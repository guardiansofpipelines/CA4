from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)


# Create and configure MySQL database connection
db = mysql.connector.connect(
    host="db",       # Use the service name defined in Docker Compose
    port="3306",
    user="root",     # Assuming this is your MySQL root user
    password="1328", # Use the MySQL root password you've set in your DBDockerfile
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
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            print('Username already exists. Please choose a different one.', 'danger')
        else:
            # Create a new user and add them to the database
            hashed_password = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password, email) VALUES (%s, %s, %s)',
                           (username, hashed_password, 'email'))
            db.commit()

            print('Signup successful! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor()

        # Retrieve user from the database by username
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user_row = cursor.fetchone()

        if user_row and check_password_hash(user_row[2], password):  # Assuming password hash is in the third column
            user = User(user_row[0], user_row[1], user_row[2])

            # Store the user's ID in the session to track the login state
            
            print('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            print('Login failed. Check your username and password.', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
