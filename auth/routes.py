from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from auth.models import User

# Blueprint = a mini Flask app that you register in the main app
auth_bp = Blueprint("auth", __name__)


# ── LOGIN ────────────────────────────────────────────────

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # If already logged in, skip to home
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        # 1. Get form data (matches login.html field names)
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # 2. Look up user in MySQL
        row = User.get_by_username(username)

        # 3. Check: user exists AND password matches hash
        if row and check_password_hash(row["password_hash"], password):
            # Create User object and log them in (sets session cookie)
            user = User(row["id"], row["username"], row["email"])
            login_user(user)
            return redirect(url_for("home"))

        # 4. If we get here, login failed
        flash("Invalid username or password", "error")

    # GET request or failed POST → show the login form
    return render_template("login.html")


# ── REGISTER ─────────────────────────────────────────────

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        # 1. Get form data (matches register.html field names)
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        # 2. Validate
        if not username or not email or not password:
            flash("All fields are required", "error")
        elif len(password) < 6:
            flash("Password must be at least 6 characters", "error")
        elif password != confirm:
            flash("Passwords don't match", "error")
        elif User.get_by_username(username):
            flash("Username already taken", "error")
        else:
            # 3. Create user in MySQL
            success = User.create_user(username, email, password)
            if success:
                flash("Account created! Please log in.", "success")
                return redirect(url_for("auth.login"))
            else:
                flash("Email already in use or database error", "error")

    return render_template("register.html")


# ── LOGOUT ───────────────────────────────────────────────

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()  # clears the session cookie
    return redirect(url_for("auth.login"))
