from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from auth.db import get_db_connection


class User(UserMixin):
    """
    Represents a logged-in user.
    Flask-Login uses this object to track the session.
    """

    def __init__(self, id, username, email):
        self.id = id              # flask-login uses this internally
        self.username = username  # displayed in navbar via {{ current_user.username }}
        self.email = email

    # ── Lookup methods (static = no need to create a User first) ──

    @staticmethod
    def get_by_id(user_id):
        """
        Called by flask-login's user_loader on every request
        to rebuild the User object from session cookie.
        Returns User object or None.
        """
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # dictionary=True → rows as dicts
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return User(row["id"], row["username"], row["email"])
        return None

    @staticmethod
    def get_by_username(username):
        """
        Used during login to find the user and check password.
        Returns the full row dict (including password_hash) or None.
        """
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row  # returns None if not found

    # ── Create method ──

    @staticmethod
    def create_user(username, email, password):
        """
        Hashes the password and inserts a new user into MySQL.
        Returns True on success, False if username/email already exists.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        pw_hash = generate_password_hash(password)  # bcrypt-like hash

        try:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, pw_hash)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
