# Login & Signup Changes

This document summarizes the changes made to add user authentication (signup/login/logout) to the MutualScope project.

## New Files
- `auth/db.py`
  - MySQL connection helper: `get_db_connection()`.
  - Table initializer: `init_db()` creates `users` table if missing.
- `auth/models.py`
  - `User` model for `flask-login` with helpers:
    - `get_by_id()` for session reload.
    - `get_by_username()` for login lookup.
    - `create_user()` for registration (password hashing + insert).
- `auth/routes.py`
  - Blueprint `auth_bp` with routes:
    - `GET/POST /login` (auth.login)
    - `GET/POST /register` (auth.register)
    - `GET /logout` (auth.logout)
- `web/templates/login.html`
  - Login form with username + password and flash messages.
- `web/templates/register.html`
  - Signup form with username + email + password + confirm password and flash messages.

## Updated Files
- `web/app.py`
  - Added `flask-login` setup (`LoginManager`, `user_loader`).
  - Registered the `auth_bp` blueprint.
  - Added `init_db()` call on startup.
  - Protected core routes with `@login_required`:
    - `/` (home)
    - `/fund/<scheme_code>`
    - `/compare`
- `web/templates/base.html`
  - Added conditional navbar links (Login / Logout + username).
  - Added global flash message block.
- `web/static/css/styles.css`
  - Added full auth UI styling:
    - `.auth-wrapper`, `.auth-card`, `.auth-form`, `.auth-btn`, `.auth-link`
    - Input styling, icon placement, password toggle button
    - Flash message styles (`.flash-msg`, `.flash-error`, `.flash-success`)
- `requirements.txt`
  - Added auth and DB dependencies:
    - `flask`, `flask-login`, `mysql-connector-python`
- `.env.example`
  - Added MySQL connection settings and `FLASK_SECRET_KEY`.

## Database Changes
- A `users` table is created automatically by `init_db()`:
  - `id` (primary key)
  - `username` (unique)
  - `email` (unique)
  - `password_hash`
  - `created_at`

## Runtime Notes
- MySQL must be running and accessible using `.env` values.
- Passwords are hashed using `werkzeug.security`.
- Auth is session-based using `flask-login`.

## Quick Validation
1. Create user in `/register`.
2. Login at `/login`.
3. Verify `/`, `/fund/<code>`, `/compare` require login.
4. Logout clears the session.

## Changed Code Blocks

### `auth/db.py`
```python
def init_db():
    """
    Ensure the users table exists. Safe to call on startup.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    cursor.close()
    conn.close()
```

### `web/app.py`
```python
from auth.db import init_db

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

app.register_blueprint(auth_bp)
init_db()

@app.route('/', methods=['GET', 'POST'])
@login_required
 def home():
    ...

@app.route('/fund/<int:scheme_code>')
@login_required
 def fund(scheme_code):
    ...

@app.route('/compare', methods=['GET', 'POST'])
@login_required
 def compare_funds():
    ...
```

### `web/templates/base.html`
```html
{% if current_user.is_authenticated %}
<span class="nav-user">{{ current_user.username }}</span>
<a href="{{ url_for('auth.logout') }}" class="nav-link nav-link--logout">Logout</a>
{% else %}
<a href="{{ url_for('auth.login') }}" class="nav-link nav-link--login {% if request.path == '/login' %}active{% endif %}">Login</a>
{% endif %}
```

```html
{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}
<div class="flash-container flash-container--global">
    {% for category, message in messages %}
    <div class="flash-msg flash-{{ category }}">{{ message }}</div>
    {% endfor %}
</div>
{% endif %}
{% endwith %}
```

### `web/templates/login.html`
```html
<form class="auth-form" method="POST" action="{{ url_for('auth.login') }}">
    <input name="username" type="text" required>
    <input name="password" type="password" required>
    <button type="submit" class="auth-btn">Sign In</button>
</form>
```

### `web/templates/register.html`
```html
<form class="auth-form" method="POST" action="{{ url_for('auth.register') }}">
    <input name="username" type="text" required>
    <input name="email" type="email" required>
    <input name="password" type="password" required>
    <input name="confirm_password" type="password" required>
    <button type="submit" class="auth-btn auth-btn--register">Create Account</button>
</form>
```

### `web/static/css/styles.css`
```css
.auth-wrapper { /* ... */ }
.auth-card { /* ... */ }
.auth-form { /* ... */ }
.auth-btn { /* ... */ }
.auth-link { /* ... */ }
.flash-msg { /* ... */ }
.flash-error { /* ... */ }
.flash-success { /* ... */ }
.nav-user { /* ... */ }
.nav-link--login { /* ... */ }
.nav-link--logout { /* ... */ }
```

### `requirements.txt`
```text
flask>=2.3.0
flask-login>=0.6.0
mysql-connector-python>=8.0.0
```

### `.env.example`
```dotenv
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=mutualscope_db
FLASK_SECRET_KEY=your-secret-key-here
```
