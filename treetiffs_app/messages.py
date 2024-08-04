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
from treetiffs_app.functions import getCursor
from treetiffs_app.functions import login_required
from treetiffs_app.functions import roles_required
from treetiffs_app.functions import active_required

# Route for posting new messages
@app.route('/messages', methods=['GET', 'POST'])
@login_required
@active_required
def messages():
    """This is the page with messages and replies."""
    cursor = getCursor()

    # If the form is submitted, insert the message into the database
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute("INSERT INTO messages (user_id, title, content, created_at) VALUES (%s, %s, %s, %s)", (session['user_id'], title, content, datetime.now()))
        return redirect(url_for('messages'))
    
    # Get all messages and their replies from the database
    cursor.execute("""
        SELECT messages.message_id, messages.title, messages.content, messages.created_at, 
               messages.user_id, users.username, users.profile_image, users.location
        FROM messages 
        JOIN users ON messages.user_id = users.user_id 
        ORDER BY messages.created_at DESC
    """)
    messages = cursor.fetchall()
    
    # Get all replies for each message
    for message in messages:
        cursor.execute("""
            SELECT replies.reply_id, replies.message_id, replies.content, replies.created_at,
                   replies.user_id, users.username, users.profile_image, users.location
            FROM replies 
            JOIN users ON replies.user_id = users.user_id 
            WHERE replies.message_id = %s
            ORDER BY replies.created_at ASC
        """, (message['message_id'],))
        message['replies'] = cursor.fetchall()
    
    return render_template('messages.html', messages=messages)

# Route for posting replies
@app.route('/reply/<int:message_id>', methods=['POST'])
@login_required
@active_required
def post_reply(message_id):
    """This is the route for posting replies to current messages"""
    content = request.form['content']
    cursor = getCursor()
    # Insert the reply into the database
    cursor.execute("INSERT INTO replies (message_id, user_id, content, created_at) VALUES (%s, %s, %s, %s)",
                    (message_id, session['user_id'], content, datetime.now()))
    return redirect(url_for('messages'))

# Route for deleting messages and replies
@app.route('/message/delete/<int:message_id>', methods=['POST'])
@login_required
@active_required
def delete_message(message_id):
    """This is the route for deleting the message and all replies"""
    cursor = getCursor()
    cursor.execute("SELECT user_id FROM messages WHERE message_id = %s", (message_id,))
    user_id = cursor.fetchone()['user_id']
    # Check if the member is the author of the message or a moderator/admin
    if session['user_id'] == user_id or session['role'] in ['moderator', 'admin']:
        cursor.execute("DELETE FROM replies WHERE message_id = %s", (message_id,))
        cursor.execute("DELETE FROM messages WHERE message_id = %s", (message_id,))
    return redirect(url_for('messages'))

# Route for deleting replies
@app.route('/reply/delete/<int:reply_id>', methods=['POST'])
@login_required
@active_required
def delete_reply(reply_id):
    """This is the route for deleting the repliy"""
    cursor = getCursor()
    cursor.execute("SELECT user_id FROM replies WHERE reply_id = %s", (reply_id,))
    user_id = cursor.fetchone()['user_id']
    # Check if the member is the author of the reply or a moderator/admin
    if session['user_id'] == user_id or session['role'] in ['moderator', 'admin']:
        cursor.execute("DELETE FROM replies WHERE reply_id = %s", (reply_id,))
    return redirect(url_for('messages'))