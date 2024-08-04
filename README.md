# Tree_Message_Board

This sample app demonstrates a simple message board that allows users to
register, log in, change profiles, view and post messages and replies. 

There are three user roles in this system:
- **Member**
- **Moderator**
- **Admin**

Anyone who registers via the app will be a **Member**. The only way to create
**Moderator** or **Admin** accounts in this simple app is to insert them directly
into the database. 

## Getting this Example Running

To run the example yourself, you'll need to:

1. Open the project in Visual Studio Code.
2. Create yourself a virtual environment.
3. Install all of the packages listed in requirements.txt 
4. Use the [Database Creation Script](<Create Database.sql>) to create your own
   copy of the **tree_message_board** database.
5. Use the [Database Population Script](<Populate Database.sql>) to populate
   the **tree_message_board** ***users*** table with example members, moderators and admins.
6. Modify [connect.py](loginapp/connect.py) with the connection details for
   your local database server.
7. Run [The Python/Flask application](run.py).

At that point, you should be able to register yourself a new **member** account
or log in using one of the **member**, **moderator**, or **admin** accounts listed in
the [Database Population Script](<Populate Database.sql>).

Enjoy!

## Database Scripts

While we're talking about the database, you should take a look at:
- [MySQL script to create the necessary database](<Create Database.sql>)
- [MySQL script to populate the database with users](<Populate Database.sql>)
- [Python script to create password hashes](password_hash_generator.py)

What's that third one? Well, for that we need to talk about...

## Passwords

One of the key things about this login system is that it doesn't actually store
users' passwords in the database. 