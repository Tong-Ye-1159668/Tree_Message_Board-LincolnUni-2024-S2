from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
from flask_hashing import Hashing
import re
from datetime import datetime
from datetime import date
from datetime import timedelta
import mysql.connector
from mysql.connector import FieldType
import connect

# Configuration and constants
app = Flask(__name__)
app.secret_key = 'KEXq3sLJCV'
hashing = Hashing(app)
PASSWORD_SALT = 'KsVUyGzItjo4kCg'

UPLOAD_FOLDER = 'static/profile_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db_connection = None

def getCursor():
    """Gets a new dictionary cursor for the database.
    
    If necessary, a new database connection will be created here and used for all
    subsequent calls to getCursor()."""
    global db_connection

    if db_connection is None or not db_connection.is_connected():
        db_connection = mysql.connector.connect(user=connect.dbuser, 
                                                password=connect.dbpass, 
                                                host=connect.dbhost, 
                                                auth_plugin='mysql_native_password',
                                                database=connect.dbname, 
                                                autocommit=True)
    
    cursor = db_connection.cursor(dictionary=True)
    return cursor

def login_required(f):
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapped_view.__name__ = f.__name__
    return wrapped_view

def roles_required(*roles):
    def decorator(f):
        def wrapped_view(*args, **kwargs):
            if 'role' not in session or session['role'] not in roles:
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        wrapped_view.__name__ = f.__name__
        return wrapped_view
    return decorator


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        msg = "Login successful!"
        username = request.form['username']
        user_password = request.form['password']
        
        cursor = getCursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        if account and hashing.check_value(account['password_hash'], user_password, PASSWORD_SALT):
            session['user_id'] = account['user_id']
            session['username'] = account['username']
            session['role'] = account['role']
            session['profile_image'] = account['profile_image']
            return redirect(url_for('index'))
        elif account:
            msg = 'Incorrect password! Please try again.'
        else:
            msg = 'Username is not exist! Please register.'
    
    return render_template('login.html', msg=msg)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['birth_date']
        location = request.form['location']
        
        # Password validation
        if len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[a-zA-Z]', password):
            msg = 'Password must be at least 8 characters long and contain both letters and digits.'
            return render_template('register.html', msg=msg, username=username, email=email, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, location=location)

        cursor = getCursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            msg = 'Username already exists!'
            return render_template('register.html', msg=msg, username=username, email=email, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, location=location)
        
        password_hash = hashing.hash_value(password, salt=PASSWORD_SALT)
        cursor.execute('''INSERT INTO users (username, email, password_hash, first_name, last_name, birth_date, location, role, status, profile_image)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                       (username, email, password_hash, first_name, last_name, date_of_birth, location, 'member', 'active', 'default.png'))
        msg = 'Registration successful!'
        return redirect(url_for('login', msg=msg))
    return render_template('register.html', msg=msg)

@app.route('/messages', methods=['GET', 'POST'])
@login_required
def messages_board():
    cursor = getCursor()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute("INSERT INTO messages (user_id, title, content, created_at) VALUES (%s, %s, %s, %s)", (session['user_id'], title, content, datetime.now()))
    cursor.execute("""
        SELECT messages.message_id, messages.title, messages.content, messages.created_at, messages.user_id, 
               users.username, users.profile_image, users.location, 
               (SELECT COUNT(*) FROM replies WHERE replies.message_id = messages.message_id) AS reply_count
        FROM messages 
        JOIN users ON messages.user_id = users.user_id 
        ORDER BY messages.created_at DESC
    """)
    messages = cursor.fetchall()
    return render_template('allmessages.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
