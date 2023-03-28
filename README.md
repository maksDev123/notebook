# Authentification in Notebook
This repository provides multiple files:
* auth.py - file with authentification logic
* notebook.py - file with note-taking logic
* auth_account.py - file with combination of two previous ones

This app provides user with ability create notes for particular account

### Commands

To create notes user has to login.
Unauthorized user can call following commands:
* "login" - login user
* "register" - create user

After loging in without role ADMIN user can call following commands:
* "login" - login user
* "register" - create user
* "logout" - logout from current account
* "create" - creates notebook

After loging in with role ADMIN user can call following commands:
* "login" - login user
* "register" - create user
* "logout" - logout from current account
* "create" - creates notebook
* "c permition" - create permission
* "set permition" - sets particular pemition to particular user

### Notes

After creating note new command will appear
"Notebook 0" - to access notebook 0

After typing in "Notebook 0" will be available following commands:
* "add" - add note
* "notes" - returns all notes
* "back" - back to navigation

User with permition ADMIN can create new roles and give them to other users. For example, user with role ADMIN can set ADMIN permition to other users.

By default created user with login - **admin** and password - **password** with role **ADMIN**

### Run program
```
python auth_account.py
```
