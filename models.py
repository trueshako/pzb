from datetime import datetime, timezone

from flask_login import UserMixin

from extensions import db, login_manager


class User(UserMixin, db.Model):
    """The Phase 1 PZB identity record. XP and achievements grow in later phases."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(32), nullable=False)
    username = db.Column(db.String(16), nullable=False, unique=True, index=True)
    badge_id = db.Column(db.String(20), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    interests = db.Column(db.String(320), nullable=False, default="")
    country = db.Column(db.String(80), nullable=True)
    avatar_url = db.Column(db.String(500), nullable=True)
    xp = db.Column(db.Integer, nullable=False, default=0)
    level = db.Column(db.Integer, nullable=False, default=1)
    role = db.Column(db.String(32), nullable=False, default="Story Explorer")
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    @property
    def initials(self):
        return "".join(part[0] for part in self.display_name.split()[:2]).upper() or "PZB"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
