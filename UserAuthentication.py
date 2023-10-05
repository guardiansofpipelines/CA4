from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

# Replace the database-related code with user management logic

# Sample data structure to store user information (replace with a proper database)
users = []

class User:
    def __init__(self, username, password):
        self.id = len(users) + 1
        self.username = username
        self.password = generate_password_hash(password)

# Dummy data for testing (replace with actual database interactions)
users.append(User('user1', 'password1'))
users.append(User('user2', 'password2'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = next((user for user in users if user.username == username), None)

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            # Create a new user and add them to the user list (replace with database code)
            new_user = User(username, password)
            users.append(new_user)

            flash('Signup successful! You can now log in.', 'success')
            return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match (replace with database code)
        user = next((user for user in users if user.username == username), None)

        if user and check_password_hash(user.password, password):
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
