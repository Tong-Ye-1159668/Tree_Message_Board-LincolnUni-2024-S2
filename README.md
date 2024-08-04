# Tree_Message_Board (Tree Tiffs)

This sample app (Tree Tiffs) demonstrates a simple message board that allows users to
register, log in, view and post messages and replies, and change profiles. 

There are three user roles in this system:
- **Member**
- **Moderator**
- **Admin**

Anyone who registers via the app will be a **Member**. The way to create
**Moderator** or **Admin** accounts in this message board app is to insert them directly
into the database. Once you have an **admin account**, you can use an admin account to change a user's role from member to Moderator or Admin. 

## Getting this Webapp Running

To run the app yourself, you'll need to:

1. Open the project in Visual Studio Code.
2. Create yourself a virtual environment.
3. Install all of the packages listed in requirements.txt 
4. Use the [Tree_Message_Board_local.sql](<Tree_Message_Board_local.sql>) to create your own
   copy of the **tree_message_board** database.
5. Use the [Database Population Script](<Populate Database.sql>) to populate
   the **tree_message_board** ***users*** table with example members, moderators and admins.
6. Modify [connect.py](treetiffs_app/connect.py) with the connection details for
   your local database server.
7. Run [The Python/Flask application](run.py).

At that point, you should be able to register yourself a new **member** account
or log in using one of the **member**, **moderator**, or **admin** accounts listed in
the [Database Population Script](<Populate Database.sql>).

Enjoy talking about your trees and neighbours now!

## Database Scripts

While we're talking about the database, you should take a look at:
- [MySQL script to create the necessary database](<Tree_Message_Board_local.sql>)
- [MySQL script to populate the database with users](<Populate Database.sql>)
- [Python script to create password hashes](password_hash_generator.py)

## Passwords

One of the key things about this login system is that it doesn’t actually store users’ passwords in the database. Instead, it stores a hashed version of the password, which is generated using the [Python script to create password hashes](password_hash_generator.py) script. This ensures that even if the database is compromised, the actual passwords remain secure.

## Usage

1. **Register an account**: 

Enter the registration page by clicking **"Log in/Sign up"** in the upper right corner of the Header and then clicking **"Sign up now"**.

If you want to modify the code,  check **register.py**

2. **Log in**: 

Enter the login page by clicking **"Log in/Sign up"** in the upper right corner of the Header.

If you want to modify the code,  check **login.py**


3. **Post messages and replies**: 

Start interacting with the community by posting messages and replying to others.

After logging in, click **"View Message"** on the homepage or **"Messages"** in the Header to enter the Message board page.

If you want to modify the code,  check **messages.py**


4. **Change Profile**: 

Update your profile information including profile image and password as needed.

After logging in, click your **profile image** in the upper right corner of the Header and then clicking **"Profile"** in the dropdown menu to enter the profile page.

If you want to modify the code,  check **profiles.py**

5. **User management**: 

The page for managing all users, including searching users by username or first name or last name, and changing the user's role and status.

After logging in, click **"User Management"** in the Header to enter the user management page.

If you want to modify the code,  check **user_management.py**


## Author

Tong Ye 1159668

## Acknowledgments

- loginexample from our Lecturer Patricia
- Lectorial from our Examiner Harley
- Flask documentation
- MySQL documentation