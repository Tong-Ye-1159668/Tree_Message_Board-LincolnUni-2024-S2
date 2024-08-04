from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
from flask_hashing import Hashing
import re
import os
from datetime import datetime
from datetime import date
from datetime import timedelta
import mysql.connector
from treetiffs_app import app
from treetiffs_app import connect
from treetiffs_app.functions import getCursor
from treetiffs_app.functions import login_required
from treetiffs_app.functions import roles_required
from treetiffs_app.functions import active_required

# User management page
@app.route('/admin/users', methods=['GET', 'POST'])
@roles_required('admin')
@active_required
def user_management():
    """This is the user management page for the admin."""
    search_member = request.form.get('search_member')
    cursor = getCursor()

    # Search for users by username, first name, or last name
    if search_member:
        cursor.execute("SELECT * FROM users WHERE username LIKE %s OR first_name LIKE %s OR last_name LIKE %s", 
                       (f"%{search_member}%", f"%{search_member}%", f"%{search_member}%"))
    # If no search words is provided, show all users
    else:
        cursor.execute("SELECT * FROM users")
    
    users = cursor.fetchall()
    return render_template('user_management.html', users=users, search_member=search_member)

# Route for editing a user's role and status
@app.route('/admin/user/<int:user_id>', methods=['GET', 'POST'])
@roles_required('admin')
@active_required
def user_edit(user_id):
    """This is the user edit page for the admin."""
    cursor = getCursor()
    if request.method == 'POST':
        status = request.form.get('status')
        role = request.form.get('role')

        # Update the user's role and status
        cursor.execute("UPDATE users SET status = %s, role = %s WHERE user_id = %s", (status, role, user_id))
        flash('User updated successfully!', 'success')
        return redirect(url_for('user_edit', user_id=user_id))
    
    # Get the user's current role and status
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    return render_template('user_edit.html', user=user)