import secrets

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

from models import User

password_hasher = PasswordHasher()


def hash_password(password):
    return password_hasher.hash(password)


def verify_password(password_hash, password):
    try:
        return password_hasher.verify(password_hash, password)
    except (VerifyMismatchError, InvalidHashError):
        return False


def unique_identity():
    """Generate public identifiers without exposing the database primary key."""
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    while True:
        username = "PZB-" + "".join(secrets.choice(alphabet) for _ in range(4))
        badge_id = "PZB-" + "".join(secrets.choice("0123456789") for _ in range(4)) + "-" + "".join(secrets.choice(alphabet) for _ in range(4))
        exists = User.query.filter((User.username == username) | (User.badge_id == badge_id)).first()
        if not exists:
            return username, badge_id
