from auth import Authenticator, Authorizor, UsernameAlreadyExists,\
PasswordTooShort, InvalidUsername, InvalidPassword, NotPermittedError,NotLoggedInError, PermissionError
from notebook import Note, Notebook



authenticator = Authenticator()

authorizor = Authorizor(authenticator)

authenticator.add_user("admin", "password")

authorizor.add_permission("ADMIN")

authorizor.permit_user("ADMIN", "admin")

USER_AUTHORIZED = None
CURRENT_NOTEBOOK = None


NAVIGATION_NOT_LOGGED_IN = """
login - login user
register - create user
"""
NAVIGATION_LOGGED_IN = NAVIGATION_NOT_LOGGED_IN + """logout - logout from current account
create - creates notebook"""

NOTEBOOK_NAVIGATION = """
Notebook navigation

add - add note
notes - returns all notes
back - back to navigation
"""



while True:
    if USER_AUTHORIZED:
        print(f"***** Logged in as {USER_AUTHORIZED.username} *****")
        if CURRENT_NOTEBOOK:
            print(NOTEBOOK_NAVIGATION)
        else:
            try:
                authorizor.check_permission("ADMIN", USER_AUTHORIZED.username)
            except NotPermittedError:
                print(NAVIGATION_LOGGED_IN)
                for i, _ in enumerate(USER_AUTHORIZED.notebooks):
                    print(f"Notebook {i} - to access notebook {i}")
            else:
                print(NAVIGATION_LOGGED_IN+"""
c permition - create permission
set permition - sets particular pemition to particular user""")
                for i, _ in enumerate(USER_AUTHORIZED.notebooks):
                    print(f"Notebook {i} - to access notebook {i}")
            print("")

    else:
        print(NAVIGATION_NOT_LOGGED_IN)

    move = input(">>> ")
    if USER_AUTHORIZED:
        if CURRENT_NOTEBOOK:
            if move == "add":
                print("")
                print("Add text of note")
                text = input(">>> ")
                CURRENT_NOTEBOOK.new_note(text)
            elif move == "notes":
                print("")
                if CURRENT_NOTEBOOK.notes:
                    for index, note in enumerate(CURRENT_NOTEBOOK.notes):
                        print(f"Note {index + 1} - {note.memo}")
                print("")
            elif move == "back":
                CURRENT_NOTEBOOK = None
        else:
            try:
                authorizor.check_permission("ADMIN", USER_AUTHORIZED.username)
            except NotPermittedError:
                pass
            else:
                if move == "set permition":
                    if not USER_AUTHORIZED:
                        print("You have to login to set permition")
                        continue
                    try:
                        authorizor.check_permission("ADMIN", USER_AUTHORIZED.username)
                    except NotPermittedError:
                        print("You must have ADMIN permition to create permitions")
                    except PermissionError:
                        print("Permission does not exist")
                    else:
                        print("Permition name")
                        permition_name = input(">>> ")
                        print("Username")
                        username = input(">>> ")
                        try:
                            authorizor.permit_user(permition_name, username)
                        except PermissionError:
                            print("Permission does not exist")
                        except InvalidUsername:
                            print("You provided unvalid username")
                        else:
                            print("Permition is set successfully")

                elif move == "c permition":
                    if not USER_AUTHORIZED:
                        print("You have to login to create permition")
                        continue
                    try:
                        authorizor.check_permission("ADMIN", USER_AUTHORIZED.username)
                    except NotPermittedError as e:
                        print("You must have ADMIN permition to create permitions")
                    except PermissionError:
                        print("Permission ADMIN does not exist")
                    else:
                        print("Permition name")
                        permition_name = input(">>> ")
                        try:
                            authorizor.add_permission(permition_name)
                        except PermissionError:
                            print("Permition already exists")
                        else:
                            print("Permition successfully created")
            if move == "logout":
                authenticator.logout(USER_AUTHORIZED.username)
                USER_AUTHORIZED = None
                print("Logged out successfully")
                continue

            elif move == "create":
                notebook = Notebook()
                USER_AUTHORIZED = USER_AUTHORIZED.add_notebook(notebook)
                print(USER_AUTHORIZED)

            elif move.split(" ")[0] == "Notebook":
                try:
                    index = int(move.split(" ")[1])
                except TypeError:
                    continue

                if 0 <= index < len(USER_AUTHORIZED.notebooks):
                    CURRENT_NOTEBOOK = USER_AUTHORIZED.notebooks[index]

    else:
        if move == "login":
            print("")
            print("Log in")
            print("Enter username")
            username = input(">>> ")
            print("Enter password")
            password = input(">>> ")
            try:
                USER_AUTHORIZED = authenticator.login(username, password)
            except InvalidUsername as e:
                print(f"Username {e.username} is invalid")
            except InvalidPassword as e:
                print(f"Password {password} is invalid")
            else:
                print("Logged in successfully")
                continue

        elif move == "register":
            print("")
            print("Register")
            print("Enter username")
            username = input(">>> ")
            print("Enter password")
            password = input(">>> ")

            try:
                authenticator.add_user(username, password)
            except UsernameAlreadyExists as e:
                print(f"Username {e.username} already exists")
            except PasswordTooShort as e:
                print(f"Password {password} is to short. Must be 6+ symbols")
            else:
                print("User created successfully")

    