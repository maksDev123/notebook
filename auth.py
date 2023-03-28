""" Auth """

import hashlib

class AuthException(Exception):
    """ This exaption ocures when problems with Authentification """
    def __init__(self, username, user=None):
        """ Init AuthException """
        super().__init__(username, user)
        self.username = username
        self.user = user


class UsernameAlreadyExists(AuthException):
    """ This exaption ocures when username already exists """
    def __init__(self, username, user=None):
        """ Init UsernameAlreadyExists exeption """
        super().__init__(username, user)


class PasswordTooShort(AuthException):
    """ This error ocures when password is too short """



class InvalidUsername(AuthException):
    """ This error ocures when invalid username is given """



class InvalidPassword(AuthException):
    """ This error ocures when invalid password is given """


class PermissionError(Exception):
    """ This error ocures when permission does not exist """


class NotLoggedInError(AuthException):
    """ This error ocures when user is not logged in """



class NotPermittedError(AuthException):
    """ This error ocures when user does not have permition on something """


class User:
    """ User class """
    def __init__(self, username, password):
        """Create a new user object. The password
        will be encrypted before storing."""
        self.username = username
        self.password = self._encrypt_pw(password)
        self.is_logged_in = False
        self.notebooks = []

    def add_notebook(self, notebook):
        """ Ads notebook to user s"""
        self.notebooks.append(notebook)
        return self

    def _encrypt_pw(self, password):
        """Encrypt the password with the username and return
        the sha digest."""
        hash_string = self.username + password
        hash_string = hash_string.encode("utf8")
        return hashlib.sha256(hash_string).hexdigest()

    def check_password(self, password):
        """Return True if the password is valid for this
        user, false otherwise."""
        encrypted = self._encrypt_pw(password)
        return encrypted == self.password


class Authenticator:
    """ Class for authentication """
    def __init__(self):
        """Construct an authenticator to manage
        users logging in and out."""
        self.users = {}

    def add_user(self, username, password):
        """ Create user """
        if username in self.users:
            raise UsernameAlreadyExists(username)
        if len(password) < 6:
            raise PasswordTooShort(username)
        self.users[username] = User(username, password)

    def login(self, username, password):
        """ Login user """
        try:
            user = self.users[username]
        except KeyError:
            raise InvalidUsername(username)

        if not user.check_password(password):
            raise InvalidPassword(username, user)

        user.is_logged_in = True
        return user

    def logout(self, username):
        """ Logout from user """
        try:
            user = self.users[username]
        except KeyError:
            return

        user.is_logged_in = False
        return

    def is_logged_in(self, username):
        """ Check whether logged in """
        if username in self.users:
            return self.users[username].is_logged_in
        return False


class Authorizor:
    """ Class for authorizoration """
    def __init__(self, authenticator):
        self.authenticator = authenticator
        self.permissions = {}

    def add_permission(self, perm_name):
        """Create a new permission that users
        can be added to"""

        # self.check_permission("ADMIN", user_create)

        try:
            _ = self.permissions[perm_name]
        except KeyError:
            self.permissions[perm_name] = set()
        else:
            raise PermissionError("Permission Exists")

    def permit_user(self, perm_name, username):
        """Grant the given permission to the user"""

        # self.check_permission("ADMIN", user_create)

        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            raise PermissionError("Permission does not exist")
        else:
            if username not in self.authenticator.users:
                raise InvalidUsername(username)
            perm_set.add(username)

    def check_permission(self, perm_name, username):
        """ Checks particular permition in particular user """
        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            raise PermissionError("Permission does not exist")
        else:
            if username not in perm_set:
                raise NotPermittedError(username)
            else:
                return True
