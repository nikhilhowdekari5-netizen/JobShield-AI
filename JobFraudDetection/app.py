from flask import (
    Flask, render_template_string, request,
    redirect, url_for, session, flash
)

import os
import sqlite3
import joblib

from datetime import datetime
from functools import wraps
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# =====================================
# 1. CONFIGURATION
# =====================================

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "development-key-change-before-deployment"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR, "job_fraud_model.pkl"
)

DB_PATH = os.path.join(
    BASE_DIR, "job_history.db"
)

model = joblib.load(MODEL_PATH)


# =====================================
# 2. DATABASE CONNECTION
# =====================================

def get_db():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            role TEXT NOT NULL,

            created_at TEXT

        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS predictions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            job_title TEXT,

            company_name TEXT,

            prediction TEXT,

            fraud_probability REAL,

            risk_level TEXT,

            recommendation TEXT,

            checked_at TEXT,

            FOREIGN KEY(user_id) REFERENCES users(id)

        )
    """)

    # Support existing prediction databases
    columns = [
        row["name"]
        for row in conn.execute(
            "PRAGMA table_info(predictions)"
        ).fetchall()
    ]

    if "user_id" not in columns:

        conn.execute(
            "ALTER TABLE predictions ADD COLUMN user_id INTEGER"
        )

    if "recommendation" not in columns:

        conn.execute(
            "ALTER TABLE predictions ADD COLUMN recommendation TEXT"
        )

    conn.commit()
    conn.close()


init_db()


# =====================================
# 3. LOGIN REQUIRED DECORATOR
# =====================================

def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:

            return redirect(url_for("login"))

        return function(*args, **kwargs)

    return wrapper


# =====================================
# 4. ROLE REQUIRED DECORATOR
# =====================================

def role_required(required_role):

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            if "user_id" not in session:

                return redirect(url_for("login"))

            if session.get("role") != required_role:

                return "Access Denied", 403

            return function(*args, **kwargs)

        return wrapper

    return decorator


# =====================================
# 5. COMMON DESIGN
# =====================================

BASE_STYLE = """
<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f1f5f9;
    color: #1e293b;
}

header {
    background: #0f172a;
    color: white;
    padding: 20px 7%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
}

header h2 {
    margin: 0;
}

nav a {
    color: white;
    text-decoration: none;
    margin-left: 15px;
    font-weight: bold;
}

.container {
    max-width: 950px;
    margin: 45px auto;
    padding: 20px;
}

.card {
    background: white;
    padding: 30px;
    border-radius: 14px;
    box-shadow: 0 5px 20px rgba(0,0,0,.06);
}

label {
    display: block;
    margin: 18px 0 8px;
    font-weight: bold;
}

input, textarea, select {
    width: 100%;
    padding: 13px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-size: 15px;
}

button {
    width: 100%;
    padding: 14px;
    margin-top: 22px;
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    background: #1d4ed8;
}

.message {
    background: #dbeafe;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 15px;
}

.error {
    background: #fee2e2;
    color: #991b1b;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 15px;
}

a {
    color: #2563eb;
}

table {
    width: 100%;
    border-collapse: collapse;
    background: white;
}

th, td {
    padding: 13px;
    border-bottom: 1px solid #e2e8f0;
    text-align: left;
}

th {
    background: #0f172a;
    color: white;
}

@media(max-width: 600px) {

    header {
        padding: 18px;
    }

    .card {
        padding: 20px;
    }

}

</style>
"""


def navigation():

    return """
    <header>
        <h2>🛡️ JobShield AI</h2>

        <nav>
            <a href="/">Home</a>
            <a href="/history">History</a>
            <a href="/logout">Logout</a>
        </nav>
    </header>
    """


# =====================================
# 6. REGISTRATION
# =====================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()

        email = request.form.get("email", "").strip().lower()

        password = request.form.get("password", "")

        role = request.form.get("role", "")

        if not name or not email or not password:

            flash("Please fill in all fields.")

        elif role not in ["job_seeker", "employer"]:

            flash("Please select a valid role.")

        elif len(password) < 8:

            flash("Password must contain at least 8 characters.")

        else:

            conn = get_db()

            try:

                hashed_password = generate_password_hash(password)

                conn.execute("""
                    INSERT INTO users
                    (name, email, password, role, created_at)

                    VALUES (?, ?, ?, ?, ?)

                """, (
                    name,
                    email,
                    hashed_password,
                    role,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))

                conn.commit()

                flash("Registration successful! Please login.")

                conn.close()

                return redirect(url_for("login"))

            except sqlite3.IntegrityError:

                flash("This email is already registered.")

            finally:

                conn.close()

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Register - JobShield AI</title>
        {{ style|safe }}
    </head>

    <body>

        <div class="container">

            <div class="card">

                <h1>🛡️ JobShield AI</h1>

                <h2>Create Your Account</h2>

                {% with messages = get_flashed_messages() %}
                {% for message in messages %}
                    <div class="message">{{ message }}</div>
                {% endfor %}
                {% endwith %}

                <form method="POST">

                    <label>Full Name</label>

                    <input
                        type="text"
                        name="name"
                        required
                    >

                    <label>Email Address</label>

                    <input
                        type="email"
                        name="email"
                        required
                    >

                    <label>Password</label>

                    <input
                        type="password"
                        name="password"
                        minlength="8"
                        required
                    >

                    <label>Select Account Type</label>

                    <select name="role" required>

                        <option value="">Choose Role</option>

                        <option value="job_seeker">
                            Job Seeker
                        </option>

                        <option value="employer">
                            Employer
                        </option>

                    </select>

                    <button type="submit">
                        Create Account
                    </button>

                </form>

                <p>
                    Already registered?
                    <a href="/login">Login here</a>
                </p>

            </div>

        </div>

    </body>
    </html>
    """, style=BASE_STYLE)


# =====================================
# 7. LOGIN
# =====================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email", ""
        ).strip().lower()

        password = request.form.get(
            "password", ""
        )

        conn = get_db()

        user = conn.execute("""
            SELECT * FROM users
            WHERE email = ?
        """, (email,)).fetchone()

        conn.close()

        if user and check_password_hash(
            user["password"], password
        ):

            session.clear()

            session["user_id"] = user["id"]

            session["name"] = user["name"]

            session["role"] = user["role"]

            if user["role"] == "admin":

                return redirect(url_for("admin"))

            return redirect(url_for("home"))

        flash("Invalid email or password.")

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login - JobShield AI</title>
        {{ style|safe }}
    </head>

    <body>

        <div class="container">

            <div class="card">

                <h1>🛡️ JobShield AI</h1>

                <h2>Welcome Back!</h2>

                <p>Login to continue.</p>

                {% with messages = get_flashed_messages() %}
                {% for message in messages %}
                    <div class="error">{{ message }}</div>
                {% endfor %}
                {% endwith %}

                <form method="POST">

                    <label>Email Address</label>

                    <input
                        type="email"
                        name="email"
                        required
                    >

                    <label>Password</label>

                    <input
                        type="password"
                        name="password"
                        required
                    >

                    <button type="submit">
                        Login
                    </button>

                </form>

                <p>
                    Don't have an account?
                    <a href="/register">Register here</a>
                </p>

            </div>

        </div>

    </body>
    </html>
    """, style=BASE_STYLE)


# =====================================
# 8. LOGOUT
# =====================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =====================================
# 9. HOME AND FRAUD DETECTION
# =====================================

@app.route("/", methods=["GET", "POST"])
@login_required
def home():

    result = None
    result_type = None

    fraud_probability = None
    risk_level = None
    recommendation = None

    job_title = ""
    company_name = ""
    company_profile = ""
    job_description = ""
    requirements = ""
    benefits = ""

    error = None

    if request.method == "POST":

        job_title = request.form.get(
            "job_title", ""
        ).strip()

        company_name = request.form.get(
            "company_name", ""
        ).strip()

        company_profile = request.form.get(
            "company_profile", ""
        ).strip()

        job_description = request.form.get(
            "job_description", ""
        ).strip()

        requirements = request.form.get(
            "requirements", ""
        ).strip()

        benefits = request.form.get(
            "benefits", ""
        ).strip()

        if not job_title or not company_name or not job_description:

            error = "Please fill in all required fields."

        else:

            job_text = " ".join([

                job_title,

                company_profile or "Not specified",

                job_description,

                requirements or "Not specified",

                benefits or "Not specified"

            ])

            prediction = int(
                model.predict([job_text])[0]
            )

            probabilities = model.predict_proba([job_text])[0]

            classes = list(
                model.named_steps["classifier"].classes_
            )

            fraud_index = classes.index(1)

            fraud_probability = round(
                float(probabilities[fraud_index]) * 100,
                2
            )

            if fraud_probability >= 60:

                risk_level = "High"

                recommendation = (
                    "Flag this job for moderator review."
                )

            elif fraud_probability >= 30:

                risk_level = "Medium"

                recommendation = (
                    "Verify the employer and job details carefully."
                )

            else:

                risk_level = "Low"

                recommendation = (
                    "No strong fraud pattern detected. "
                    "Verify the employer independently."
                )

            if prediction == 1:

                result = "Potentially Fraudulent Job Posting"

                result_type = "fraud"

            else:

                result = "Likely Legitimate Job Posting"

                result_type = "safe"

            conn = get_db()

            conn.execute("""
                INSERT INTO predictions (

                    user_id,
                    job_title,
                    company_name,
                    prediction,
                    fraud_probability,
                    risk_level,
                    recommendation,
                    checked_at

                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?)

            """, (

                session["user_id"],
                job_title,
                company_name,
                result,
                fraud_probability,
                risk_level,
                recommendation,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            ))

            conn.commit()
            conn.close()

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>JobShield AI</title>
        {{ style|safe }}

        <style>

            .hero {
                text-align: center;
                margin-bottom: 30px;
            }

            .result {
                padding: 22px;
                margin-top: 25px;
                border-radius: 12px;
            }

            .fraud {
                background: #fee2e2;
                color: #991b1b;
            }

            .safe {
                background: #dcfce7;
                color: #166534;
            }

            .score {
                font-size: 32px;
                font-weight: bold;
            }

            .progress {
                height: 14px;
                background: #e2e8f0;
                border-radius: 20px;
                overflow: hidden;
            }

            .bar {
                height: 100%;
                background: #dc2626;
            }

        </style>
    </head>

    <body>

        {{ nav|safe }}

        <div class="container">

            <div class="hero">

                <h1>Stay Safe From Job Scams</h1>

                <h3>Welcome, {{ name }}!</h3>

                <p>
                    Check job postings using Machine Learning.
                </p>

            </div>

            <div class="card">

                <h2>Check a Job Posting</h2>

                {% if error %}
                    <div class="error">{{ error }}</div>
                {% endif %}

                <form method="POST">

                    <label>Job Title *</label>

                    <input
                        name="job_title"
                        value="{{ job_title }}"
                        required
                    >

                    <label>Company Name *</label>

                    <input
                        name="company_name"
                        value="{{ company_name }}"
                        required
                    >

                    <label>Company Profile</label>

                    <textarea
                        name="company_profile"
                    >{{ company_profile }}</textarea>

                    <label>Job Description *</label>

                    <textarea
                        name="job_description"
                        required
                    >{{ job_description }}</textarea>

                    <label>Requirements</label>

                    <textarea
                        name="requirements"
                    >{{ requirements }}</textarea>

                    <label>Benefits</label>

                    <textarea
                        name="benefits"
                    >{{ benefits }}</textarea>

                    <button type="submit">
                        🔍 Check Job Safety
                    </button>

                </form>

                {% if result %}

                <div class="result {{ result_type }}">

                    <h2>{{ result }}</h2>

                    <h3>Fraud Probability</h3>

                    <div class="score">
                        {{ fraud_probability }}%
                    </div>

                    <div class="progress">

                        <div class="bar"
                             style="width:{{ fraud_probability }}%">
                        </div>

                    </div>

                    <h3>Risk Level: {{ risk_level }}</h3>

                    <p>
                        <strong>Recommendation:</strong>
                        {{ recommendation }}
                    </p>

                </div>

                {% endif %}

                <p class="message">
                    Predictions are automated estimates.
                    Always verify employers independently.
                </p>

            </div>

        </div>

    </body>
    </html>
    """,

    style=BASE_STYLE,
    nav=navigation(),
    name=session["name"],
    result=result,
    result_type=result_type,
    fraud_probability=fraud_probability,
    risk_level=risk_level,
    recommendation=recommendation,
    job_title=job_title,
    company_name=company_name,
    company_profile=company_profile,
    job_description=job_description,
    requirements=requirements,
    benefits=benefits,
    error=error
    )


# =====================================
# 10. PREDICTION HISTORY
# =====================================

@app.route("/history")
@login_required
def history():

    conn = get_db()

    if session["role"] == "admin":

        records = conn.execute("""
            SELECT
                predictions.*,
                users.name
            FROM predictions
            LEFT JOIN users
            ON predictions.user_id = users.id
            ORDER BY predictions.id DESC
        """).fetchall()

    else:

        records = conn.execute("""
            SELECT *
            FROM predictions
            WHERE user_id = ?
            ORDER BY id DESC
        """, (session["user_id"],)).fetchall()

    conn.close()

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Prediction History</title>
        {{ style|safe }}
    </head>

    <body>

        {{ nav|safe }}

        <div class="container">

            <h1>Prediction History</h1>

            <div class="card">

                <p>Total jobs checked: {{ records|length }}</p>

                <table>

                    <tr>
                        <th>Job</th>
                        <th>Company</th>
                        <th>Prediction</th>
                        <th>Fraud %</th>
                        <th>Risk</th>
                        <th>Date</th>

                        {% if role == "admin" %}
                            <th>User</th>
                        {% endif %}
                    </tr>

                    {% for row in records %}

                    <tr>

                        <td>{{ row["job_title"] }}</td>

                        <td>{{ row["company_name"] }}</td>

                        <td>{{ row["prediction"] }}</td>

                        <td>{{ row["fraud_probability"] }}%</td>

                        <td>{{ row["risk_level"] }}</td>

                        <td>{{ row["checked_at"] }}</td>

                        {% if role == "admin" %}
                            <td>{{ row["name"] or "Unknown" }}</td>
                        {% endif %}

                    </tr>

                    {% endfor %}

                </table>

                {% if not records %}
                    <p>No history available.</p>
                {% endif %}

            </div>

        </div>

    </body>
    </html>
    """,

    style=BASE_STYLE,
    nav=navigation(),
    records=records,
    role=session["role"]
    )


# =====================================
# 11. ADMIN DASHBOARD
# =====================================

@app.route("/admin")
@role_required("admin")
def admin():

    conn = get_db()

    users = conn.execute("""
        SELECT id, name, email, role, created_at
        FROM users
        ORDER BY id DESC
    """).fetchall()

    total_users = len(users)

    total_jobs = conn.execute("""
        SELECT COUNT(*) FROM predictions
    """).fetchone()[0]

    fraud_jobs = conn.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE prediction = 'Potentially Fraudulent Job Posting'
    """).fetchone()[0]

    conn.close()

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Dashboard</title>
        {{ style|safe }}
    </head>

    <body>

        {{ nav|safe }}

        <div class="container">

            <h1>Admin Dashboard</h1>

            <div class="card">

                <h3>Total Users: {{ total_users }}</h3>

                <h3>Total Jobs Checked: {{ total_jobs }}</h3>

                <h3>Potentially Fraudulent Jobs: {{ fraud_jobs }}</h3>

                <h2>Registered Users</h2>

                <table>

                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Role</th>
                    </tr>

                    {% for user in users %}

                    <tr>

                        <td>{{ user["id"] }}</td>

                        <td>{{ user["name"] }}</td>

                        <td>{{ user["email"] }}</td>

                        <td>{{ user["role"] }}</td>

                    </tr>

                    {% endfor %}

                </table>

                <p>
                    <a href="/history">View All Predictions</a>
                </p>

            </div>

        </div>

    </body>
    </html>
    """,

    style=BASE_STYLE,
    nav=navigation(),
    users=users,
    total_users=total_users,
    total_jobs=total_jobs,
    fraud_jobs=fraud_jobs
    )


# =====================================
# 12. RUN APPLICATION
# =====================================

if __name__ == "__main__":

    app.run(debug=True)