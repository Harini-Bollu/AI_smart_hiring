import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "smart_hiring.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            salt TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def add_user(username, email, salt, password_hash):
    try:
        conn = get_connection()

        conn.execute(
            """
            INSERT INTO users
            (username, email, salt, password_hash)
            VALUES (?, ?, ?, ?)
            """,
            (
                username,
                email,
                salt,
                password_hash
            )
        )

        conn.commit()
        conn.close()

        return True, "Account created successfully."

    except sqlite3.IntegrityError as e:

        if "username" in str(e).lower():
            return False, "Username already exists."

        if "email" in str(e).lower():
            return False, "Email already exists."

        return False, "Username or email already exists."

    except Exception as e:
        return False, f"Database error: {e}"


def get_user_by_login(login):
    conn = get_connection()

    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
           OR email = ?
        LIMIT 1
        """,
        (login, login)
    ).fetchone()

    conn.close()

    if user:
        return dict(user)

    return None


def get_user_by_id(user_id):
    conn = get_connection()

    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        LIMIT 1
        """,
        (user_id,)
    ).fetchone()

    conn.close()

    if user:
        return dict(user)

    return None


def update_password(user_id, salt, password_hash):
    conn = get_connection()

    conn.execute(
        """
        UPDATE users
        SET salt = ?, password_hash = ?
        WHERE id = ?
        """,
        (
            salt,
            password_hash,
            user_id
        )
    )

    conn.commit()
    conn.close()


def delete_user(user_id):
    conn = get_connection()

    conn.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()


init_db()