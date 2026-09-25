import hashlib
import hmac
import secrets

import db


ITERATIONS = 120000


def hash_password(password, salt=None):

    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        ITERATIONS
    ).hex()

    return salt, password_hash


def verify_password(password, salt, stored_hash):

    _, password_hash = hash_password(
        password,
        salt
    )

    return hmac.compare_digest(
        password_hash,
        stored_hash
    )


def register_user(username, email, password):

    username = username.strip()
    email = email.strip().lower()

    if not username:
        return False, "Username is required."

    if not email:
        return False, "Email is required."

    if "@" not in email:
        return False, "Please enter a valid email address."

    if len(password) < 6:
        return False, "Password must contain at least 6 characters."

    salt, password_hash = hash_password(password)

    return db.add_user(
        username,
        email,
        salt,
        password_hash
    )


def login_user(login, password):

    login = login.strip()

    if not login:
        return None, "Please enter username or email."

    if not password:
        return None, "Please enter your password."

    user = db.get_user_by_login(login)

    if user is None:
        return None, "Invalid username/email or password."

    valid = verify_password(
        password,
        user["salt"],
        user["password_hash"]
    )

    if not valid:
        return None, "Invalid username/email or password."

    return user, "Login successful."


def get_user(user_id):

    return db.get_user_by_id(user_id)


def change_password(user_id, old_password, new_password):

    user = db.get_user_by_id(user_id)

    if user is None:
        return False, "User not found."

    if not verify_password(
        old_password,
        user["salt"],
        user["password_hash"]
    ):
        return False, "Current password is incorrect."

    if len(new_password) < 6:
        return False, "New password must contain at least 6 characters."

    salt, password_hash = hash_password(
        new_password
    )

    db.update_password(
        user_id,
        salt,
        password_hash
    )

    return True, "Password changed successfully."