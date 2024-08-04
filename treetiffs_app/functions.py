from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask_hashing import Hashing
import re
import os
from datetime import datetime
from datetime import date
from datetime import timedelta
import mysql.connector
from treetiffs_app import app
from treetiffs_app import connect
import mysql.connector

hashing = Hashing(app)
PASSWORD_SALT = 'KsVUyGzItjo4kCg'
UPLOAD_FOLDER = 'static/profile_images'
app.config['UPLOAD_FOLDER'] = 'treetiffs_app/static/profile_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
    """Decorator to ensure that a user is logged in before accessing a view."""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def roles_required(*roles):
    """Decorator to ensure that a user has the required role(s) before accessing a view."""
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] not in roles:
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator

def active_required(f):
    """Decorator to ensure that a user has an active account before accessing a view."""
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return f(*args, **kwargs)
        cursor = getCursor()
        cursor.execute("SELECT status FROM users WHERE user_id = %s", (session['user_id'],))
        user = cursor.fetchone()
        if user['status'] == 'inactive':
            return redirect(url_for('inactive_account'))  # Redirect to a specific inactive account page
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Error handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404