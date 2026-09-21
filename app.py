import os
from pathlib import Path

import click
from flask import Flask, abort, flash, redirect, render_template, send_from_directory, url_for
from flask_login import current_user, login_required, login_user, logout_user

from config import Config
from extensions import csrf, db, limiter, login_manager, migrate
from forms import LoginForm, RegistrationForm
from models import User
from security import hash_password, unique_identity, verify_password


PROJECT_ROOT = Path(__file__).resolve().parent


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="assets", static_url_path="/static")
    app.config.from_object(Config)

    if os.environ.get("FLASK_ENV") == "production" and app.config["SECRET_KEY"] == "development-only-change-me":
        raise RuntimeError("SECRET_KEY must be set in production.")

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    limiter.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = "Enter your PZB Badge details to continue."
    login_manager.login_message_category = "info"

    @app.cli.command("init-db")
    def init_db():
        """Create the local database tables. Use migrations before production changes."""
        db.create_all()
        click.echo("PZB database is ready.")

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/about")
    def about():
        return render_template("about.html")

    @app.get("/mission")
    def mission():
        return render_template("mission.html")

    @app.get("/timeline")
    def timeline():
        return render_template("timeline.html")

    @app.get("/archive")
    def archive():
        return render_template("archive.html")

    @app.get("/badge")
    def badge():
        return redirect(url_for("dashboard" if current_user.is_authenticated else "register"))

    @app.route("/join", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
        form = RegistrationForm()
        if form.validate_on_submit():
            username, badge_id = unique_identity()
            user = User(
                display_name=form.display_name.data.strip(),
                username=username,
                badge_id=badge_id,
                password_hash=hash_password(form.password.data),
                interests=",".join(form.interests.data),
                country=(form.country.data or "").strip() or None,
                avatar_url=(form.avatar_url.data or "").strip() or None,
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("badge_ready"))
        return render_template("auth/register.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    @limiter.limit("5 per minute")
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data.strip().upper()
            user = User.query.filter_by(username=username).first()
            if user and verify_password(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for("dashboard"))
            flash("That PZB username or password is not correct.", "error")
        return render_template("auth/login.html", form=form)

    @app.post("/logout")
    @login_required
    def logout():
        logout_user()
        flash("You have left PZB safely.", "info")
        return redirect(url_for("home"))

    @app.get("/badge-ready")
    @login_required
    def badge_ready():
        return render_template("portal/badge_ready.html")

    @app.get("/home")
    @login_required
    def dashboard():
        return render_template("portal/dashboard.html")

    @app.get("/profile")
    @login_required
    def profile():
        return render_template("portal/profile.html")

    @app.get("/assets/<path:filename>")
    def legacy_assets(filename):
        return send_from_directory(PROJECT_ROOT / "assets", filename)

    @app.get("/<filename>")
    def root_images(filename):
        allowed_files = {"pzb-logo.png", "fav.png", "White.png", "CNAME"}
        if filename not in allowed_files:
            abort(404)
        return send_from_directory(PROJECT_ROOT, filename)

    @app.get("/founders/nathan-shako")
    def nathan_profile():
        return send_from_directory(PROJECT_ROOT / "founders" / "nathan-shako", "index.html")

    @app.get("/founder/<name>")
    def founder_profile(name):
        if name not in {"dan-mwamba", "yoasi-solomon"}:
            abort(404)
        return send_from_directory(PROJECT_ROOT / "founder" / name, "index.html")

    @app.get("/about.html")
    def legacy_about(): return redirect(url_for("about"), code=301)
    @app.get("/index.html")
    def legacy_home(): return redirect(url_for("home"), code=301)
    @app.get("/mission.html")
    def legacy_mission(): return redirect(url_for("mission"), code=301)
    @app.get("/timeline.html")
    def legacy_timeline(): return redirect(url_for("timeline"), code=301)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_ENV") != "production")
